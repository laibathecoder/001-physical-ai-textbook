---
sidebar_position: 3
title: URDF for Humanoid Robots
---

# URDF for Humanoid Robots

## Understanding URDF

Unified Robot Description Format (URDF) is an XML-based format used to describe robot models in ROS. For humanoid robots, URDF defines the physical structure, kinematic properties, and visual appearance of the robot. This description is essential for simulation, visualization, and control algorithms.

## URDF Structure for Humanoid Robots

### Basic Components

A humanoid robot URDF typically includes:

1. **Links**: Represent rigid parts of the robot (torso, head, arms, legs)
2. **Joints**: Define connections between links (revolute, prismatic, fixed)
3. **Materials**: Define visual properties (color, texture)
4. **Gazebo Plugins**: Define physics properties and simulation behavior

### Link Definition

Each link in a humanoid robot contains:
- **Inertial properties**: Mass, center of mass, and inertia matrix
- **Visual properties**: Mesh or geometric shape for visualization
- **Collision properties**: Shape for collision detection

```xml
<link name="torso">
  <inertial>
    <mass value="10.0"/>
    <origin xyz="0 0 0.2" rpy="0 0 0"/>
    <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.1" iyz="0" izz="0.1"/>
  </inertial>
  <visual>
    <origin xyz="0 0 0.2" rpy="0 0 0"/>
    <geometry>
      <mesh filename="package://humanoid_robot/meshes/torso.dae"/>
    </geometry>
    <material name="gray">
      <color rgba="0.5 0.5 0.5 1.0"/>
    </material>
  </visual>
  <collision>
    <origin xyz="0 0 0.2" rpy="0 0 0"/>
    <geometry>
      <box size="0.3 0.3 0.4"/>
    </geometry>
  </collision>
</link>
```

### Joint Definition

Joints connect links and define the degrees of freedom:

```xml
<joint name="torso_head_joint" type="revolute">
  <parent link="torso"/>
  <child link="head"/>
  <origin xyz="0 0 0.4" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="-1.57" upper="1.57" effort="100" velocity="1.0"/>
  <dynamics damping="0.1" friction="0.0"/>
</joint>
```

## Humanoid Robot Kinematic Structure

### Typical Humanoid Configuration

A standard humanoid robot includes:
- **Torso**: Central body with head attachment
- **Head**: With neck joint for gaze control
- **Arms**: Shoulders, elbows, wrists with multiple degrees of freedom
- **Legs**: Hips, knees, ankles for locomotion
- **Hands/Feet**: For manipulation and stable support

### Kinematic Chains

Humanoid robots typically have multiple kinematic chains:
- **Left Arm Chain**: Torso → Shoulder → Elbow → Wrist → Hand
- **Right Arm Chain**: Torso → Shoulder → Elbow → Wrist → Hand
- **Left Leg Chain**: Torso → Hip → Knee → Ankle → Foot
- **Right Leg Chain**: Torso → Hip → Knee → Ankle → Foot

## URDF Best Practices for Humanoids

### Naming Conventions

Use consistent naming patterns:
- Links: `base_link`, `torso`, `head`, `left_upper_arm`, `right_lower_leg`, etc.
- Joints: `torso_head_joint`, `left_shoulder_pitch`, `right_knee_joint`, etc.
- Consistent prefixes: `left_`, `right_` for bilateral symmetry

### Inertial Properties

Accurate inertial properties are crucial for realistic simulation:
- Use CAD software to calculate exact inertial properties
- Ensure center of mass is correctly positioned
- Use realistic mass values based on actual hardware

### Visual and Collision Separation

Separate visual and collision properties:
- Visual: Detailed meshes for rendering
- Collision: Simplified geometries for efficient collision detection

## Advanced URDF Features for Humanoids

### Transmission Elements

Define how joints are controlled:

```xml
<transmission name="left_shoulder_pitch_trans">
  <type>transmission_interface/SimpleTransmission</type>
  <joint name="left_shoulder_pitch">
    <hardwareInterface>hardware_interface/EffortJointInterface</hardwareInterface>
  </joint>
  <actuator name="left_shoulder_pitch_motor">
    <hardwareInterface>hardware_interface/EffortJointInterface</hardwareInterface>
    <mechanicalReduction>1</mechanicalReduction>
  </actuator>
</transmission>
```

### Gazebo Integration

Include Gazebo-specific properties:

```xml
<gazebo reference="left_foot">
  <mu1>0.8</mu1>
  <mu2>0.8</mu2>
  <kp>1000000.0</kp>
  <kd>100.0</kd>
  <material>Gazebo/Grey</material>
</gazebo>
```

### Xacro for Complex Humanoids

For complex humanoid robots, use Xacro (XML Macros) to simplify the URDF:

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="humanoid_robot">

  <xacro:property name="M_PI" value="3.14159"/>

  <xacro:macro name="simple_arm" params="prefix reflect">
    <link name="${prefix}_upper_arm">
      <!-- arm link definition -->
    </link>
    <joint name="${prefix}_shoulder_joint" type="revolute">
      <!-- joint definition -->
    </joint>
  </xacro:macro>

  <xacro:simple_arm prefix="left" reflect="1"/>
  <xacro:simple_arm prefix="right" reflect="-1"/>

</robot>
```

## Simulation Considerations

### Physics Parameters

For stable simulation of humanoid robots:
- Set appropriate damping and friction values
- Use realistic joint limits
- Ensure proper mass distribution

### Control Integration

URDF works with ROS 2 control frameworks:
- Joint state publisher for sensor feedback
- Joint trajectory controllers for motion execution
- Effort or position controllers for actuator interfaces

## Validation and Debugging

### URDF Validation

Use ROS 2 tools to validate your URDF:
- `check_urdf`: Validate URDF syntax and structure
- `urdf_to_graphiz`: Generate visual representation of kinematic tree
- `rviz2`: Visualize the robot model

### Common Issues

- **Kinematic loops**: Avoid closed kinematic chains without proper constraints
- **Inertial properties**: Ensure CoM and inertia values are realistic
- **Joint limits**: Set appropriate limits based on hardware capabilities

## References

1. Chitta, S., Marder-Eppstein, E., & Prats, M. (2012). *ROS Industrial: Advanced capabilities for robot manipulation*. IEEE-RAS International Conference on Humanoid Robots, 525-530.

2. Siciliano, B., & Khatib, O. (Eds.). (2016). *Springer handbook of robotics* (2nd ed.). Springer. Chapter 4: Robot Modeling and Control.

3. ROS 2 Documentation. (2023). *URDF Tutorials*. Retrieved from https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/URDF-Main.html

4. Murai, R., & Ude, A. (2018). A framework for learning from demonstration with an application to humanoid robots. *IEEE-RAS 18th International Conference on Humanoid Robots (Humanoids)*, 1-9.

5. Featherstone, R. (2008). *Rigid body dynamics algorithms*. Springer Science & Business Media.

6. Kuffner, J. (2004). Automatically configuring collision-avoidance groups for humanoid robot simulation and control. *IEEE International Conference on Robotics and Automation*, 2382-2387.

7. Nakanishi, J., Cory, R., Mistry, M., Peters, J., & Schaal, S. (2008). Operational space control: A theoretical and empirical comparison. *International Journal of Robotics Research*, 27(6), 737-757.

8. Tedrake, R. (2022). *Underactuated Robotics: Algorithms for Walking, Running, Swimming, Flying, and Manipulation*. MIT Press.