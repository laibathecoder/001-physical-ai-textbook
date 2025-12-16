from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    """Launch file for the complete humanoid robot system"""

    # Declare launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    # Path to the humanoid robot URDF
    urdf_path = PathJoinSubstitution([
        FindPackageShare('humanoid_robot_examples'),
        'urdf',
        'humanoid_model.urdf'
    ])

    # Robot state publisher node
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[
            {'use_sim_time': use_sim_time},
            {'robot_description': urdf_path}
        ],
        output='screen'
    )

    # Joint state publisher (for simulation)
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[
            {'use_sim_time': use_sim_time}
        ],
        output='screen'
    )

    # The main humanoid robot system node
    humanoid_system = Node(
        package='humanoid_robot_examples',
        executable='humanoid_robot_system',
        name='humanoid_robot_system',
        parameters=[
            {'use_sim_time': use_sim_time}
        ],
        output='screen',
        respawn=True
    )

    # Navigation system (Nav2)
    nav2_bringup_launch = PathJoinSubstitution([
        FindPackageShare('nav2_bringup'),
        'launch',
        'navigation_launch.py'
    ])

    # Isaac ROS perception nodes (simulated)
    isaac_perception = Node(
        package='isaac_ros_perceptor',
        executable='perception_node',
        name='perception_node',
        parameters=[
            {'use_sim_time': use_sim_time}
        ],
        output='screen'
    )

    # Voice command interface
    voice_interface = Node(
        package='voice_interface',
        executable='voice_command_node',
        name='voice_command_node',
        parameters=[
            {'use_sim_time': use_sim_time}
        ],
        output='screen'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'
        ),
        robot_state_publisher,
        joint_state_publisher,
        humanoid_system,
        isaac_perception,
        voice_interface,
        # Note: Nav2 launch would be included separately or via composition
    ])