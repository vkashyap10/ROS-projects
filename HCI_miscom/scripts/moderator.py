#!/usr/bin/env python

# this node generates speaker tag which lasts between 20 seconds
import rospy
from std_msgs.msg import String
import numpy as np
from std_msgs.msg import Int32


def generate_data():

    # initialise the two publishers
    pub = rospy.Publisher('speaker', String, queue_size=10)

    # intialise the ros node. This registers it with ros master
    rospy.init_node('moderator', anonymous=False)
    # set rate to publish every 10 seconds
    rate = rospy.Rate(0.1) # 0.05hz

    while not rospy.is_shutdown():
        # generate random object size, human expression, human action
        speaker_r = np.random.randint(low=1,high=3)
       	speaker_var = String()

	if(speaker_r == 1):
		speaker_var.data = "Agent 1"
	else:
		speaker_var.data = "Agent 2"

        rospy.loginfo(speaker_var)
	pub.publish(speaker_var)

        rate.sleep()

if __name__ == '__main__':
    try:
        # this function will generate random data for speaker and fluency
        generate_data()
    except rospy.ROSInterruptException:
        pass
