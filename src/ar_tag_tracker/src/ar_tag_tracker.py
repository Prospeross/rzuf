#!/usr/bin/env python

import rospy
from ar_track_alvar_msgs.msg import AlvarMarkers
from geometry_msgs.msg import Twist
from math import copysign

class ARFollower():
    def __init__(self):
        rospy.init_node("ar_follower")
                        
        # Ustawienie funkcji wylaczenia robota (zatrzymania)
        rospy.on_shutdown(self.shutdown)

        # Jaki marker ma byc podazany?
        self.MarkerID = rospy.get_param("~MarkerID", 0)
        
        # Jak czesto updatowac ruch robota?
        self.rate = rospy.get_param("~rate", 10)
        r = rospy.Rate(self.rate) 
        
        # Maksymalna predkosc skrecania [rad/s]
        self.max_angular_speed = rospy.get_param("~max_angular_speed", 1.5)
        
        # Minimalna predkosc skrecania [rad/s]
        self.min_angular_speed = rospy.get_param("~min_angular_speed", 0.2)
        
        # Maksymalny dystans znacznika zeby robota za nim podazal
        self.max_z = rospy.get_param("~max_z", 5.0)
        
        # Docelowa odleglosc miedzy robotami [w metrach]
        self.goal_z = rospy.get_param("~goal_z", 0.5)
        
        # Wartosc progu reakcji osi z (roznicy miedzy odlegloscia robotow) [w metrach]
        self.z_threshold = rospy.get_param("~z_threshold", 0.05)
        
        # Wartosc progu reakcja na przesuniecie znacznika na boki w osi x [w metrach]
        self.x_threshold = rospy.get_param("~x_threshold", 0.05)
        
        # Skalowanie wartosci odpowiedzi na zmiane (os z)
        self.z_scale = rospy.get_param("~z_scale", 0.5)

        # Skalowanie wartosci odpowiedzi na zmiane (os x)     
        self.x_scale = rospy.get_param("~x_scale", 1.0)
        
        # Maksymalna predkosc liniowa [m/s]
        self.max_linear_speed = rospy.get_param("~max_linear_speed", 1)
        
        # Minimalna predkosc liniowa [m/s]
        self.min_linear_speed = rospy.get_param("~min_linear_speed", 0.1)

        # Publikowanie na odpowiedni topic (zalezne od hoverboard_driver)
        self.cmd_vel_pub = rospy.Publisher('/hoverboard_velocity_controller/cmd_vel', Twist, queue_size=5)
        
        # Uruchomienie wiadomosci
        self.move_cmd = Twist()
        
        # Flaga, czy znacznik jest widziany
        self.target_visible = False

	    # Ostatnia znana predkosc
        self.last_speed = 0
        
        # Oczekiwanie na topic ar_pose_marker by wyslal dane
        rospy.loginfo("Oczekiwanie topic ar_pose_marker...")
        rospy.wait_for_message('ar_pose_marker', AlvarMarkers)
        
        # Subskrybcja do topicu ar_pose_marker 
        rospy.Subscriber('ar_pose_marker', AlvarMarkers, self.set_cmd_vel)
        
        rospy.loginfo("Poprawne uruchomienie wezlu. Zaczynam szukac markera...")
        
        # Petla publikacji na cmd_vel
        while not rospy.is_shutdown():
            # Wyslanie wiadomosci twist do cmd_vel
            self.cmd_vel_pub.publish(self.move_cmd)
            
            # Zaczekaj 1/self.rate [s]
            r.sleep()

    def set_cmd_vel(self, msg):
        # Szukamy markera o konkretnym ID
        marker = next((m for m in msg.markers if m.id == self.MarkerID), None)

        if marker is None:
            # Znacznik nie zostal znaleziony, robot powoli sie zatrzymuje
            self.move_cmd.linear.x /= 1.5
            self.move_cmd.angular.z /= 1.5

            if self.target_visible:
                rospy.loginfo("Zgubiono marker. Konczenie podazania")
            self.target_visible = False
            return

        # Znacznik zostal znaleziony
        if not self.target_visible:
            rospy.loginfo("Znaleziono marker. Rozpoczynanie podazania")
        self.target_visible = True
                
        # Uzyskanie przesuniecie w osi x znacznika wzgledem pozycji kamery [m]
        target_offset_x = marker.pose.pose.position.x
        
        # Uzyskanie odleglosci w osi z znacznika wzgledem pozycji kamery [m]
        target_offset_z = marker.pose.pose.position.z
        
        # Obrot robota tylko wtedy, gdy przemieszczenie celu przekroczy prog
        if abs(target_offset_x) > self.x_threshold:
            # Ustaw predkosc skrecania proporcjonalnie do przemieszczenia celu
            speed = target_offset_x * self.x_scale
            self.move_cmd.angular.z = copysign(max(self.min_angular_speed,
                                        min(self.max_angular_speed, abs(speed))), speed)
        else:
            self.move_cmd.angular.z = 0.0
 
        # Ustaw predkosc liniowa proporcjonalnie do przemieszczenia celu
        if abs(target_offset_z - self.goal_z) > self.z_threshold:
            speed = (target_offset_z - self.goal_z) * self.z_scale
            if speed < 0:
                speed *= 1.5

            self.move_cmd.linear.x = copysign(min(self.max_linear_speed, max(self.min_linear_speed, abs(speed))), speed)
            self.last_speed = self.move_cmd.linear.x
        else:
            self.move_cmd.linear.x = 0.0

    def shutdown(self):
        rospy.loginfo("Zatrzymywanie robota...")
        self.cmd_vel_pub.publish(Twist())
        rospy.sleep(1)     

if __name__ == '__main__':
    try:
        ARFollower()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("AR follower node zakonczony.")