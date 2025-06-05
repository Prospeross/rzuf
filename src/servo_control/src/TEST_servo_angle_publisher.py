#!/usr/bin/env python

# Nod testowy do ustalanie potrzebnych kat dla odpowiedniego gimala 
# oraz dla odpowiedniego ustawienia

import rospy
from std_msgs.msg import UInt16MultiArray

class ServoCommandNode:
    def __init__(self):
        rospy.init_node("servo_command_sender")
        self.pub = rospy.Publisher("/servo_angles", UInt16MultiArray, queue_size=10)

        rospy.loginfo("Node servo_command_sender uruchomiony.")
        self.run()

    def run(self):
        rate = rospy.Rate(10)  # 10 Hz
        while not rospy.is_shutdown():
            try:
                angle1 = int(input("Wprowadz wartosc kata dla servo 1 (0-180): "))
                angle2 = int(input("Wprowadz wartosc kata dla servo 2 (0-180): "))
                
                if not (0 <= angle1 <= 180 and 0 <= angle2 <= 180):
                    rospy.logwarn("Podane katy musza byc w zakresie od 0 do 180.")
                    continue

                msg = UInt16MultiArray()
                msg.data = [angle1, angle2]
                self.pub.publish(msg)
                rospy.loginfo(f"Wyslane katy: {angle1}, {angle2}")

            except ValueError:
                rospy.logwarn("Nieprawidlowa wartosc. Wprowadz liczne calkowita (int).")
            except KeyboardInterrupt:
                rospy.loginfo("Przerwane przez uzytkownika.")
                break

if __name__ == "__main__":
    try:
        ServoCommandNode()
    except rospy.ROSInterruptException:
        pass
