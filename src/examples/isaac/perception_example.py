#!/usr/bin/env python3

"""
Isaac ROS Perception Example

This example demonstrates the use of Isaac ROS for perception tasks
including object detection, pose estimation, and scene understanding
for humanoid robotics applications.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo, PointCloud2
from geometry_msgs.msg import PoseStamped, TransformStamped
from vision_msgs.msg import Detection2DArray, ObjectHypothesisWithPose
from std_msgs.msg import Header
from tf2_ros import TransformBroadcaster
import cv2
from cv_bridge import CvBridge
import numpy as np
import tf_transformations
from scipy.spatial.transform import Rotation as R


class BoundingBox2D:
    """Simple bounding box representation"""
    def __init__(self):
        self.center = Point2D()
        self.size_x = 0.0
        self.size_y = 0.0


class Point2D:
    """Simple 2D point"""
    def __init__(self):
        self.x = 0.0
        self.y = 0.0


class Detection:
    """Simple detection representation"""
    def __init__(self):
        self.bbox = None
        self.class_name = ""
        self.confidence = 0.0


class IsaacPerceptionNode(Node):
    """
    A perception node demonstrating Isaac ROS capabilities for humanoid robots.
    This node processes camera data, performs object detection, and estimates poses.
    """

    def __init__(self):
        super().__init__('isaac_perception_node')

        # Initialize CV bridge for image conversion
        self.bridge = CvBridge()

        # Create subscribers for sensor data
        self.image_sub = self.create_subscription(
            Image,
            '/camera/rgb/image_rect_color',
            self.image_callback,
            10
        )

        self.depth_sub = self.create_subscription(
            Image,
            '/camera/depth/image_rect',
            self.depth_callback,
            10
        )

        self.camera_info_sub = self.create_subscription(
            CameraInfo,
            '/camera/rgb/camera_info',
            self.camera_info_callback,
            10
        )

        # Create publishers for perception results
        self.detection_pub = self.create_publisher(
            Detection2DArray,
            '/isaac_ros/detections',
            10
        )

        self.pose_pub = self.create_publisher(
            PoseStamped,
            '/isaac_ros/object_pose',
            10
        )

        # TF broadcaster for object poses
        self.tf_broadcaster = TransformBroadcaster(self)

        # Internal state
        self.camera_intrinsics = None
        self.latest_depth = None
        self.object_detector = ObjectDetector()

        self.get_logger().info('Isaac Perception Node initialized')

    def camera_info_callback(self, msg):
        """Store camera intrinsics for 3D reconstruction"""
        self.camera_intrinsics = np.array(msg.k).reshape(3, 3)

    def depth_callback(self, msg):
        """Store latest depth image for 3D pose estimation"""
        try:
            depth_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
            self.latest_depth = depth_image
        except Exception as e:
            self.get_logger().error(f'Error converting depth image: {e}')

    def image_callback(self, msg):
        """Process camera image and perform perception tasks"""
        try:
            # Convert ROS image to OpenCV
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # Perform object detection
            detections = self.object_detector.detect(cv_image)

            # Estimate 3D poses from 2D detections and depth
            detection_array = Detection2DArray()
            detection_array.header = msg.header

            for detection in detections:
                # Convert 2D bounding box to 3D pose
                pose_3d = self.estimate_3d_pose(detection, self.latest_depth)

                if pose_3d is not None:
                    # Create detection message
                    vision_detection = self.create_vision_detection(detection, pose_3d, msg.header)
                    detection_array.detections.append(vision_detection)

                    # Publish pose
                    pose_msg = PoseStamped()
                    pose_msg.header = msg.header
                    pose_msg.pose = pose_3d
                    self.pose_pub.publish(pose_msg)

                    # Broadcast transform
                    self.broadcast_transform(detection.class_name, pose_3d, msg.header)

            # Publish all detections
            self.detection_pub.publish(detection_array)

        except Exception as e:
            self.get_logger().error(f'Error in image callback: {e}')

    def estimate_3d_pose(self, detection, depth_image):
        """Estimate 3D pose from 2D detection and depth information"""
        if depth_image is None or self.camera_intrinsics is None:
            return None

        # Extract bounding box
        bbox = detection.bbox
        center_x = int(bbox.center.x)
        center_y = int(bbox.center.y)

        # Get depth at center of bounding box (average in region)
        roi_size = 10  # pixels around center
        y_start = max(0, center_y - roi_size)
        y_end = min(depth_image.shape[0], center_y + roi_size)
        x_start = max(0, center_x - roi_size)
        x_end = min(depth_image.shape[1], center_x + roi_size)

        depth_roi = depth_image[y_start:y_end, x_start:x_end]
        valid_depths = depth_roi[np.isfinite(depth_roi)]

        if len(valid_depths) == 0:
            return None

        avg_depth = np.mean(valid_depths)

        # Convert pixel coordinates to 3D using camera intrinsics
        fx = self.camera_intrinsics[0, 0]
        fy = self.camera_intrinsics[1, 1]
        cx = self.camera_intrinsics[0, 2]
        cy = self.camera_intrinsics[1, 2]

        x_3d = (center_x - cx) * avg_depth / fx
        y_3d = (center_y - cy) * avg_depth / fy
        z_3d = avg_depth

        # Create pose with estimated position
        pose = PoseStamped()
        pose.position.x = x_3d
        pose.position.y = y_3d
        pose.position.z = z_3d

        # For simplicity, assume object is upright
        pose.orientation.w = 1.0
        pose.orientation.x = 0.0
        pose.orientation.y = 0.0
        pose.orientation.z = 0.0

        return pose

    def create_vision_detection(self, detection, pose_3d, header):
        """Create vision_msgs/Detection2D message from detection and pose"""
        vision_detection = Detection2D()
        vision_detection.header = header
        vision_detection.bbox = detection.bbox

        # Add hypothesis with pose
        hypothesis = ObjectHypothesisWithPose()
        hypothesis.hypothesis.class_id = detection.class_name
        hypothesis.hypothesis.score = detection.confidence
        hypothesis.pose = pose_3d

        vision_detection.results.append(hypothesis)
        return vision_detection

    def broadcast_transform(self, object_name, pose_3d, header):
        """Broadcast object transform for TF tree"""
        t = TransformStamped()

        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = header.frame_id
        t.child_frame_id = f'{object_name}_frame'

        t.transform.translation.x = pose_3d.position.x
        t.transform.translation.y = pose_3d.position.y
        t.transform.translation.z = pose_3d.position.z

        t.transform.rotation = pose_3d.orientation

        self.tf_broadcaster.sendTransform(t)


class ObjectDetector:
    """
    Simple object detector for demonstration purposes.
    In practice, this would use Isaac ROS detection nodes or
    GPU-accelerated networks via TensorRT.
    """

    def __init__(self):
        # In a real implementation, this would load a pre-trained model
        # For this example, we'll simulate detections
        self.classes = ['person', 'chair', 'table', 'cup', 'robot']
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

    def detect(self, image):
        """Detect objects in the image (simulated for this example)"""
        height, width = image.shape[:2]
        detections = []

        # Simulate detections with reasonable probabilities
        # In real Isaac ROS, this would use DetectNet or other GPU-accelerated detectors
        for i in range(np.random.randint(1, 4)):  # 1-3 random detections
            class_idx = np.random.randint(0, len(self.classes))
            class_name = self.classes[class_idx]

            # Random bounding box
            x = np.random.randint(0, width // 3)
            y = np.random.randint(0, height // 3)
            w = np.random.randint(width // 4, width // 2)
            h = np.random.randint(height // 4, height // 2)

            # Ensure bounds
            x = min(x, width - 1)
            y = min(y, height - 1)
            w = min(w, width - x)
            h = min(h, height - y)

            # Create bounding box
            bbox = BoundingBox2D()
            bbox.center.x = x + w / 2
            bbox.center.y = y + h / 2
            bbox.size_x = w
            bbox.size_y = h

            # Detection object
            detection = Detection()
            detection.bbox = bbox
            detection.class_name = class_name
            detection.confidence = np.random.uniform(0.6, 0.95)

            detections.append(detection)

        return detections


def main(args=None):
    """Main function to run the Isaac perception node"""
    rclpy.init(args=args)

    perception_node = IsaacPerceptionNode()

    try:
        rclpy.spin(perception_node)
    except KeyboardInterrupt:
        print("Shutting down Isaac Perception Node...")
    finally:
        perception_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()