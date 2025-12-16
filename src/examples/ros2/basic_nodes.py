#!/usr/bin/env python3

"""
Basic ROS 2 Node Example

This example demonstrates the fundamental concepts of ROS 2 nodes,
publishers, subscribers, and basic messaging patterns.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
import sys
import time


class HelloWorldPublisher(Node):
    """
    A simple publisher node that publishes "Hello World" messages
    with a counter to demonstrate basic publishing functionality.
    """

    def __init__(self):
        super().__init__('hello_world_publisher')

        # Create a publisher for String messages on the 'hello_world' topic
        self.publisher = self.create_publisher(String, 'hello_world', 10)

        # Timer to publish messages every 0.5 seconds
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.counter = 0

        self.get_logger().info('Hello World Publisher Node initialized')

    def timer_callback(self):
        """Callback function that publishes messages periodically"""
        msg = String()
        msg.data = f'Hello World: {self.counter}'
        self.publisher.publish(msg)
        self.get_logger().info(f'Published: "{msg.data}"')
        self.counter += 1


class VelocityPublisher(Node):
    """
    A publisher node that publishes velocity commands to control a robot.
    Demonstrates publishing geometry_msgs/Twist messages.
    """

    def __init__(self):
        super().__init__('velocity_publisher')

        # Create a publisher for Twist messages on the 'cmd_vel' topic
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)

        # Timer to publish velocity commands every 0.1 seconds
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.get_logger().info('Velocity Publisher Node initialized')

    def timer_callback(self):
        """Publish velocity commands to move the robot in a square pattern"""
        msg = Twist()

        # Set linear velocity (m/s) - forward motion
        msg.linear.x = 0.2  # Move forward at 0.2 m/s

        # Set angular velocity (rad/s) - turning motion
        msg.angular.z = 0.0  # No turning initially

        self.publisher.publish(msg)
        self.get_logger().info(f'Velocity command - Linear: {msg.linear.x}, Angular: {msg.angular.z}')


class MessageSubscriber(Node):
    """
    A subscriber node that listens to messages from other nodes.
    Demonstrates basic subscription functionality.
    """

    def __init__(self):
        super().__init__('message_subscriber')

        # Create a subscriber for String messages on the 'hello_world' topic
        self.subscription = self.create_subscription(
            String,
            'hello_world',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.get_logger().info('Message Subscriber Node initialized')

    def listener_callback(self, msg):
        """Callback function that processes received messages"""
        self.get_logger().info(f'Received: "{msg.data}"')


class VelocitySubscriber(Node):
    """
    A subscriber node that listens to velocity commands.
    Demonstrates subscription to geometry_msgs/Twist messages.
    """

    def __init__(self):
        super().__init__('velocity_subscriber')

        # Create a subscriber for Twist messages on the 'cmd_vel' topic
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.velocity_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.get_logger().info('Velocity Subscriber Node initialized')

    def velocity_callback(self, msg):
        """Process received velocity commands"""
        self.get_logger().info(f'Received velocity command - Linear: {msg.linear.x}, Angular: {msg.angular.z}')


def main(args=None):
    """
    Main function to demonstrate different node types
    """
    rclpy.init(args=args)

    # Parse command line arguments to determine which node to run
    node_type = "all"  # default
    if len(sys.argv) > 1:
        node_type = sys.argv[1].lower()

    nodes = []

    if node_type in ["publisher", "all"]:
        hello_publisher = HelloWorldPublisher()
        vel_publisher = VelocityPublisher()
        nodes.extend([hello_publisher, vel_publisher])

    if node_type in ["subscriber", "all"]:
        message_subscriber = MessageSubscriber()
        vel_subscriber = VelocitySubscriber()
        nodes.extend([message_subscriber, vel_subscriber])

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