#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16MultiArray
from geometry_msgs.msg import Twist

# Konfiguracja PWM z RC
PWM_NEUTRAL = 1500
PWM_RANGE = 250          # realny zakres wokol neutralnego 1500
DEADBAND_SPEED = 10      # martwa strefa dla jazdy
DEADBAND_STEER = 10      # martwa strefa dla skrotu

# Maksymalne wartosci predkosci robota
MAX_LINEAR = 1.0         # [m/s]
MAX_ANGULAR = 1.0        # [rad/s]

# Failsafe: zatrzymanie po X sekundach bez sygnalu
FAILSAFE_TIMEOUT = 3.0   # [s]

last_msg_time = None
received_once = False  # czy kiedykolwiek odebrano dane

def pwm_to_cmd(pwm, max_val, deadband):
    delta = pwm - PWM_NEUTRAL
    if abs(delta) < deadband:
        return 0.0
    return max(min(delta / float(PWM_RANGE), 1.0), -1.0) * max_val

def rc_callback(msg):
    global last_msg_time, received_once

    if len(msg.data) < 2:
        rospy.logwarn("Odebrano niepelne dane z /rc_channels: %s", msg.data)
        return

    speed_pwm = msg.data[0]
    steer_pwm = msg.data[1]

    twist = Twist()
    twist.linear.x = pwm_to_cmd(speed_pwm, MAX_LINEAR, DEADBAND_SPEED)
    twist.angular.z = pwm_to_cmd(steer_pwm, MAX_ANGULAR, DEADBAND_STEER)

    pub.publish(twist)
    last_msg_time = rospy.Time.now()
    received_once = True

def failsafe_timer(event):
    if not received_once or last_msg_time is None:
        return

    elapsed = (rospy.Time.now() - last_msg_time).to_sec()
    if elapsed > FAILSAFE_TIMEOUT:
        rospy.logwarn_throttle(5, "Failsafe aktywny: brak danych z RC przez %.1f s", elapsed)
        stop_msg = Twist()  # same zera
        pub.publish(stop_msg)

if __name__ == "__main__":
    rospy.init_node("rc_channels_to_cmd_vel")
    pub = rospy.Publisher("/hoverboard_velocity_controller/cmd_vel", Twist, queue_size=1)
    sub = rospy.Subscriber("/rc_channels", Int16MultiArray, rc_callback)

    # Co 0.1 s sprawdzamy, czy RC dziala
    rospy.Timer(rospy.Duration(0.1), failsafe_timer)

    rospy.loginfo("Node rc_channels_to_cmd_vel uruchomiony (z failsafe 3s)")
    rospy.spin()
