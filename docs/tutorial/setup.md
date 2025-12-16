---
sidebar_position: 1
title: Environment Setup Guide
---

# Environment Setup Guide

## Introduction

This guide provides step-by-step instructions for setting up the development environment required to work with the Physical AI & Humanoid Robotics textbook. The setup process includes installing ROS 2, Gazebo, NVIDIA Isaac Sim, Unity, and other tools necessary for implementing the examples and exercises in this textbook.

## System Requirements

### Minimum System Requirements
- **Operating System**: Ubuntu 20.04 LTS or 22.04 LTS (recommended), Windows 10/11 (with WSL2), or macOS (limited support)
- **CPU**: 8+ cores (Intel i7 or AMD Ryzen 7 equivalent or better)
- **RAM**: 16GB minimum, 32GB recommended
- **GPU**: NVIDIA GPU with CUDA Compute Capability 6.0 or higher (GTX 1060/RX 580 equivalent or better)
- **Storage**: 50GB free space minimum
- **Network**: Internet connection for package downloads and updates

### Recommended System Configuration
- **CPU**: 12+ cores (Intel i9 or AMD Ryzen 9)
- **RAM**: 32GB or more
- **GPU**: NVIDIA RTX 3080/4080 or better with 12GB+ VRAM
- **Storage**: SSD with 100GB+ free space

## Prerequisites Installation

### Step 1: Install Basic Dependencies

#### For Ubuntu 22.04 LTS:
```bash
# Update package lists
sudo apt update && sudo apt upgrade -y

# Install basic build tools and dependencies
sudo apt install -y \
    build-essential \
    cmake \
    git \
    python3-colcon-common-extensions \
    python3-flake8 \
    python3-pip \
    python3-rosdep \
    python3-vcstool \
    wget \
    curl \
    gnupg \
    lsb-release \
    software-properties-common \
    python3-rosinstall-generator \
    python3-rosinstall \
    python3-pykdl \
    libeigen3-dev \
    libboost-system-dev \
    libboost-python-dev \
    libtinyxml2-dev \
    libopencv-dev \
    python3-opencv \
    python3-dev \
    libasio-dev \
    libtinyxml-dev \
    libbullet-dev \
    libcunit1-dev \
    libgraphviz-dev \
    libjsoncpp-dev \
    liblua5.3-dev \
    liborocos-kdl-dev \
    libpcl-dev \
    libsqlite3-dev \
    libyaml-dev \
    openjdk-11-jdk \
    pkg-config \
    python3-catkin-pkg-modules \
    python3-dev \
    python3-nose \
    python3-pip \
    python3-rosdep \
    python3-setuptools \
    python3-vcstool \
    rsync \
    screen \
    unzip \
    zip \
    zlib1g-dev

# Install pip packages
pip3 install -U \
    argcomplete \
    colcon-output \
    flake8 \
    flake8-blind-except \
    flake8-builtins \
    flake8-class-newline \
    flake8-comprehensions \
    flake8-deprecated \
    flake8-import-order \
    flake8-quotes \
    pytest-repeat \
    pytest-rerunfailures \
    setuptools \
    wheel
```

### Step 2: Install ROS 2 Humble Hawksbill

```bash
# Set up the ROS 2 apt repository
sudo apt update && sudo apt install -y curl gnupg lsb-release
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | sudo gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update
sudo apt install -y ros-humble-desktop
sudo apt install -y python3-colcon-common-extensions python3-rosdep python3-vcstool

# Install ROS 2 development tools
sudo apt install -y \
    ros-dev-tools \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-xacro \
    ros-humble-joint-state-publisher \
    ros-humble-robot-state-publisher \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-rosbridge-suite \
    ros-humble-vision-msgs \
    ros-humble-geometry-msgs

# Source ROS 2 environment
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source /opt/ros/humble/setup.bash
```

### Step 3: Install Gazebo Garden

