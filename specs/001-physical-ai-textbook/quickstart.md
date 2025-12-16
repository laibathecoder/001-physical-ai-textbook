# Quickstart Guide: Physical AI & Humanoid Robotics Textbook

## Overview
This guide provides a rapid introduction to the Physical AI & Humanoid Robotics textbook project, helping you get started with the content, tools, and examples.

## Prerequisites
Before starting with this textbook, ensure you have:
- Basic programming experience (Python preferred)
- Understanding of linear algebra and calculus
- Familiarity with Linux command line
- Computer with sufficient resources for robotics simulation (8GB+ RAM, dedicated GPU recommended)

## Environment Setup

### 1. Install ROS 2 Humble Hawksbill
```bash
# Follow the official ROS 2 installation guide for your OS
# Ubuntu/Debian:
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update
sudo apt install ros-humble-desktop
sudo apt install python3-rosdep2
source /opt/ros/humble/setup.bash
```

### 2. Install Gazebo Garden
```bash
# Follow the Gazebo installation guide
# Ubuntu/Debian:
sudo apt install gz-garden
```

### 3. Set up NVIDIA Isaac Sim (Optional but Recommended)
- Download Isaac Sim from NVIDIA Developer website
- Follow installation instructions for your platform
- Ensure CUDA-compatible GPU is available

### 4. Install Docusaurus for Documentation
```bash
npm init docusaurus@latest website classic
cd website
npm install
```

## Getting Started with the Textbook

### 1. Start with Chapter 1: Foundations of Physical AI
Begin with the foundational concepts to understand why AI must understand physics and the difference between digital AI and embodied AI. This chapter establishes the theoretical basis for all subsequent content.

### 2. Progress Through the Modules
Follow the recommended sequence:
1. Physical AI & Embodied Intelligence
2. ROS 2 - The Robotic Nervous System
3. Digital Twin (Gazebo & Unity)
4. NVIDIA Isaac Systems
5. Vision-Language-Action (VLA)
6. Capstone Project

### 3. Execute Code Examples
Each chapter includes practical examples in the `src/examples/` directory. Run them in the recommended order:
```bash
# Example for ROS 2 nodes:
cd src/examples/ros2
python3 basic_nodes.py
```

### 4. Run Simulations
Use the provided simulation environments to test concepts:
```bash
# Launch Gazebo simulation
ros2 launch examples_gazebo simulation.launch.py
```

## Key Concepts to Master

### Physical AI Fundamentals
- Understanding the relationship between physics and AI
- Environmental grounding and sensor integration
- Embodied cognition principles

### ROS 2 Architecture
- Nodes, topics, services, and actions
- URDF for robot modeling
- Launch files and parameter systems

### Simulation and Digital Twins
- Physics-based simulation principles
- Sensor simulation (LiDAR, RGB-D, IMUs)
- Environment modeling

### AI Integration with Isaac
- Isaac Sim for photorealistic simulation
- Isaac ROS for perception and navigation
- Nav2 for path planning

## Working with Code Examples

### File Structure
```
src/examples/
├── ros2/              # ROS 2 examples
│   ├── basic_nodes.py
│   └── publisher_subscriber.py
├── urdf/              # Robot description files
│   └── humanoid_model.urdf
└── isaac/             # Isaac examples
    └── perception_example.py
```

### Running Examples
1. Navigate to the appropriate directory
2. Ensure ROS 2 environment is sourced
3. Execute the example file
4. Observe the output and compare with textbook explanations

## Creating Your Own Experiments

### 1. Clone the Example Structure
Use the provided examples as templates for your own experiments.

### 2. Modify Parameters
Change parameters in launch files or code to see different behaviors.

### 3. Extend Functionality
Add new features to existing examples to deepen understanding.

## Validation and Testing

### Code Verification
Each code example should run without errors in the appropriate environment.

### Concept Validation
Test your understanding by predicting outcomes before running simulations.

### Citation Verification
Check the referenced sources to deepen your understanding of concepts.

## Getting Help

### Documentation
- Official ROS 2 documentation
- Gazebo tutorials
- Isaac Sim documentation
- This textbook's reference section

### Community Resources
- ROS Discourse forums
- Gazebo community
- Robotics Stack Exchange
- Academic papers referenced in the textbook

## Next Steps

1. Complete the setup process
2. Read Chapter 1 and execute the foundational examples
3. Progress through each module systematically
4. Complete the capstone project to synthesize all learned concepts
5. Validate your learning by implementing original robotics solutions