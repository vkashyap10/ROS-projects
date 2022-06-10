#!/usr/bin/env python

# this node subscribes to preceived info topic and queires the bayesian network. It then publishes to robot_info_topic

from __future__ import print_function

import sys
import rospy
from cr_week8_test.srv import *
from cr_week8_test.msg import robot_info, perceived_info
import imp; imp.find_module('bayesian_belief_networks')
from bayesian_belief_networks.ros_utils import *
from bayesian_belief_networks.msg import Observation, Result
from bayesian_belief_networks.srv import Query

def callback(data):

    # call bbn service with perceived information
    rospy.wait_for_service('predict_robot_expression/query')
    print("service initialised")
    try:
	# initialise a query object for the constructed bbn
	query = rospy.ServiceProxy('predict_robot_expression/query', Query)
        msg = []
	
	# query based on availability of information. 0 means the variable was not observed
	if(data.object_size !=0):
            o = Observation()
            o.node = 'O'
            o.evidence = str(data.object_size)
            msg.append(o)

	if(data.human_action !=0):
            o = Observation()
            o.node = 'HA'
            o.evidence = str(data.human_action)
            msg.append(o)

	if(data.human_expression !=0):
            o = Observation()
            o.node = 'HE'
            o.evidence = str(data.human_expression)
            msg.append(o)
	
	# query bbn and get response
        resp1 = query(msg) 
	for res in resp1.results:
            if(res.node =="RE" and res.Value=="3"):
		p_neutral = res.Marginal
	    if(res.node =="RE" and res.Value=="2"):
		p_sad = res.Marginal
	    if(res.node =="RE" and res.Value=="1"):
		p_happy = res.Marginal   

    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

    # publish robot expression to robot info topic

    # initialise robot_info  message object
    robot_info_var = robot_info()
    robot_info_var.id = data.id
    robot_info_var.p_happy = p_happy
    robot_info_var.p_sad = p_sad
    robot_info_var.p_neutral = p_neutral

    # publish to topic
    rospy.loginfo(robot_info_var)
    pub.publish(robot_info_var)

    print("published data")


if __name__ == "__main__":

    # initialise node
    rospy.init_node('robot_controller', anonymous=True)
    
    # initialise publisher to publish robot expressions
    pub = rospy.Publisher('robot_info_topic', robot_info, queue_size=10)

    # subscribe to perceived info topic
    rospy.Subscriber('perceived_info_topic', perceived_info, callback)

    rospy.spin()