```bash
# Add Gazebo's Ubuntu package repository
sudo curl -sSL http://get.gazebosim.org | sh

# Install Gazebo Garden
sudo apt install gz-garden

# Install additional Gazebo plugins and tools
sudo apt install \
    libgz-sim7-dev \
    libgz-common5-dev \
    libgz-math8-dev \
    libgz-physics6-dev \
    libgz-sensors8-dev \
    libgz-transport13-dev \
    libgz-fuel-tools9-dev \
    libgz-gui8-dev \
    libgz-rendering8-dev \
    libgz-cmake4-dev \
    python3-gz-sim7
```

### Step 4: Install NVIDIA Isaac Sim (Prerequisites)

```bash
# Install NVIDIA driver (if not already installed)
# Check if NVIDIA GPU is detected
lspci | grep -i nvidia

# Install CUDA (if not already installed)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
sudo apt update
sudo apt install -y cuda-toolkit-12-0

# Install additional NVIDIA libraries
sudo apt install -y \
    libnvinfer8 \
    libnvinfer-dev \
    libnvonnxparsers-dev \
    libnvparsers-dev \
    python3-libnvinfer \
    nvidia-utils-470
```

### Step 5: Install Python Development Environment

```bash
# Install Python virtual environment tools
sudo apt install -y python3-venv python3-pip

# Create project virtual environment
cd ~/workspace
mkdir -p physical_ai_textbook
cd physical_ai_textbook
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install essential Python packages for robotics
pip install \
    numpy \
    scipy \
    matplotlib \
    pandas \
    opencv-python \
    pyquaternion \
    transforms3d \
    openai-whisper \
    torch \
    torchvision \
    torchaudio \
    --index-url https://download.pytorch.org/whl/cu118
```

### Step 6: Install Docusaurus for Documentation

```bash
# Install Node.js and npm (if not already installed)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install project dependencies
npm install -g yarn
```

## Isaac Sim Installation (Detailed Instructions)

