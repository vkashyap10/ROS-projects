#!/usr/bin/env python

# This node gets id, object size, human expression and action from human_info_topic and object_info_topic topics. It then randomly selects from these variables and publishes to another topic.

import rospy
from std_msgs.msg import String
import numpy as np

# import messages to be used
from cr_week8_test.msg import object_info, human_info, perceived_info
from message_filters import ApproximateTimeSynchronizer, Subscriber
import numpy as np

def gotinfo(o_sub, h_sub):
    # check if ids from both topics match and proceed
    if(o_sub.id == h_sub.id):
        # randomly put values to 0
        filter_ = np.random.randint(low=1,high=9)

        # variables for perceived_info
        id_ = o_sub.id
        object_size = o_sub.object_size
        ha = h_sub.human_action
        he = h_sub.human_expression

        if(filter_==1):
            object_size = 0
        if(filter_==2):
            ha =0
        if(filter_==3):
            he = 0
        if(filter_==4):
            object_size =0
            ha = 0
        if(filter_==5):
            object_size=0
            he = 0
        if(filter_==6):
            ha = 0
            he = 0
        if(filter_==7):
            object_size =0
            ha = 0
            he = 0

        # initialise message object and assign generated values
        perceived_info_var = perceived_info()
        perceived_info_var.id = id_
        perceived_info_var.object_size = object_size
        perceived_info_var.human_expression = he
        perceived_info_var.human_action = ha
        rospy.loginfo(perceived_info_var)
        # publish
        pub.publish(perceived_info_var)

def listener():
    
    # initialise node and subscribe to topics
    rospy.init_node('perception_filter', anonymous=True)
    o_sub = Subscriber("object_info_topic", object_info)
    h_sub = Subscriber("human_info_topic", human_info)
    
    # ApproximateTimeSynchronizers synchronizes incoming channels by the timestamps, and outputs them in the form of a single callback that takes the same number of channels
    ats = ApproximateTimeSynchronizer([o_sub, h_sub], queue_size=10, slop=1,allow_headerless=True)
    ats.registerCallback(gotinfo)

    rospy.spin()

if __name__ == '__main__':

    # initialise publisher 
    pub = rospy.Publisher('perceived_info_topic', perceived_info, queue_size=10)

    listener()
