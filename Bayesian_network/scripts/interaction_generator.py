#!/usr/bin/env python

# this node generates object size, human action and human expression every 10 seconds
import rospy
from std_msgs.msg import String
import numpy as np
# import messages to be used
from cr_week8_test.msg import object_info, human_info

def generate_data():

    # initialise the two publishers
    pub1 = rospy.Publisher('object_info_topic', object_info, queue_size=10)
    pub2 = rospy.Publisher('human_info_topic',human_info,queue_size = 10)

    # intialise the ros node. This registers it with ros master
    rospy.init_node('interaction_generator', anonymous=True)
    # set rate to publish every 10 seconds
    rate = rospy.Rate(0.1) # 0.1hz

    # iteration id
    itr = 1
    while not rospy.is_shutdown():
        # generate random object size, human expression, human action
        object_size = np.random.randint(low=1,high=3)
        human_expression = np.random.randint(low=1,high=4)
        human_action = np.random.randint(low=1,high=4)
        
        # publish id and object size on ros topic object info
        # initialise message object and assign generated values
        object_info_var = object_info()
        object_info_var.id = itr
        object_info_var.object_size = object_size
        rospy.loginfo(object_info_var)
        
        
        # publish id, expression and action on ros topic human info
        # initialise message object and assign generated values
        human_info_var = human_info()
        human_info_var.id = itr
        human_info_var.human_expression = human_expression
        human_info_var.human_action = human_action
        rospy.loginfo(human_info_var)

	pub1.publish(object_info_var)
        pub2.publish(human_info_var)

        # update the iteration id
        itr = itr + 1
        rate.sleep()

if __name__ == '__main__':
    try:
        # this function will generate random data for object and human behavior and publish to 2 ros topics
        generate_data()
    except rospy.ROSInterruptException:
        pass
