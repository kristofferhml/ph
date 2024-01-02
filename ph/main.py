import rclpy
import os
from datetime import datetime
from . import utils
from rclpy.node import Node
from std_msgs.msg import String

I2C_ADDRESS = int(os.getenv('I2C_ADDRESS',99))
READ_CMD = os.getenv('READ_CMD','R')

class Ph(Node):

    def __init__(self):
        super().__init__('ph')
        self.publisher_ = self.create_publisher(String, 'ph', 10)
        timer_period = 3 # seconds
        self.device = utils.get_device(I2C_ADDRESS)
        if (self.device):
            self.get_logger().info('Starting ph')
            self.timer = self.create_timer(timer_period, self.timer_callback)

        else:
            self.get_logger().info('Unable to start ph. No device found. Tried address "%d"' % I2C_ADDRESS)
       
    def timer_callback(self):
        reading = String()
        response = self.device.query(READ_CMD)
        if not response:
            self.get_logger().info('Lost device on address "%d"' % I2C_ADDRESS)
        
        else:
            reading.data = self.device.query(READ_CMD)
            self.publisher_.publish(reading)
            self.get_logger().info('Publishing: %s' % reading.data)
        
def main(args=None):
    rclpy.init(args=args)
    ph = Ph()
    rclpy.spin(ph)

    ph.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()