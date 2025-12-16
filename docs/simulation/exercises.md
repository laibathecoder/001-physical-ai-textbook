---
sidebar_position: 4
title: Simulation Exercises - Verify Student Understanding
---

# Simulation Exercises - Verify Student Understanding

## Exercise 1: Gazebo Environment Setup

### Objective
Set up a basic Gazebo simulation environment with a simple robot model.

### Tasks
1. Install Gazebo and verify the installation
2. Launch Gazebo with a default world (empty.world)
3. Spawn a simple robot model (e.g., PR2 or TurtleBot)
4. Control the robot using Gazebo's GUI controls
5. Save the simulation state

### Expected Outcome
- Understanding of Gazebo's basic interface
- Ability to launch and control a simulated robot
- Knowledge of how to save and restore simulation states

### Solution Steps
```bash
# Launch Gazebo with default world
gazebo

# Launch Gazebo with specific world
gazebo worlds/empty.world

# Spawn a model
ros2 run gazebo_ros spawn_entity.py -file model.sdf -entity my_robot

# Check available models
ls /usr/share/gazebo-*/models
```

### Assessment Questions
1. What is the purpose of the physics engine in Gazebo?
2. How does Gazebo handle collision detection between objects?
3. What are the main differences between ODE, Bullet, and DART physics engines?

## Exercise 2: Robot Model Integration

### Objective
Integrate a custom robot model into Gazebo simulation.

### Tasks
1. Create a simple URDF model of a wheeled robot
2. Add Gazebo-specific tags to the URDF for simulation
3. Load the robot into Gazebo using robot_state_publisher
4. Verify that the robot appears correctly in the simulation
5. Test joint movement and visualization

### Expected Outcome
- Understanding of URDF-Gazebo integration
- Knowledge of Gazebo-specific URDF tags
- Ability to visualize and control custom robots in simulation

### Solution Steps
```xml
<!-- Add Gazebo tags to URDF -->
<gazebo reference="link_name">
  <material>Gazebo/Blue</material>
  <mu1>0.2</mu1>
  <mu2>0.2</mu2>
</gazebo>

<!-- Add transmission for joint control -->
<transmission name="tran1">
  <type>transmission_interface/SimpleTransmission</type>
  <joint name="joint1">
    <hardwareInterface>hardware_interface/EffortJointInterface</hardwareInterface>
  </joint>
  <actuator name="motor1">
    <hardwareInterface>hardware_interface/EffortJointInterface</hardwareInterface>
    <mechanicalReduction>1</mechanicalReduction>
  </actuator>
</transmission>
```

```bash
# Launch robot in Gazebo
ros2 launch gazebo_ros spawn_entity.launch.py robot_namespace:=my_robot spawn_args:="-urdf -param robot_description -model my_robot"
```

### Assessment Questions
1. Explain the purpose of transmission tags in URDF for Gazebo simulation.
2. How do you specify different materials for robot links in Gazebo?
3. What is the role of the robot_state_publisher in Gazebo simulation?

## Exercise 3: Sensor Simulation

### Objective
Simulate various sensors on a robot model and process the sensor data.

### Tasks
1. Add a camera sensor to your robot model
2. Add a LIDAR sensor to your robot model
3. Launch the robot in Gazebo with sensors active
4. Subscribe to sensor topics and visualize data
5. Implement basic sensor processing (e.g., obstacle detection)

### Expected Outcome
- Understanding of sensor simulation in Gazebo
- Ability to configure and use different sensor types
- Knowledge of processing sensor data in ROS 2

### Solution Steps
```bash
# Check available sensor topics
ros2 topic list | grep sensor

# Echo sensor data
ros2 topic echo /camera/image_raw sensor_msgs/msg/Image
ros2 topic echo /laser_scan sensor_msgs/msg/LaserScan

# Visualize sensors in RViz
ros2 run rviz2 rviz2
```

### Assessment Questions
1. What are the main differences between 2D and 3D LIDAR simulation?
2. How does depth camera simulation differ from RGB camera simulation?
3. What noise models are typically used for sensor simulation?

## Exercise 4: Controller Integration

### Objective
Integrate controllers to make the simulated robot move realistically.

