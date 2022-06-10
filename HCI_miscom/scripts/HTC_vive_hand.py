#!/usr/bin/env python

# listen to fluency and generate data for hand velocity and height

import numpy as np
import rospy
# import messages to be used
from cr_final.msg import htc_hand_sensor
from std_msgs.msg import String

# callback will subsribe to 
def callback_a1(data):

    if data.data == 'fluent':
        # hand movement
        hand_height = 0.77 - 0.0010
        # gesture rate: low
        gesture_rate = list(np.random.normal(0.2, 0.1, 1))[0]
        
    else:
        # hand movement
        hand_height = 0.87 + 0.0139 + (0.0208 - 0.0010)
        # gesture rate: high
        gesture_rate = list(np.random.normal(0.45, 0.15, 1))[0]
    
    # initialise cubic_traj_coeffs  message object
    htc_hand_var = htc_hand_sensor()

    # initialise cubic_traj coeffs msg
    htc_hand_var.hand_height = hand_height
    htc_hand_var.gesture_rate = gesture_rate
    htc_hand_var.fluency = data.data
    
    # publish to topic
    rospy.loginfo(htc_hand_var)
    pub2.publish(htc_hand_var)

    print("published data to agent 2")

    return

# callback will subsribe to 
def callback_a2(data):
    mean_gesture_rate = 0.7
    sd = 3.0
    if data.data == 'fluent':
        # hand movement
        hand_height = 0.77 - 0.0010
        # gesture rate: low
        gesture_rate = mean_gesture_rate + list(np.random.normal(0.0, sd, 1))[0]
        
    else:
        # hand movement
        hand_height = 0.87 + 0.0139 + (0.0208 - 0.0010)*0.25
        # gesture rate: high
        gesture_rate = mean_gesture_rate + list(np.random.normal(sd, 2*sd, 1))[0]
    
    # initialise cubic_traj_coeffs  message object
    htc_hand_var = htc_hand_sensor()

    # initialise cubic_traj coeffs msg
    htc_hand_var.hand_height = hand_height
    htc_hand_var.gesture_rate = gesture_rate
    htc_hand_var.fluency = data.data
    
    # publish to topic
    rospy.loginfo(htc_hand_var)
    pub1.publish(htc_hand_var)

    print("published data to agent 1")

    return

if __name__ == '__main__':

    # initialise node
    rospy.init_node('HTC_vive_tracker', anonymous=False)

    # subscribe to agent 1 fluency tag
    rospy.Subscriber('fluency_agent_1', String, callback_a1)

    # subscribe to agent 2 fluency tag
    rospy.Subscriber('fluency_agent_2', String, callback_a2)
    # depening on the speaker initialise topics and generate data

    pub1 = rospy.Publisher('HTC_tracker_agent_1', htc_hand_sensor, queue_size=10)

    pub2 = rospy.Publisher('HTC_tracker_agent_2', htc_hand_sensor, queue_size=10)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

