---
sidebar_position: 5
title: ROS 2 Hands-On Exercises
---

# ROS 2 Hands-On Exercises

## Exercise 1: Node Creation and Communication

### Objective
Create a simple publisher and subscriber pair to understand the basics of ROS 2 communication.

### Tasks
1. Create a publisher node that publishes "Hello, Robot!" messages to a topic called `robot_greetings`
2. Create a subscriber node that listens to the `robot_greetings` topic and prints received messages
3. Launch both nodes and observe the communication
4. Modify the publisher to include a counter in the message

### Expected Outcome
- Understanding of basic node structure
- Knowledge of publisher/subscriber pattern
- Ability to create and run ROS 2 nodes

### Solution Steps
```bash
# Create a new package
ros2 pkg create --build-type ament_python robot_exercises
cd robot_exercises

# Create publisher node
mkdir -p robot_exercises/nodes
# (Add your publisher code to robot_exercises/nodes/greeting_publisher.py)

# Create subscriber node
# (Add your subscriber code to robot_exercises/nodes/greeting_subscriber.py)

# Update setup.py to include entry points for your nodes

# Build and run
colcon build --packages-select robot_exercises
source install/setup.bash

# Run the nodes
ros2 run robot_exercises greeting_publisher
# In another terminal
ros2 run robot_exercises greeting_subscriber
```

## Exercise 2: Parameter Management

### Objective
Learn how to use parameters in ROS 2 to configure node behavior at runtime.

### Tasks
1. Create a node that declares a parameter for controlling its behavior
2. Set the parameter value through a launch file
3. Change the parameter value at runtime using the command line
4. Observe how changing the parameter affects the node's behavior

### Expected Outcome
- Understanding of parameter declaration and usage
- Knowledge of launch file parameter configuration
- Ability to modify parameters at runtime

### Solution Steps
```python
# In your node file
def __init__(self):
    super().__init__('parameter_demo_node')
    self.declare_parameter('loop_rate', 1.0)  # Default value is 1.0
    self.rate = self.get_parameter('loop_rate').value

def update_rate(self):
    self.rate = self.get_parameter('loop_rate').value
```

```bash
# Run with parameter override
ros2 run robot_exercises parameter_demo --ros-args -p loop_rate:=2.0
```

## Exercise 3: Service Implementation

### Objective
Implement a service server and client to understand request/response communication.

### Tasks
1. Create a service definition file (srv file) for a simple calculator service
2. Implement a service server that performs basic arithmetic operations
3. Create a service client that sends requests to the server
4. Test the service communication

### Expected Outcome
- Understanding of service-based communication
- Ability to create custom service definitions
- Knowledge of service server and client implementation

### Solution Steps
```bash
# Create service definition in srv/AddTwoInts.srv
int64 a
int64 b
---
int64 sum
```

```python
# Service server implementation
from robot_exercises.srv import AddTwoInts

def add_two_ints_callback(self, request, response):
    response.sum = request.a + request.b
    self.get_logger().info(f'Returning {response.sum}')
    return response
```

## Exercise 4: Action Implementation

### Objective
Implement an action server and client for long-running tasks with feedback.

### Tasks
1. Create an action definition for a robot movement task
2. Implement an action server that simulates robot movement with feedback
3. Create an action client that sends goals and monitors progress
4. Handle preempting and cancellation of goals

### Expected Outcome
- Understanding of action-based communication
- Knowledge of feedback and goal management
- Ability to implement long-running task handlers

### Solution Steps
```bash
# Create action definition in action/MoveRobot.action
float64 target_x
float64 target_y
---
float64 final_x
float64 final_y
string result_message
---
float64 current_x
float64 current_y
float64 distance_remaining
```

## Exercise 5: URDF and TF Exploration

### Objective
Work with URDF files and transform trees to understand robot representation.

### Tasks
1. Load the humanoid robot URDF into RViz
2. Visualize the TF tree of the robot
3. Create a simple URDF for a custom robot
4. Add joint state publishers to animate the robot

### Expected Outcome
- Understanding of URDF structure
- Knowledge of TF tree visualization
- Ability to create and modify robot models

### Solution Steps
```bash
# Launch robot state publisher
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:='$(find robot_exercises)/urdf/my_robot.urdf'

# Visualize in RViz
ros2 run rviz2 rviz2

# View TF tree
ros2 run tf2_tools view_frames
```

## Exercise 6: Launch File Configuration

### Objective
Create complex launch files to manage multiple nodes and parameters.

### Tasks
1. Create a launch file that starts multiple nodes with different parameters
2. Use launch arguments to customize the launch configuration
3. Include other launch files in a hierarchical structure
4. Add conditional launching based on arguments

### Expected Outcome
- Understanding of launch file syntax and structure
- Ability to manage complex multi-node systems
- Knowledge of launch arguments and conditions

### Solution Steps
```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Declare launch arguments
    use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation clock if true'
    )

    # Create nodes
    talker_node = Node(
        package='demo_nodes_cpp',
        executable='talker',
        name='talker_node',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    return LaunchDescription([
        use_sim_time,
        talker_node
    ])
```

## Exercise 7: Debugging and Tools

### Objective
Use ROS 2 tools for debugging and monitoring system behavior.

### Tasks
1. Use `ros2 topic` commands to inspect topics and messages
2. Use `ros2 node` commands to inspect nodes and their connections
3. Use `ros2 service` commands to call services from command line
4. Use `rqt` for graphical monitoring and debugging

### Expected Outcome
- Proficiency with ROS 2 command-line tools
- Ability to debug communication issues
- Knowledge of monitoring techniques

### Solution Steps
```bash
# List all topics
ros2 topic list

# Echo messages on a topic
ros2 topic echo /topic_name std_msgs/msg/String

# Call a service
ros2 service call /service_name std_srvs/srv/SetBool '{data: true}'

# Monitor nodes
ros2 node info node_name

# Launch rqt
rqt
```

## Assessment Questions

### Basic Level
1. Explain the difference between topics, services, and actions in ROS 2.
2. What is the purpose of a launch file?
3. How do you declare and use parameters in a ROS 2 node?

### Intermediate Level
4. Describe the process of creating a custom message type in ROS 2.
5. What is the TF tree and why is it important in robotics?
6. How would you structure a launch file to start a robot with multiple sensors?

### Advanced Level
7. Design a system architecture for a mobile manipulator using appropriate communication patterns (topics, services, actions).
8. How would you implement a fault-tolerant system with multiple redundant nodes?
9. What considerations would you make when deploying a ROS 2 system on embedded hardware?