### Tasks
1. Set up joint state broadcaster for the robot
2. Configure a joint trajectory controller
3. Send commands to move the robot joints
4. Verify that the robot moves as expected in simulation
5. Test different control strategies (position, velocity, effort)

### Expected Outcome
- Understanding of robot control in simulation
- Ability to configure and use ROS 2 controllers
- Knowledge of different control interfaces

### Solution Steps
```bash
# Load and activate controllers
ros2 control load_controller --set-state active joint_state_broadcaster
ros2 control load_controller --set-state active joint_trajectory_controller

# Send trajectory commands
ros2 action send_goal /follow_joint_trajectory control_msgs/action/FollowJointTrajectory "{goal_tolerance: 0.01}"
```

### Assessment Questions
1. Explain the difference between position, velocity, and effort control.
2. What is the purpose of the joint_state_broadcaster?
3. How do you tune PID parameters for joint controllers?

## Exercise 5: Unity Environment Setup

### Objective
Set up a Unity environment for robot simulation and visualization.

### Tasks
1. Install Unity Hub and Unity Editor
2. Install the Unity Robotics package
3. Import the URDF Importer package
4. Create a new Unity scene with basic lighting
5. Import a robot model using the URDF Importer

### Expected Outcome
- Understanding of Unity's robotics capabilities
- Ability to set up Unity for robotics applications
- Knowledge of URDF import process

### Solution Steps
```csharp
// Example script to load a URDF in Unity
using Unity.Robotics.URDFImporter;

public class RobotLoader : MonoBehaviour
{
    void Start()
    {
        // Load robot from URDF file
        GameObject robot = URDFLoader.LoadURDF("Assets/urdfs/my_robot.urdf");
        robot.transform.SetParent(this.transform);
    }
}
```

### Assessment Questions
1. What are the advantages of using Unity over Gazebo for robotics simulation?
2. How does the URDF Importer convert ROS robot models to Unity format?
3. What is the role of the ROS TCP Connector in Unity robotics?

## Exercise 6: Unity-ROS Communication

### Objective
Establish communication between Unity and ROS 2 for integrated simulation.

### Tasks
1. Set up the ROS TCP Connector in Unity
2. Create a simple publisher in Unity to send data to ROS
3. Create a subscriber in Unity to receive data from ROS
4. Test bidirectional communication
5. Synchronize robot states between Unity and Gazebo

### Expected Outcome
- Understanding of Unity-ROS integration
- Ability to establish network communication
- Knowledge of message serialization between platforms

### Solution Steps
```csharp
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Std;

public class UnityRosBridge : MonoBehaviour
{
    ROSConnection ros;

    void Start()
    {
        ros = ROSConnection.instance;
    }

    void Update()
    {
        // Publish a string message
        ros.Publish("/unity_chatter", new StringMsg("Hello from Unity"));
    }

    // Callback function for receiving messages
    void OnMessageReceived(StringMsg msg)
    {
        Debug.Log("Received: " + msg.data);
    }
}
```

### Assessment Questions
1. Explain the communication architecture between Unity and ROS 2.
2. What are the latency considerations when using network-based communication?
3. How do you handle message serialization and deserialization between Unity and ROS?

## Exercise 7: Sensor Simulation in Unity

### Objective
Simulate sensors within the Unity environment and process sensor data.

### Tasks
1. Create a camera sensor in Unity
2. Implement raycasting for simple range sensing
3. Generate point cloud data from depth information
4. Publish sensor data to ROS topics
5. Process sensor data in ROS nodes

### Expected Outcome
- Understanding of sensor simulation in Unity
- Ability to create custom sensor simulators
- Knowledge of processing Unity-generated sensor data

### Solution Steps
```csharp
using UnityEngine;

public class UnityLidar : MonoBehaviour
{
    public float range = 10.0f;
    public int rays = 360;

    void Update()
    {
        float[] distances = new float[rays];

        for (int i = 0; i < rays; i++)
        {
            float angle = (float)i / rays * Mathf.PI * 2f;
            Vector3 direction = new Vector3(Mathf.Cos(angle), 0, Mathf.Sin(angle));

            if (Physics.Raycast(transform.position, direction, out RaycastHit hit, range))
            {
                distances[i] = hit.distance;
            }
            else
            {
                distances[i] = range; // Max range if no hit
            }
        }

        // Process distances array as needed
        ProcessLidarData(distances);
    }

    void ProcessLidarData(float[] distances)
    {
        // Convert to ROS message and publish
        // Implementation depends on specific requirements
    }
}
```

