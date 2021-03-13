import rospy
from std_msgs.msg import String
from sensor_msgs.msg import BatteryState
from pony.orm import *
from datetime import datetime, timezone
import random

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

username = '' # token=username:password
password = '' # token=username:password
bucket = 'testing' # database
organization = '-' # organization, as influxdb is inferior than 2, it is "-"

client = influxdb_client.InfluxDBClient(url='http://localhost:8086', token=f'{username}:{password}', org='-')

write_api = client.write_api(write_options=SYNCHRONOUS)


def callback(data: BatteryState):
    dt = datetime.now()
    utc_time = dt.replace(tzinfo = timezone.utc)
    utc_timestamp = utc_time.timestamp()
    rospy.loginfo(rospy.get_caller_id() + " Voltaje en batería: %s en la hora: %s", str(data.voltage), str(utc_timestamp))
    p = influxdb_client.Point("battery").field("voltage", data.voltage)
    write_api.write(bucket=bucket,record=p)

def callback_dht(data: String):
    rospy.loginfo(rospy.get_caller_id() + "Valor sensor DHT: %s", data)

# Función que se encarga del código de ROS
def setup_ros_loop():
    rospy.Subscriber("test_topic_ufro", BatteryState, callback)
    rospy.Subscriber("dht_sensor", String, callback_dht)
    rospy.init_node('ufro_database', anonymous=True)
    rospy.loginfo("Antes del spin")
    rospy.spin()
    rospy.loginfo("Después del spin")



if __name__ == "__main__":
    setup_ros_loop()