### Download Isaac Sim
1. Visit the [NVIDIA Developer Portal](https://developer.nvidia.com/isaac-sim)
2. Register/login with your NVIDIA developer account
3. Download Isaac Sim (select the appropriate version for your system)
4. Extract the downloaded file to your preferred location (e.g., `/home/username/isaac-sim`)

### Install Isaac Sim
```bash
# Extract the downloaded Isaac Sim archive
tar -xzf isaac-sim-XXXX.X.X.tar.gz -C ~/workspace/

# Navigate to Isaac Sim directory
cd ~/workspace/isaac-sim

# Run the installation script
./isaac-sim-headless.sh  # For headless operation
# OR
./isaac-sim.sh  # For GUI operation
```

### Configure Isaac Sim Environment
```bash
# Add Isaac Sim to your bash profile
echo "# Isaac Sim Environment" >> ~/.bashrc
echo "export ISAACSIM_PATH=~/workspace/isaac-sim" >> ~/.bashrc
echo "export OMNI_SERVICES_APP=omniorb" >> ~/.bashrc
echo "source ~/workspace/isaac-sim/setup_conda_env.sh" >> ~/.bashrc

# Apply changes
source ~/.bashrc
```

## Unity Installation (Optional - Advanced Users)

### Install Unity Hub and Editor
1. Download Unity Hub from the [Unity website](https://unity.com/download)
2. Install Unity Hub
3. Through Unity Hub, install Unity 2022.3 LTS
4. Install the following modules:
   - Linux Build Support (IL2CPP)
   - Visual Studio Editor (for Windows users)

### Unity Robotics Package Installation
1. Open Unity Hub and create a new 3D project
2. In the Package Manager, install:
   - Unity Robotics Package
   - Unity Simulation Package
   - URDF Importer

## Project Workspace Setup

### Create Catkin Workspace
```bash
# Create ROS 2 workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws

# Source ROS 2 environment
source /opt/ros/humble/setup.bash

# Build the workspace (initial empty build)
colcon build --symlink-install
```

### Clone Textbook Examples
```bash
# Navigate to source directory
cd ~/ros2_ws/src

# Clone the textbook example repository (or create your own structure)
mkdir -p physical_ai_examples
cd physical_ai_examples

# Create the basic project structure as outlined in the textbook
mkdir -p \
    physical_ai_foundations \
    ros2_examples \
    simulation_examples \
    isaac_examples \
    vla_examples \
    capstone_project

# Create basic CMakeLists.txt and package.xml for each package
```

### Create Basic Package Structure
```bash
# Create a basic package for physical AI examples
cd ~/ros2_ws/src/physical_ai_examples/physical_ai_foundations
touch CMakeLists.txt package.xml

# Example package.xml for a basic ROS 2 package
cat > package.xml << EOF
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>physical_ai_foundations</name>
  <version>0.0.1</version>
  <description>Physical AI Foundations Examples</description>
  <maintainer email="student@example.com">Student</maintainer>
  <license>Apache-2.0</license>

  <depend>rclpy</depend>
  <depend>std_msgs</depend>
  <depend>geometry_msgs</depend>
  <depend>sensor_msgs</depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
EOF

# Example CMakeLists.txt
cat > CMakeLists.txt << EOF
cmake_minimum_required(VERSION 3.8)
project(physical_ai_foundations)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

# Install Python modules
ament_python_install_package(\${PROJECT_NAME})

# Install launch files
install(DIRECTORY
  launch
  DESTINATION share/\${PROJECT_NAME}/
)

# Install scripts
install(PROGRAMS
  scripts/
  DESTINATION lib/\${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
EOF
```

## Environment Validation

### Validate ROS 2 Installation
```bash
# Source the ROS 2 environment
source /opt/ros/humble/setup.bash

# Test basic ROS 2 functionality
ros2 topic list
ros2 node list

# Create a test workspace to verify everything works
mkdir -p ~/test_ws/src
cd ~/test_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash

# Test creating a simple publisher/subscriber
ros2 run demo_nodes_cpp talker &
ros2 run demo_nodes_cpp listener &
```

### Validate Gazebo Installation
```bash
# Test Gazebo installation
gz sim --version
gz sim -s verbose

# If Gazebo doesn't launch with GUI, try headless mode
gz sim -s verbose --headless-rendering
```

### Validate Python Environment
```bash
# Activate your Python environment
source ~/workspace/physical_ai_textbook/venv/bin/activate

# Test Python packages
python3 -c "import numpy; print('NumPy version:', numpy.__version__)"
python3 -c "import torch; print('PyTorch version:', torch.__version__); print('CUDA available:', torch.cuda.is_available())"
python3 -c "import cv2; print('OpenCV version:', cv2.__version__)"
```

### Validate Isaac Sim (if installed)
```bash
# Test Isaac Sim installation
cd ~/workspace/isaac-sim
./python.sh -c "import omni; print('Isaac Sim Python interface OK')"
```

## Troubleshooting Common Issues

### ROS 2 Installation Issues
**Problem**: `command 'ros2' not found`
**Solution**: Make sure to source the ROS 2 environment:
```bash
source /opt/ros/humble/setup.bash
# Add this line to your ~/.bashrc to make it permanent
```

**Problem**: Permission denied during apt install
**Solution**: Use sudo properly and update package lists:
```bash
sudo apt update
sudo apt install [package_name]
```

### Gazebo Installation Issues
**Problem**: Gazebo crashes on startup
**Solution**: Check GPU drivers and try headless mode first:
```bash
gz sim --headless-rendering
```

**Problem**: GPU rendering issues
**Solution**: Install appropriate graphics drivers:
```bash
sudo ubuntu-drivers autoinstall  # For automatic driver installation
```

### Isaac Sim Issues
**Problem**: Isaac Sim fails to launch with graphics errors
**Solution**:
1. Verify NVIDIA GPU and drivers
2. Check CUDA installation
3. Ensure OpenGL support
4. Try launching from a proper display environment

### Python Environment Issues
**Problem**: Package installation fails
**Solution**:
1. Update pip: `pip install --upgrade pip`
2. Use appropriate index: `pip install --index-url https://download.pytorch.org/whl/cu118 torch`
3. Check CUDA compatibility

## Development Workflow Setup

### VS Code Configuration (Recommended)
```bash
# Install VS Code if not already installed
sudo snap install --classic code

# Install recommended extensions for ROS 2 development
code --install-extension ms-iot.vscode-ros
code --install-extension ms-python.python
code --install-extension ms-vscode.cpptools
code --install-extension twxs.cmake
```

### Create Development Scripts
```bash
# Create helper scripts for common operations
mkdir -p ~/workspace/physical_ai_textbook/scripts

# Script to source all environments
cat > ~/workspace/physical_ai_textbook/scripts/setup_env.sh << EOF
#!/bin/bash

# Source ROS 2 environment
source /opt/ros/humble/setup.bash

# Source workspace (if built)
if [ -f ~/ros2_ws/install/setup.bash ]; then
    source ~/ros2_ws/install/setup.bash
fi

# Activate Python virtual environment
source ~/workspace/physical_ai_textbook/venv/bin/activate

# Export Isaac Sim path if installed
if [ -d ~/workspace/isaac-sim ]; then
    export ISAACSIM_PATH=~/workspace/isaac-sim
fi

echo "Environment setup complete!"
echo "ROS_DISTRO: \$ROS_DISTRO"
echo "Python virtual environment activated"
EOF

chmod +x ~/workspace/physical_ai_textbook/scripts/setup_env.sh

# Script to build ROS 2 workspace
cat > ~/workspace/physical_ai_textbook/scripts/build_workspace.sh << EOF
#!/bin/bash

# Build ROS 2 workspace
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install --parallel-workers 4
source install/setup.bash
echo "Workspace built and sourced!"
EOF

chmod +x ~/workspace/physical_ai_textbook/scripts/build_workspace.sh
```

## Verification Checklist

### Before Proceeding with Textbook Examples
- [ ] ROS 2 Humble installed and accessible
- [ ] Gazebo Garden installed and running
- [ ] Python environment with required packages
- [ ] Docusaurus installed for documentation
- [ ] CUDA drivers and toolkit installed (for Isaac Sim)
- [ ] Isaac Sim installed and accessible (if installed)
- [ ] Unity Hub and Editor installed (if pursuing Unity integration)
- [ ] Basic workspace structure created
- [ ] Helper scripts created and tested

## Next Steps

Once your environment is set up and validated, proceed with:

1. **Chapter 1**: Physical AI Foundations - Start with the introductory examples
2. **Chapter 2**: ROS 2 Concepts - Follow the node and topic examples
3. **Chapter 3**: Simulation - Begin with basic Gazebo examples
4. **Chapter 4**: Isaac Systems - Work with Isaac Sim when ready
5. **Chapter 5**: Vision-Language-Action - Integrate perception and action
6. **Chapter 6**: Capstone Project - Combine all concepts in a complete system

## Getting Help

### Documentation Resources
- [ROS 2 Documentation](https://docs.ros.org/en/humble/)
- [Gazebo Documentation](https://gazebosim.org/)
- [Isaac Sim Documentation](https://docs.omniverse.nvidia.com/isaac-sim/latest/)
- [Unity Robotics Documentation](https://unity.com/solutions/industries/robotics)

### Community Resources
- [ROS Answers](https://answers.ros.org/questions/)
- [Gazebo Answers](https://answers.gazebosim.org/)
- [NVIDIA Developer Forums](https://forums.developer.nvidia.com/)
- [Robotics Stack Exchange](https://robotics.stackexchange.com/)

## Maintaining Your Environment

### Regular Updates
```bash
# Update ROS 2 packages
sudo apt update && sudo apt upgrade

# Update Python packages
source ~/workspace/physical_ai_textbook/venv/bin/activate
pip install --upgrade --upgrade-strategy eager numpy scipy torch

# Backup your environment configuration
cp ~/.bashrc ~/.bashrc.backup.\$(date +%Y%m%d)
```

### Environment Cleanup
Periodically clean up your environment:
- Remove unused Docker containers and images (if using)
- Clear ROS 2 logs in `~/.ros/log/`
- Update your workspace as needed based on textbook progress

Your environment is now set up for working with the Physical AI & Humanoid Robotics textbook. Each chapter will build on these foundations, adding complexity as you progress through the material.