### Assessment Questions
1. How do Unity's physics raycasting capabilities compare to Gazebo's sensor simulation?
2. What are the advantages and disadvantages of simulating sensors in Unity versus Gazebo?
3. How can you ensure consistency between Unity and Gazebo sensor outputs?

## Exercise 8: Humanoid Robot Simulation

### Objective
Simulate a humanoid robot with realistic physics and control.

### Tasks
1. Create or import a humanoid robot model
2. Configure physics properties for realistic movement
3. Implement balance control algorithms
4. Test walking gaits in simulation
5. Validate stability and natural movement

### Expected Outcome
- Understanding of humanoid robot simulation challenges
- Ability to implement balance control
- Knowledge of gait generation and stability

### Solution Steps
```bash
# Launch humanoid robot in simulation
ros2 launch my_robot_bringup humanoid_simulation.launch.py

# Monitor joint states
ros2 topic echo /joint_states sensor_msgs/msg/JointState

# Send walking commands
ros2 action send_goal /walk_controller human_walking_msgs/action/Walk "{step_size: 0.3, step_height: 0.1}"
```

### Assessment Questions
1. What are the main challenges in simulating humanoid robots compared to wheeled robots?
2. How do you model and simulate the center of mass for humanoid balance?
3. What physics parameters are critical for realistic humanoid movement?

## Exercise 9: Multi-Robot Simulation

### Objective
Simulate multiple robots interacting in the same environment.

### Tasks
1. Spawn multiple robots in Gazebo
2. Implement robot-to-robot communication
3. Coordinate actions between robots
4. Handle collision avoidance
5. Demonstrate cooperative behavior

### Expected Outcome
- Understanding of multi-robot simulation
- Ability to coordinate multiple agents
- Knowledge of communication protocols

### Solution Steps
```bash
# Launch multiple robots with namespaces
ros2 launch multi_robot_demo multi_robot.launch.py

# Check topics for each robot
ros2 topic list | grep robot_1
ros2 topic list | grep robot_2

# Monitor robot positions
ros2 run tf2_tools view_frames
```

### Assessment Questions
1. How do you manage namespaces in multi-robot ROS systems?
2. What are the computational considerations for multi-robot simulation?
3. How do you implement communication and coordination between robots?

## Exercise 10: Simulation Validation

### Objective
Validate the simulation against real-world robot behavior.

### Tasks
1. Compare simulation and real robot behavior
2. Measure the sim-to-real gap
3. Identify key differences in dynamics
4. Propose improvements to simulation fidelity
5. Document validation results

### Expected Outcome
- Understanding of simulation validation methodologies
- Ability to quantify sim-to-real differences
- Knowledge of improving simulation accuracy

### Solution Steps
```bash
# Record data from both simulation and real robot
ros2 bag record /joint_states /odom /imu/data

# Analyze differences using custom tools
python3 analyze_differences.py simulation.bag real_robot.bag
```

### Assessment Questions
1. What metrics are most important for validating simulation accuracy?
2. How do you quantify the sim-to-real gap?
3. What are the main sources of discrepancy between simulation and reality?

## Advanced Assessment Questions

### Theoretical Understanding
1. Explain the physics simulation pipeline in Gazebo and how it affects robot behavior.
2. Compare and contrast different approaches to sensor simulation (analytical vs. raycasting vs. neural rendering).
3. Analyze the trade-offs between simulation accuracy and computational efficiency.

### Practical Application
4. Design a simulation environment for testing a specific humanoid robot task (e.g., object manipulation, navigation).
5. Create a sensor fusion system that combines data from multiple simulated sensors.
6. Implement a control system that works both in simulation and on a real robot.

### Problem-Solving
7. Troubleshoot a simulation where the robot behaves differently than expected.
8. Optimize a simulation to run in real-time while maintaining necessary accuracy.
9. Adapt a simulation pipeline to work with a new robot model that has different capabilities.