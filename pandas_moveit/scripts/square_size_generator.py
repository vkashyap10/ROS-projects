#!/usr/bin/env python
# developed by: Vishal Kashyap

# this node generates random square size for the panda robot every 20 seconds
import rospy
import numpy as np
# import messages to be used
from std_msgs.msg import Float64

def generate_data():

    # initialise the publisher (this will publish the square size)
    pub1 = rospy.Publisher('square_size', Float64, queue_size=10)

    # intialise the ros node. This registers it with ros master
    rospy.init_node('square_size_generator', anonymous=True)
    # set rate to publish every 20 seconds
    rate = rospy.Rate(0.05) # 0.05hz

    while not rospy.is_shutdown():
        # generate random square size
        square_size = np.random.uniform(low=0.05,high=0.2)
        
        # publish square size on ros topic
        # initialise message object and assign generated values
        square_size_var = Float64()
        square_size_var.data = square_size
        rospy.loginfo(square_size_var)
	pub1.publish(square_size_var)

        rate.sleep()

if __name__ == '__main__':
    try:
        generate_data()
    except rospy.ROSInterruptException:
        pass
