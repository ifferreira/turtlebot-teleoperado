import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty
import sys, select, termios, tty

class TurtlebotTeleop(Node):
    def __init__(self):
        super().__init__('turtlebot_teleop')
        self.publisher = self.create_publisher(
            msg_type=Twist,
            topic="cmd_vel",
            qos_profile=10
        )

        self.twist = Twist()
        self.client = self.create_client(Empty, 'kill_robot_process')

    def send_request(self):
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Esperando serviço ficar disponível...')
        req = Empty.Request()
        future = self.client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            self.get_logger().info('Chamada de serviço bem-sucedida')
        else:
            self.get_logger().error('Chamada de serviço mal-sucedida')

    def move_turtlebot(self, linear_x, angular_z):
        self.twist.linear.x = linear_x
        self.twist.angular.z = angular_z
        self.publisher.publish(self.twist)
        print(f"Linear_x: {linear_x}, Angular_z: {angular_z}")

def getKey():     
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def main(args=None):
    rclpy.init(args=args)
    teleop = TurtlebotTeleop()
    print('''Para teleoperar o turtlebot, utilize as seguintes teclas:
            w: ir para frente
            s: ir para trás
            a: rotacionar sentido anti-horário
            d: rotacionar sentido horário

            q: parada de emergência
            e: chamar serviço para parar o robô e destruir o nó de teleoperação''')

    try:
        while True:
            key = getKey()
            match key:
                case 'w':
                    teleop.move_turtlebot(0.2, 0.0)
                case 'a':
                    teleop.move_turtlebot(0.0, 0.2)
                case 's':
                    teleop.move_turtlebot(-0.2, 0.0)
                case 'd':
                    teleop.move_turtlebot(0.0, -0.2)
                case 'q':
                    teleop.move_turtlebot(0.0, 0.0)
                case 'e':
                    teleop.send_request()
                case '\x03':
                    break

            #teleop.move_turtlebot(0.0, 0.0)
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)
    main()
