import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx(styles.heroBanner)} role="banner">
      <div className="container">
        <Heading as="h1" className={styles.heroTitle}>
          Physical AI & Humanoid Robotics Textbook
        </Heading>
        <p className={styles.heroSubtitle}>
          A comprehensive guide to embodied intelligence and humanoid control systems
        </p>
        <div className={styles.buttons}>
          <a
            className={styles.heroButton}
            href="/docs/intro"
          >
            Start Exploring
          </a>
        </div>
        <div className={styles.modulesSection}>
          <div className={styles.modulesContainer}>
            <div className={styles.moduleCard}>
              <h3 className={styles.moduleTitle}>Module 1 (Physical AI)</h3>
              <ul className={styles.moduleTopics}>
                <li>Foundations of embodied intelligence</li>
                <li>Neural networks and deep learning</li>
                <li>Physics simulation and dynamics</li>
                <li>Sensor fusion and perception</li>
              </ul>
              <Link to="/docs/physical-ai/foundations" className={styles.cardButton}>
                Explore Module
              </Link>
            </div>
            <div className={styles.moduleCard}>
              <h3 className={styles.moduleTitle}>Module 2 (ROS2)</h3>
              <ul className={styles.moduleTopics}>
                <li>ROS 2 architecture and concepts</li>
                <li>Nodes, topics, and services</li>
                <li>Message passing and communication</li>
                <li>Robot control and navigation</li>
              </ul>
              <Link to="/docs/ros2/overview" className={styles.cardButton}>
                Explore Module
              </Link>
            </div>
            <div className={styles.moduleCard}>
              <h3 className={styles.moduleTitle}>Module 3 (Simulation)</h3>
              <ul className={styles.moduleTopics}>
                <li>Gazebo simulation environment</li>
                <li>Physics engines and collision</li>
                <li>Robot models and URDF</li>
                <li>Simulation workflows</li>
              </ul>
              <Link to="/docs/simulation/gazebo" className={styles.cardButton}>
                Explore Module
              </Link>
            </div>
            <div className={styles.moduleCard}>
              <h3 className={styles.moduleTitle}>Module 4 (Isaac)</h3>
              <ul className={styles.moduleTopics}>
                <li>Isaac Sim fundamentals</li>
                <li>NVIDIA robotics platform</li>
                <li>AI training environments</li>
                <li>Hardware acceleration</li>
              </ul>
              <Link to="/docs/isaac/isaac-sim" className={styles.cardButton}>
                Explore Module
              </Link>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Physical AI & Humanoid Robotics Textbook`}
      description="A comprehensive guide to embodied intelligence and humanoid control systems">
      <HomepageHeader />
    </Layout>
  );
}
