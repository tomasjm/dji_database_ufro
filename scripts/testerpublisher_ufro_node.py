import rospy
from sensor_msgs.msg import BatteryState
import random


def talker():
    pub = rospy.Publisher("test_topic_ufro", BatteryState, queue_size=10)
    rospy.init_node('publisher_ufro', anonymous=True)
    rate = rospy.Rate(1) # 10hz
    while not rospy.is_shutdown():
        battery = BatteryState()
        battery.voltage = random.random()*10
        rospy.loginfo(battery.voltage)
        pub.publish(battery)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass