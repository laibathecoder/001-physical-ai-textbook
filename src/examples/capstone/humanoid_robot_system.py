#!/usr/bin/env python3
"""
Humanoid Robot System Integration - Capstone Project Implementation

This module integrates all concepts from the Physical AI & Humanoid Robotics textbook
into a comprehensive autonomous humanoid robot system that can operate in complex environments.

The system combines:
- Physical AI and embodied intelligence principles
- ROS 2 communication and control systems
- Digital twin simulation and sensor integration
- NVIDIA Isaac AI systems for perception and navigation
- Vision-Language-Action (VLA) capabilities for natural interaction
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

from std_msgs.msg import String, Float32
from sensor_msgs.msg import Image, LaserScan, Imu, JointState
from geometry_msgs.msg import PoseStamped, Twist, Point
from nav_msgs.msg import Odometry
from tf2_ros import TransformListener, Buffer

import numpy as np
from typing import List, Dict, Tuple, Optional
import math
import time
from dataclasses import dataclass
from enum import Enum

# Import Isaac ROS components (these would be available in a real Isaac setup)
try:
    from isaac_ros_perception_msgs.msg import Detection2DArray, Detection3DArray
    from vision_msgs.msg import Detection2D
    ISAAC_AVAILABLE = True
except ImportError:
    ISAAC_AVAILABLE = False
    print("Isaac ROS components not available, using simulated perception")


@dataclass
class RobotState:
    """Represents the current state of the humanoid robot"""
    position: Point
    orientation: Tuple[float, float, float, float]  # quaternion
    joint_positions: List[float]
    joint_velocities: List[float]
    joint_efforts: List[float]
    com_position: Point  # Center of mass
    com_velocity: Point
    balance_state: float  # Stability measure (0.0-1.0)
    battery_level: float
    current_task: str
    task_status: str


class HumanoidTask(Enum):
    """Enumeration of possible humanoid tasks"""
    IDLE = "idle"
    NAVIGATE = "navigate"
    GRASP = "grasp"
    MANIPULATE = "manipulate"
    INTERACT = "interact"
    CHARGING = "charging"


class PhysicalAIController:
    """
    Implements Physical AI and embodied intelligence principles
    """

    def __init__(self):
        self.gravity = 9.81  # m/s^2
        self.mass = 60.0  # kg, approximate humanoid mass
        self.com_height = 0.8  # m, approximate center of mass height
        self.stability_threshold = 0.1  # m, acceptable CoM deviation

    def calculate_balance_metrics(self, joint_positions: List[float],
                                 joint_velocities: List[float]) -> Dict[str, float]:
        """
        Calculate balance metrics based on current joint configuration
        Implements physical principles for maintaining humanoid balance
        """
        # Simplified balance calculation - in reality, this would use
        # forward kinematics to compute center of mass and ZMP (Zero Moment Point)

        # Calculate approximate CoM position based on joint angles
        # This is a simplified model - real implementation would use full kinematics
        com_x = 0.0
        com_y = 0.0
        com_z = self.com_height

        # Add influence of joint positions on CoM
        for i, (pos, vel) in enumerate(zip(joint_positions, joint_velocities)):
            # Simplified influence model - each joint affects CoM based on position
            influence_factor = 0.01 * (i % 10)  # Simplified model
            com_x += math.sin(pos) * influence_factor
            com_y += math.cos(pos) * influence_factor

        # Calculate stability based on CoM position relative to support polygon
        # (feet positions in this simplified model)
        stability = max(0.0, min(1.0, 1.0 - abs(com_x) - abs(com_y)))

        return {
            'com_x': com_x,
            'com_y': com_y,
            'com_z': com_z,
            'stability': stability,
            'zmp_x': com_x,  # Simplified ZMP calculation
            'zmp_y': com_y   # Simplified ZMP calculation
        }

    def apply_physical_constraints(self, target_positions: List[float],
                                  current_positions: List[float]) -> List[float]:
        """
        Apply physical constraints to ensure movements are physically plausible
        """
        constrained_positions = []

        for target, current in zip(target_positions, current_positions):
            # Limit maximum joint velocity based on physical constraints
            max_velocity = 2.0  # rad/s, simplified constraint
            velocity = target - current
            clamped_velocity = max(-max_velocity, min(max_velocity, velocity))
            constrained_pos = current + clamped_velocity

            # Apply joint limits (simplified)
            joint_limit = math.pi  # rad, simplified limit
            clamped_pos = max(-joint_limit, min(joint_limit, constrained_pos))

            constrained_positions.append(clamped_pos)

        return constrained_positions


class PerceptionSystem:
    """
    Implements perception system integrating multiple sensor modalities
    """

    def __init__(self):
        self.object_detections = []
        self.spatial_map = {}  # Environment representation
        self.last_detection_time = time.time()

    def process_camera_data(self, image_msg: Image) -> List[Dict]:
        """
        Process camera data for object detection and scene understanding
        """
        # Simulate object detection
        # In a real system, this would use Isaac ROS perception nodes
        detected_objects = []

        # Simulate detection of common objects
        for i in range(3):
            obj = {
                'id': f'object_{i}',
                'type': np.random.choice(['cup', 'box', 'ball', 'chair']),
                'position': Point(
                    x=np.random.uniform(0.5, 2.0),
                    y=np.random.uniform(-1.0, 1.0),
                    z=0.0
                ),
                'confidence': np.random.uniform(0.7, 0.95),
                'bbox': [0, 0, 100, 100]  # bounding box
            }
            detected_objects.append(obj)

        self.object_detections = detected_objects
        self.last_detection_time = time.time()

        return detected_objects

    def process_lidar_data(self, scan_msg: LaserScan) -> Dict:
        """
        Process LIDAR data for environment mapping and obstacle detection
        """
        # Simplified LIDAR processing
        obstacles = []
        min_distance = float('inf')

        for i, range_val in enumerate(scan_msg.ranges):
            if not math.isnan(range_val) and range_val < 2.0:  # 2m threshold
                angle = scan_msg.angle_min + i * scan_msg.angle_increment
                x = range_val * math.cos(angle)
                y = range_val * math.sin(angle)

                obstacles.append({
                    'x': x,
                    'y': y,
                    'distance': range_val
                })

                if range_val < min_distance:
                    min_distance = range_val

        return {
            'obstacles': obstacles,
            'min_distance': min_distance,
            'free_space': min_distance > 0.5  # 50cm clearance
        }

    def integrate_sensor_data(self) -> Dict:
        """
        Integrate data from multiple sensors for comprehensive scene understanding
        """
        # This would integrate camera, LIDAR, IMU, and other sensor data
        # in a real implementation
        integrated_data = {
            'objects': self.object_detections,
            'obstacles': [],
            'free_space_map': {},
            'spatial_relationships': {},
            'confidence_map': {}
        }

        return integrated_data


class NavigationSystem:
    """
    Implements humanoid-specific navigation with balance constraints
    """

    def __init__(self):
        self.path = []
        self.current_waypoint = 0
        self.global_plan = []
        self.local_plan = []
        self.footstep_plan = []

    def plan_path(self, start_pose: Point, goal_pose: Point,
                  environment_map: Dict) -> List[Point]:
        """
        Plan a path from start to goal considering humanoid-specific constraints
        """
        # Simplified path planning - in reality, this would use sophisticated
        # algorithms considering balance, step constraints, and environment
        path = [start_pose]

        # Create a simple path to goal
        steps = 10
        for i in range(1, steps + 1):
            t = i / steps
            x = start_pose.x + (goal_pose.x - start_pose.x) * t
            y = start_pose.y + (goal_pose.y - start_pose.y) * t
            z = start_pose.z + (goal_pose.z - start_pose.z) * t

            path.append(Point(x=x, y=y, z=z))

        return path

    def plan_footsteps(self, path: List[Point], start_state: RobotState) -> List[Dict]:
        """
        Plan footstep sequence for humanoid locomotion
        """
        footsteps = []

        # Simplified footstep planning
        # In reality, this would consider balance, step length limits, and gait patterns
        for i, pose in enumerate(path):
            if i % 2 == 0:  # Alternate between left and right foot
                footstep = {
                    'position': pose,
                    'foot_type': 'left' if i % 4 == 0 else 'right',
                    'step_time': i * 0.5,  # 0.5s per step
                    'swing_height': 0.05  # 5cm lift
                }
                footsteps.append(footstep)

        return footsteps

    def execute_navigation(self, goal_pose: Point, robot_state: RobotState) -> bool:
        """
        Execute navigation to goal pose while maintaining balance
        """
        # Plan path considering current robot state
        path = self.plan_path(robot_state.position, goal_pose, {})
        self.footstep_plan = self.plan_footsteps(path, robot_state)

        # Execute footstep plan
        for footstep in self.footstep_plan:
            success = self.execute_single_step(footstep, robot_state)
            if not success:
                return False

        return True

    def execute_single_step(self, footstep: Dict, robot_state: RobotState) -> bool:
        """
        Execute a single footstep while maintaining balance
        """
        # Simplified step execution
        # In reality, this would involve complex whole-body control
        # and balance feedback

        # Calculate required joint movements for step
        target_joints = self.calculate_step_joints(footstep, robot_state)

        # Apply physical constraints
        physical_ai = PhysicalAIController()
        constrained_joints = physical_ai.apply_physical_constraints(
            target_joints, robot_state.joint_positions
        )

        # Update robot state (simulated)
        robot_state.joint_positions = constrained_joints

        # Check balance after step
        balance_metrics = physical_ai.calculate_balance_metrics(
            robot_state.joint_positions,
            robot_state.joint_velocities
        )

        if balance_metrics['stability'] < 0.3:  # Unstable
            return False

        return True

    def calculate_step_joints(self, footstep: Dict, robot_state: RobotState) -> List[float]:
        """
        Calculate required joint positions for executing a footstep
        """
        # Simplified joint calculation
        # In reality, this would use inverse kinematics and whole-body control
        current_joints = robot_state.joint_positions
        target_joints = [pos + 0.1 for pos in current_joints]  # Simplified

        return target_joints


class ManipulationSystem:
    """
    Implements humanoid manipulation with grasp planning and execution
    """

    def __init__(self):
        self.current_grasp = None
        self.manipulation_plans = []

    def plan_grasp(self, object_info: Dict, robot_state: RobotState) -> Optional[Dict]:
        """
        Plan a grasp for the target object considering humanoid constraints
        """
        # Analyze object properties and robot state to generate grasp candidates
        object_pose = object_info['position']

        # Generate potential grasp poses around the object
        grasp_candidates = []

        for angle in np.linspace(0, 2*np.pi, 8):  # 8 different approach angles
            grasp_pose = {
                'position': Point(
                    x=object_pose.x + 0.1 * math.cos(angle),  # 10cm from object
                    y=object_pose.y + 0.1 * math.sin(angle),
                    z=object_pose.z + 0.1  # 10cm above object
                ),
                'orientation': self.calculate_approach_orientation(angle),
                'grasp_type': 'power' if object_info['type'] == 'box' else 'precision',
                'quality_score': np.random.uniform(0.6, 0.95)
            }
            grasp_candidates.append(grasp_pose)

        # Select best grasp based on quality and kinematic feasibility
        best_grasp = max(grasp_candidates, key=lambda g: g['quality_score'])

        # Verify kinematic feasibility
        if self.is_kinematic_feasible(best_grasp, robot_state):
            return best_grasp
        else:
            # Try alternative grasps
            for grasp in grasp_candidates:
                if self.is_kinematic_feasible(grasp, robot_state):
                    return grasp

        return None  # No feasible grasp found

    def is_kinematic_feasible(self, grasp_pose: Dict, robot_state: RobotState) -> bool:
        """
        Check if a grasp pose is kinematically feasible for the robot
        """
        # Simplified kinematic feasibility check
        # In reality, this would solve inverse kinematics

        # Check if position is within reachable workspace
        distance = math.sqrt(
            (grasp_pose['position'].x - robot_state.position.x)**2 +
            (grasp_pose['position'].y - robot_state.position.y)**2 +
            (grasp_pose['position'].z - robot_state.position.z)**2
        )

        return distance < 1.0  # 1m reachability limit

    def calculate_approach_orientation(self, angle: float) -> Tuple[float, float, float, float]:
        """
        Calculate approach orientation for grasping
        """
        # Simplified orientation calculation
        # In reality, this would consider object shape and grasp type
        w = math.cos(angle/2)
        x = 0.0
        y = 0.0
        z = math.sin(angle/2)

        return (w, x, y, z)

    def execute_grasp(self, grasp_pose: Dict, robot_state: RobotState) -> bool:
        """
        Execute grasp action while maintaining balance
        """
        # Move to pre-grasp position
        pre_grasp = Point(
            x=grasp_pose['position'].x + 0.05,  # 5cm above grasp
            y=grasp_pose['position'].y,
            z=grasp_pose['position'].z + 0.05
        )

        if not self.move_to_position(pre_grasp, robot_state):
            return False

        # Execute approach to grasp position
        if not self.move_to_position(grasp_pose['position'], robot_state):
            return False

        # Close gripper (simulated)
        robot_state.current_task = "grasping"

        # Verify grasp success
        return self.verify_grasp_success(robot_state)

    def move_to_position(self, target_position: Point, robot_state: RobotState) -> bool:
        """
        Move end effector to target position
        """
        # Simplified movement
        # In reality, this would use inverse kinematics and trajectory planning
        robot_state.position = target_position
        return True

    def verify_grasp_success(self, robot_state: RobotState) -> bool:
        """
        Verify that grasp was successful
        """
        # Simplified verification
        # In reality, this would use force/torque sensors and visual feedback
        return np.random.random() > 0.2  # 80% success rate


class VoiceCommandProcessor:
    """
    Implements voice command processing using simulated Whisper integration
    """

    def __init__(self):
        self.command_keywords = {
            'navigate': ['go to', 'move to', 'navigate to', 'walk to'],
            'grasp': ['pick up', 'grasp', 'take', 'get'],
            'manipulate': ['move', 'place', 'put', 'set'],
            'interact': ['hello', 'hi', 'talk', 'speak', 'listen'],
            'stop': ['stop', 'halt', 'pause', 'wait']
        }

    def process_voice_command(self, command_text: str) -> Tuple[HumanoidTask, Dict]:
        """
        Process natural language command and convert to robot action
        """
        command_text = command_text.lower()

        # Identify task type
        for task, keywords in self.command_keywords.items():
            for keyword in keywords:
                if keyword in command_text:
                    task_enum = HumanoidTask(task)
                    params = self.extract_parameters(command_text, task_enum)
                    return task_enum, params

        # If no specific task identified, assume interaction
        return HumanoidTask.INTERACT, {'text': command_text}

    def extract_parameters(self, command: str, task: HumanoidTask) -> Dict:
        """
        Extract parameters from voice command
        """
        params = {}

        if task == HumanoidTask.NAVIGATE:
            # Extract location information
            if 'kitchen' in command:
                params['location'] = Point(x=2.0, y=1.0, z=0.0)
            elif 'living room' in command:
                params['location'] = Point(x=0.0, y=0.0, z=0.0)
            elif 'bedroom' in command:
                params['location'] = Point(x=-1.0, y=2.0, z=0.0)
            else:
                # Extract coordinates if mentioned
                params['location'] = Point(x=1.0, y=1.0, z=0.0)  # default

        elif task == HumanoidTask.GRASP:
            # Extract object information
            if 'cup' in command:
                params['object_type'] = 'cup'
            elif 'box' in command:
                params['object_type'] = 'box'
            elif 'ball' in command:
                params['object_type'] = 'ball'
            else:
                params['object_type'] = 'object'  # generic

        elif task == HumanoidTask.INTERACT:
            params['text'] = command

        return params


class HumanoidRobotSystem(Node):
    """
    Main humanoid robot system node that integrates all subsystems
    """

    def __init__(self):
        super().__init__('humanoid_robot_system')

        # Initialize subsystems
        self.physical_ai_controller = PhysicalAIController()
        self.perception_system = PerceptionSystem()
        self.navigation_system = NavigationSystem()
        self.manipulation_system = ManipulationSystem()
        self.voice_processor = VoiceCommandProcessor()

        # Initialize robot state
        self.robot_state = RobotState(
            position=Point(x=0.0, y=0.0, z=0.0),
            orientation=(1.0, 0.0, 0.0, 0.0),
            joint_positions=[0.0] * 28,  # 28 DOF humanoid
            joint_velocities=[0.0] * 28,
            joint_efforts=[0.0] * 28,
            com_position=Point(x=0.0, y=0.0, z=0.8),
            com_velocity=Point(x=0.0, y=0.0, z=0.0),
            balance_state=1.0,
            battery_level=1.0,
            current_task=HumanoidTask.IDLE.value,
            task_status='ready'
        )

        # Initialize ROS 2 interfaces
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # Publishers
        self.cmd_vel_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.joint_cmd_publisher = self.create_publisher(JointState, '/joint_commands', 10)
        self.voice_response_publisher = self.create_publisher(String, '/voice_response', 10)

        # Subscribers
        self.joint_state_subscriber = self.create_subscription(
            JointState, '/joint_states', self.joint_state_callback, 10)
        self.imu_subscriber = self.create_subscription(
            Imu, '/imu/data', self.imu_callback, 10)
        self.odom_subscriber = self.create_subscription(
            Odometry, '/odom', self.odom_callback, 10)
        self.camera_subscriber = self.create_subscription(
            Image, '/camera/rgb/image_raw', self.camera_callback, qos_profile)
        self.lidar_subscriber = self.create_subscription(
            LaserScan, '/scan', self.lidar_callback, qos_profile)
        self.voice_command_subscriber = self.create_subscription(
            String, '/voice_command', self.voice_command_callback, 10)

        # TF listener for coordinate transformations
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Timer for main control loop
        self.control_timer = self.create_timer(0.1, self.control_loop)  # 10Hz

        self.get_logger().info('Humanoid Robot System initialized')

    def joint_state_callback(self, msg: JointState):
        """Update joint state from robot feedback"""
        self.robot_state.joint_positions = list(msg.position)
        if msg.velocity:
            self.robot_state.joint_velocities = list(msg.velocity)
        if msg.effort:
            self.robot_state.joint_efforts = list(msg.effort)

    def imu_callback(self, msg: Imu):
        """Update balance state from IMU data"""
        # Calculate balance metrics from IMU data
        balance_metrics = self.physical_ai_controller.calculate_balance_metrics(
            self.robot_state.joint_positions,
            self.robot_state.joint_velocities
        )
        self.robot_state.balance_state = balance_metrics['stability']

    def odom_callback(self, msg: Odometry):
        """Update position from odometry"""
        self.robot_state.position = msg.pose.pose.position
        self.robot_state.orientation = (
            msg.pose.pose.orientation.w,
            msg.pose.pose.orientation.x,
            msg.pose.pose.orientation.y,
            msg.pose.pose.orientation.z
        )

    def camera_callback(self, msg: Image):
        """Process camera data"""
        objects = self.perception_system.process_camera_data(msg)
        self.get_logger().debug(f'Detected {len(objects)} objects')

    def lidar_callback(self, msg: LaserScan):
        """Process LIDAR data"""
        lidar_data = self.perception_system.process_lidar_data(msg)
        self.get_logger().debug(f'Detected {len(lidar_data["obstacles"])} obstacles')

    def voice_command_callback(self, msg: String):
        """Process voice command"""
        self.get_logger().info(f'Received voice command: {msg.data}')

        # Process the command
        task, params = self.voice_processor.process_voice_command(msg.data)
        self.robot_state.current_task = task.value

        # Execute the task
        success = self.execute_task(task, params)

        # Respond to user
        response = f"Executed {task.value} task: {'Success' if success else 'Failed'}"
        response_msg = String()
        response_msg.data = response
        self.voice_response_publisher.publish(response_msg)

    def execute_task(self, task: HumanoidTask, params: Dict) -> bool:
        """Execute the specified task with given parameters"""
        self.get_logger().info(f'Executing task: {task.value} with params: {params}')

        try:
            if task == HumanoidTask.NAVIGATE:
                return self.execute_navigation_task(params)
            elif task == HumanoidTask.GRASP:
                return self.execute_grasp_task(params)
            elif task == HumanoidTask.MANIPULATE:
                return self.execute_manipulation_task(params)
            elif task == HumanoidTask.INTERACT:
                return self.execute_interaction_task(params)
            elif task == HumanoidTask.IDLE:
                return self.execute_idle_task()
            else:
                self.get_logger().warn(f'Unknown task: {task}')
                return False
        except Exception as e:
            self.get_logger().error(f'Error executing task {task}: {e}')
            return False

    def execute_navigation_task(self, params: Dict) -> bool:
        """Execute navigation task"""
        if 'location' in params:
            goal_pose = params['location']
            success = self.navigation_system.execute_navigation(goal_pose, self.robot_state)
            return success
        else:
            self.get_logger().warn('No location specified for navigation task')
            return False

    def execute_grasp_task(self, params: Dict) -> bool:
        """Execute grasp task"""
        # For this example, we'll use the closest detected object
        objects = self.perception_system.object_detections
        if not objects:
            self.get_logger().warn('No objects detected for grasping')
            return False

        # Find the closest object of the requested type
        target_object = None
        if 'object_type' in params:
            for obj in objects:
                if obj['type'] == params['object_type']:
                    target_object = obj
                    break

        if not target_object:
            # Just take the first detected object
            target_object = objects[0]

        # Plan and execute grasp
        grasp_plan = self.manipulation_system.plan_grasp(target_object, self.robot_state)
        if grasp_plan:
            success = self.manipulation_system.execute_grasp(grasp_plan, self.robot_state)
            return success
        else:
            self.get_logger().warn('Could not plan grasp for object')
            return False

    def execute_manipulation_task(self, params: Dict) -> bool:
        """Execute manipulation task"""
        # Simplified manipulation task
        self.get_logger().info('Executing manipulation task')
        return True

    def execute_interaction_task(self, params: Dict) -> bool:
        """Execute interaction task"""
        self.get_logger().info(f'Interacting with: {params.get("text", "unknown")}')
        return True

    def execute_idle_task(self) -> bool:
        """Execute idle task"""
        self.get_logger().info('Robot is idling')
        return True

    def control_loop(self):
        """Main control loop that runs at 10Hz"""
        # Update robot state
        self.update_robot_state()

        # Check safety conditions
        if not self.check_safety_conditions():
            self.emergency_stop()
            return

        # Monitor battery level
        self.robot_state.battery_level -= 0.001  # Simulate battery drain

        # If battery is low, go to charging station
        if self.robot_state.battery_level < 0.2 and self.robot_state.current_task != HumanoidTask.CHARGING.value:
            self.robot_state.current_task = HumanoidTask.CHARGING.value
            # Navigate to charging station (simplified)
            charging_station = Point(x=-2.0, y=0.0, z=0.0)
            self.navigation_system.execute_navigation(charging_station, self.robot_state)

    def update_robot_state(self):
        """Update robot state based on physical AI principles"""
        # Calculate balance metrics
        balance_metrics = self.physical_ai_controller.calculate_balance_metrics(
            self.robot_state.joint_positions,
            self.robot_state.joint_velocities
        )
        self.robot_state.balance_state = balance_metrics['stability']

        # Update COM position (simplified)
        self.robot_state.com_position.x = balance_metrics['com_x']
        self.robot_state.com_position.y = balance_metrics['com_y']
        self.robot_state.com_position.z = balance_metrics['com_z']

    def check_safety_conditions(self) -> bool:
        """Check if robot is in safe operating conditions"""
        # Check balance
        if self.robot_state.balance_state < 0.1:  # Too unstable
            self.get_logger().warn('Robot balance below safety threshold')
            return False

        # Check joint limits
        for pos in self.robot_state.joint_positions:
            if abs(pos) > math.pi * 2:  # Check for extreme joint angles
                self.get_logger().warn('Joint limit exceeded')
                return False

        return True

    def emergency_stop(self):
        """Execute emergency stop procedures"""
        self.get_logger().error('Emergency stop activated!')

        # Publish zero velocity
        stop_cmd = Twist()
        self.cmd_vel_publisher.publish(stop_cmd)

        # Update task status
        self.robot_state.current_task = HumanoidTask.IDLE.value
        self.robot_state.task_status = 'emergency_stop'


def main(args=None):
    """Main function to run the humanoid robot system"""
    rclpy.init(args=args)

    # Create and run the humanoid robot system
    robot_system = HumanoidRobotSystem()

    try:
        rclpy.spin(robot_system)
    except KeyboardInterrupt:
        robot_system.get_logger().info('Shutting down Humanoid Robot System...')
    finally:
        robot_system.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()