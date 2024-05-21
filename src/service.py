import sys
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty

class KillRobotProcess(Node):
    def __init__(self):
        super().__init__('kill_robot_process')
        self.publisher = self.create_publisher(msg_type=Twist, topic="cmd_vel", qos_profile=10)
        self.twist = Twist()
        self.srv = self.create_service(Empty, 'kill_robot_process', self.kill_robot_process_callback)


    def kill_robot_process_callback(self, request, response):
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0
        self.publisher.publish(self.twist)
        self.get_logger().info('Turtlebot parando por meio da chamada do serviço...')
        rclpy.shutdown()
        return response


def main(args=None):
    rclpy.init(args=args)
    krp = KillRobotProcess()
    rclpy.spin(krp)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
