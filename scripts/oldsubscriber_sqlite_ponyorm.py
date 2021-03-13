import rospy
from std_msgs.msg import String
from sensor_msgs.msg import BatteryState
from pony.orm import *
from datetime import datetime
import random
db = Database()

# Declaración de tablas y entidades de la base de datos
class Data(db.Entity):
    id = PrimaryKey(int, auto=True)
    battery_voltage = Required(float)
    created_at = Required(datetime,default=datetime.utcnow)

# Declaración de funciones que se comunicarán con la base de datos
@db_session
def create_data(battery_voltage=12.3457):
    v1 = Data(battery_voltage=battery_voltage)
    commit()

# Función que inicializa la conexión con la base de datos
def init_db():
    db.bind(provider='sqlite', filename='database.db', create_db=True)
    db.generate_mapping(create_tables=True)
    set_sql_debug(True)
    try:
        setup_ros_loop()
    except rospy.ROSInterruptException:
        print("Error de ros")
        pass


# Ros callback
def callback(data: BatteryState):
    rospy.loginfo(rospy.get_caller_id() + "Voltaje en batería: %s", str(data.voltage))
    #create_data(battery_voltage=data.voltage)

def callback_fast(data: BatteryState):
    rospy.loginfo(rospy.get_caller_id() + "Voltaje en batería_fast: %s", str(data.voltage))

# Función que se encarga del código de ROS
def setup_ros_loop():
    rospy.Subscriber("test_topic_ufro", BatteryState, callback)
    rospy.Subscriber("test_topic_fast_ufro", BatteryState, callback_fast)
    rospy.init_node('database_ufro', anonymous=True)
    rospy.loginfo("Antes del spin")
    rospy.spin()
    rospy.loginfo("Después del spin")



if __name__ == "__main__":
    init_db()