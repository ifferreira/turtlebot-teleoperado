import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Header, String
import cv2
import time

class WebcamPublisher(Node):
    def __init__(self):
        super().__init__('webcam_publisher')
        self.publisher_ = self.create_publisher(CompressedImage, '/video_frames', 10)
        self.latency_publisher_ = self.create_publisher(String, '/latency', 10)
        self.timer = self.create_timer(0.02, self.timer_callback)  # Publish every 0.1 seconds (10 Hz)
        self.cap = cv2.VideoCapture(0)

    def timer_callback(self):
        start_time = time.time()
        ret, frame = self.cap.read()
        if ret:
            # Encode frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            msg = CompressedImage()
            msg.format = "jpeg"
            msg.data = buffer.tobytes()
            msg.header = Header()
            msg.header.stamp = self.get_clock().now().to_msg()
            self.publisher_.publish(msg)
            end_time = time.time()
            latency = end_time - start_time
            latency_msg = String()
            latency_msg.data = f"{int(latency * 1000)} ms"
            self.latency_publisher_.publish(latency_msg)
            print(f"Latency: {int(latency * 1000)} ms")

def main(args=None):
    rclpy.init(args=args)
    webcam_publisher = WebcamPublisher()
    rclpy.spin(webcam_publisher)
    webcam_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
