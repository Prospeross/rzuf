#!/usr/bin/env python
import rospy
from std_msgs.msg import UInt16MultiArray

def main():
    rospy.init_node("servo_angle_publisher")

    # Odczyt parametrow z pliku launch
    servo1 = rospy.get_param("~servo1_angle", 90)
    servo2 = rospy.get_param("~servo2_angle", 55)

    # Publikowanie na topic servo angles
    pub = rospy.Publisher("/servo_angles", UInt16MultiArray, queue_size=10)

    rospy.loginfo(f"Publishing servo angles: servo1={servo1}, servo2={servo2}")

    msg = UInt16MultiArray()
    msg.data = [servo1, servo2]

    # Publikuj cyklicznie (mozliwosc rozszrzenie o dynamiczne rozgladanie sie)
    rate = rospy.Rate(1)  # 1 Hz
    while not rospy.is_shutdown():
        pub.publish(msg)
        rate.sleep()

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass