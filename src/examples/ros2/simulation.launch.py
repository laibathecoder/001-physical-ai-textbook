from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import os


def generate_launch_description():
    # Declare launch arguments
    use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )

    world_name = DeclareLaunchArgument(
        'world_name',
        default_value='small_room',
        description='Choose one of the world files from `/gazebo_ros_pkgs/gazebo_worlds`'
    )

    robot_name = DeclareLaunchArgument(
        'robot_name',
        default_value='humanoid_robot',
        description='Name of the robot to spawn in Gazebo'
    )

    # Get Gazebo launch file from gazebo_ros package
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            ])
        ]),
        launch_arguments={
            'world': PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'worlds',
                LaunchConfiguration('world_name')
            ]),
            'verbose': 'false',
        }.items()
    )

    # Robot State Publisher node
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'robot_description': get_robot_description()
        }]
    )

    # Spawn entity node to load robot into Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', LaunchConfiguration('robot_name'),
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.5'
        ],
        output='screen'
    )

    # Joint State Publisher node (for simulation)
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'rate': 50  # Hz
        }],
        output='screen'
    )

    # Example sensor processing node
    sensor_processor = Node(
        package='simulation_examples',
        executable='sensor_processor',
        name='sensor_processor',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time')
        }],
        output='screen'
    )

    # Example controller node
    controller_node = Node(
        package='simulation_examples',
        executable='motion_controller',
        name='motion_controller',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'control_freq': 50.0
        }],
        output='screen'
    )

    return LaunchDescription([
        use_sim_time,
        world_name,
        robot_name,
        gazebo,
        robot_state_publisher,
        joint_state_publisher,
        spawn_entity,
        sensor_processor,
        controller_node
    ])


def get_robot_description():
    """
    Helper function to get robot description from URDF file.
    In a real implementation, this would read from the actual URDF file.
    """
    # This is a placeholder - in practice, you would read the actual URDF file
    urdf_content = '''
<?xml version="1.0"?>
<robot name="simple_humanoid">
  <link name="base_link">
    <inertial>
      <mass value="5.0"/>
      <origin xyz="0 0 0.2" rpy="0 0 0"/>
      <inertia ixx="0.1" ixy="0" ixz="0" iyy="0.1" iyz="0" izz="0.1"/>
    </inertial>
    <visual>
      <origin xyz="0 0 0.2" rpy="0 0 0"/>
      <geometry>
        <box size="0.3 0.3 0.4"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 0.8"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 0.2" rpy="0 0 0"/>
      <geometry>
        <box size="0.3 0.3 0.4"/>
      </geometry>
    </collision>
  </link>

  <link name="head">
    <inertial>
      <mass value="1.0"/>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.001"/>
    </inertial>
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
      <material name="white">
        <color rgba="1 1 1 0.8"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
    </collision>
  </link>

  <joint name="base_head_joint" type="fixed">
    <parent link="base_link"/>
    <child link="head"/>
    <origin xyz="0 0 0.4" rpy="0 0 0"/>
  </joint>
</robot>'''
    return urdf_content