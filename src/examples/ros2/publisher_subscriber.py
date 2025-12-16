#!/usr/bin/env python3

"""
Publisher-Subscriber Example for ROS 2

This example demonstrates the publisher-subscriber pattern in ROS 2,
showing how nodes can communicate through topics using the publish-subscribe mechanism.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Point
import random
import time


class TemperaturePublisher(Node):
    """
    A publisher that simulates temperature sensor readings.
    This node publishes temperature data that other nodes can subscribe to.
    """

    def __init__(self):
        super().__init__('temperature_publisher')

        # Create a publisher for temperature readings
        self.publisher = self.create_publisher(String, 'temperature_data', 10)

        # Create a timer to publish data periodically
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.publish_temperature)

        self.temperature_range = (18.0, 25.0)  # Temperature range in Celsius
        self.get_logger().info('Temperature Publisher initialized')

    def publish_temperature(self):
        """Publish simulated temperature data"""
        # Generate random temperature within range
        temp = round(random.uniform(*self.temperature_range), 2)

        msg = String()
        msg.data = f'Temperature: {temp}°C at {self.get_clock().now().seconds_nanoseconds()}'

        self.publisher.publish(msg)
        self.get_logger().info(f'Published temperature: {msg.data}')


class DistancePublisher(Node):
    """
    A publisher that simulates distance sensor readings (like LIDAR).
    This demonstrates publishing more complex sensor data.
    """

    def __init__(self):
        super().__init__('distance_publisher')

        # Create a publisher for distance readings
        self.publisher = self.create_publisher(LaserScan, 'scan', 10)

        # Create a timer to publish data periodically
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.publish_scan)

        self.angle_min = -1.57  # -90 degrees in radians
        self.angle_max = 1.57   # 90 degrees in radians
        self.angle_increment = 0.017  # ~1 degree
        self.scan_ranges = []

        # Initialize scan ranges with random distances
        num_scans = int((self.angle_max - self.angle_min) / self.angle_increment)
        self.scan_ranges = [round(random.uniform(0.1, 10.0), 2) for _ in range(num_scans)]

        self.get_logger().info('Distance Publisher initialized')

    def publish_scan(self):
        """Publish simulated laser scan data"""
        msg = LaserScan()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'laser_frame'

        msg.angle_min = self.angle_min
        msg.angle_max = self.angle_max
        msg.angle_increment = self.angle_increment
        msg.time_increment = 0.0
        msg.scan_time = 0.1
        msg.range_min = 0.05
        msg.range_max = 10.0

        # Add some random variation to the ranges
        for i in range(len(self.scan_ranges)):
            variation = random.uniform(-0.05, 0.05)
            self.scan_ranges[i] = max(0.05, min(10.0, self.scan_ranges[i] + variation))

        msg.ranges = self.scan_ranges[:]
        msg.intensities = []  # No intensity data for simplicity

        self.publisher.publish(msg)
        self.get_logger().info(f'Published scan with {len(msg.ranges)} ranges')


class DataSubscriber(Node):
    """
    A subscriber that receives and processes data from publishers.
    This node subscribes to multiple topics to demonstrate multi-topic subscription.
    """

    def __init__(self):
        super().__init__('data_subscriber')

        # Create subscriptions to different topics
        self.temp_subscription = self.create_subscription(
            String,
            'temperature_data',
            self.temp_callback,
            10)
        self.temp_subscription  # prevent unused variable warning

        self.scan_subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10)
        self.scan_subscription  # prevent unused variable warning

        self.get_logger().info('Data Subscriber initialized')

    def temp_callback(self, msg):
        """Process temperature data"""
        self.get_logger().info(f'Received temperature data: {msg.data}')

    def scan_callback(self, msg):
        """Process scan data"""
        if len(msg.ranges) > 0:
            avg_distance = sum(r for r in msg.ranges if not float('inf') > r > 0) / len(msg.ranges)
            self.get_logger().info(f'Received scan data: {len(msg.ranges)} readings, avg distance: {avg_distance:.2f}m')


class CoordinatorNode(Node):
    """
    A coordinator node that demonstrates how a node can both publish and subscribe.
    This node coordinates between different data streams.
    """

    def __init__(self):
        super().__init__('coordinator_node')

        # Subscriptions
        self.temp_subscription = self.create_subscription(
            String,
            'temperature_data',
            self.temp_callback,
            10)
        self.temp_subscription  # prevent unused variable warning

        # Publisher for coordinated actions
        self.action_publisher = self.create_publisher(String, 'action_commands', 10)

        # Timer for periodic coordination
        self.timer = self.create_timer(2.0, self.coordinate_actions)

        self.last_temp = None
        self.get_logger().info('Coordinator Node initialized')

    def temp_callback(self, msg):
        """Process temperature data and store for coordination"""
        # Extract temperature value from message
        try:
            temp_str = msg.data.split(':')[1].split('°')[0].strip()
            self.last_temp = float(temp_str)
            self.get_logger().info(f'Coordinator stored temperature: {self.last_temp}°C')
        except (ValueError, IndexError):
            self.get_logger().warn(f'Could not parse temperature from: {msg.data}')

    def coordinate_actions(self):
        """Make decisions based on available data"""
        if self.last_temp is not None:
            if self.last_temp > 23.0:
                action_msg = String()
                action_msg.data = 'Action: Activate cooling system'
                self.action_publisher.publish(action_msg)
                self.get_logger().info(f'Published action: {action_msg.data}')
            elif self.last_temp < 20.0:
                action_msg = String()
                action_msg.data = 'Action: Activate heating system'
                self.action_publisher.publish(action_msg)
                self.get_logger().info(f'Published action: {action_msg.data}')
            else:
                self.get_logger().info('Temperature in acceptable range, no action needed')


def main(args=None):
    """
    Main function to demonstrate publisher-subscriber patterns
    """
    rclpy.init(args=args)

    # Create nodes
    temp_publisher = TemperaturePublisher()
    dist_publisher = DistancePublisher()
    subscriber = DataSubscriber()
    coordinator = CoordinatorNode()

    # Collect all nodes
    nodes = [temp_publisher, dist_publisher, subscriber, coordinator]

    try:
        # Spin all nodes simultaneously
        rclpy.spin_multi_threaded(nodes)
    except KeyboardInterrupt:
        print("\nShutting down nodes...")
    finally:
        # Clean shutdown
        for node in nodes:
            node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()