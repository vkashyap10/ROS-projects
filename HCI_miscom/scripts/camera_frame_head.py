#!/usr/bin/env python

# listen to fluency and generate data for hand velocity and height

import rospy
import numpy as np
# import messages to be used
from std_msgs.msg import Float64
from std_msgs.msg import String

# callback will subsribe to 
def callback_a1(data):

    if data.data == 'fluent':
        # head nod: high in fluent discussions
        head_nod_rate = list(np.random.normal(0.5, 0.03, 1))[0]
        
    else:
        # head nod: low in miscomm
        head_nod_rate = list(np.random.normal(0.2, 0.05, 1))[0]
    
    # initialise cubic_traj_coeffs  message object
    htc_head_var = Float64()

    # initialise cubic_traj coeffs msg
    htc_head_var.data = head_nod_rate
    
    # publish to topic
    rospy.loginfo(htc_head_var)
    pub2.publish(htc_head_var)

    print("published data to agent 2")

    return

def callback_a2(data):

    if data.data == 'fluent':
        # head nod: high in fluent discussions
        head_nod_rate = list(np.random.normal(0.3, 0.03, 1))[0]
        
    else:
        # head nod: low in miscomm
        head_nod_rate = list(np.random.normal(0.5, 0.05, 1))[0]
    
    # initialise cubic_traj_coeffs  message object
    htc_head_var = Float64()

    # initialise cubic_traj coeffs msg
    htc_head_var.data = head_nod_rate
    
    # publish to topic
    rospy.loginfo(htc_head_var)
    pub1.publish(htc_head_var)

    print("published data to agent 1")

    return

if __name__ == '__main__':

    # initialise node
    rospy.init_node('Camera_head_nods', anonymous=False)

    # subscribe to agent 1 fluency tag
    rospy.Subscriber('fluency_agent_1', String, callback_a1)

    # subscribe to agent 2 fluency tag
    rospy.Subscriber('fluency_agent_2', String, callback_a2)
    # depening on the speaker initialise topics and generate data

    pub1 = rospy.Publisher('head_nod_agent_1', Float64, queue_size=10)

    pub2 = rospy.Publisher('head_nod_agent_2', Float64, queue_size=10)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

