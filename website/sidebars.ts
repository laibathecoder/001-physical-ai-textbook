import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // Manual sidebar configuration for the Physical AI & Humanoid Robotics textbook
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Introduction',
      items: ['intro/index'],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Physical AI & Embodied Intelligence',
      items: [
        'physical-ai/foundations',
        'physical-ai/concepts',
        'physical-ai/assessment',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'ROS 2 - The Robotic Nervous System',
      items: [
        'ros2/overview',
        'ros2/nodes-topics',
        'ros2/urdf',
        'ros2/launch-files',
        'ros2/exercises',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Digital Twin Simulation',
      items: [
        'simulation/gazebo',
        'simulation/unity',
        'simulation/sensors',
        'simulation/exercises',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'NVIDIA Isaac AI Systems',
      items: [
        'isaac/isaac-sim',
        'isaac/isaac-ros',
        'isaac/nav2',
        'isaac/exercises',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Vision-Language-Action (VLA)',
      items: [
        'vla/vision-language-action',
        'vla/whisper',
        'vla/exercises',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Capstone: Autonomous Humanoid Robot',
      items: [
        'capstone/project',
        'capstone/path-planning',
        'capstone/manipulation',
        'capstone/assessment',
        'capstone/capstone_integration_issue',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'References',
      items: ['references/citations'],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Tutorial',
      items: ['tutorial/setup'],
      collapsed: false,
    },
  ],
};

export default sidebars;
