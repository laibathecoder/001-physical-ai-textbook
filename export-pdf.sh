#!/bin/bash

# PDF Export Script for Physical AI & Humanoid Robotics Textbook
# This script combines all markdown files into a single PDF with embedded citations

set -e  # Exit on any error

echo "Starting PDF export for Physical AI & Humanoid Robotics Textbook..."

# Create a temporary directory for the export
TEMP_DIR=$(mktemp -d)
echo "Using temporary directory: $TEMP_DIR"

# Copy all markdown files to the temp directory and create a combined version
echo "Gathering documentation files..."

# Create a combined markdown file with proper frontmatter
cat > "$TEMP_DIR/combined_textbook.md" << 'EOF'
---
title: "Physical AI & Humanoid Robotics Textbook"
author: [Physical AI & Humanoid Robotics Project Team]
date: "2025"
abstract: |
  A comprehensive guide to embodied intelligence and humanoid control systems that bridges digital AI concepts with real-world humanoid robot behavior. This textbook guides readers from foundational Physical AI concepts to developing a complete simulated humanoid capable of natural interaction.
---

# Introduction

Welcome to the Physical AI & Humanoid Robotics textbook. This comprehensive guide bridges digital AI concepts with real-world humanoid robot behavior, guiding you from foundational Physical AI concepts to developing a complete simulated humanoid capable of natural interaction.

EOF

# Add all the main content files in the correct order based on the sidebar structure
cat docs/intro/index.md >> "$TEMP_DIR/combined_textbook.md"
echo -e "\n\n# Physical AI & Embodied Intelligence\n" >> "$TEMP_DIR/combined_textbook.md"
cat docs/physical-ai/foundations.md >> "$TEMP_DIR/combined_textbook.md"
cat docs/physical-ai/concepts.md >> "$TEMP_DIR/combined_textbook.md"
cat docs/physical-ai/assessment.md >> "$TEMP_DIR/combined_textbook.md"

echo -e "\n\n# ROS 2 - The Robotic Nervous System\n" >> "$TEMP_DIR/combined_textbook.md"
cat docs/ros2/overview.md >> "$TEMP_DIR/combined_textbook.md"
cat docs/ros2/nodes-topics.md >> "$TEMP_DIR/combined_textbook.md"
cat docs/ros2/urdf.md >> "$TEMP_DIR/combined_textbook.md"
cat docs/ros2/launch-files.md >> "$TEMP_DIR/combined_textbook.md"
cat docs/ros2/exercises.md >> "$TEMP_DIR/combined_textbook.md"

echo -e "\n\n# Digital Twin Simulation\n" >> "$TEMP_DIR/combined_textbook.md"
cat docs/simulation/gazebo.md >> "$TEMP_DIR/combined_textbook.md"
cat docs/simulation/unity.md >> "$TEMP_DIR/combined_textbook.md"
cat docs/simulation/sensors.md >> "$TEMP_DIR/combined_textbook.md"
cat docs/simulation/exercises.md >> "$TEMP_DIR/combined_textbook.md"

echo -e "\n\n# NVIDIA Isaac AI Systems\n" >> "$TEMP_DIR/combined_textbook.md"
cat docs/isaac/isaac-sim.md >> "$TEMP_DIR/combined_textbook.md"
cat docs/isaac/isaac-ros.md >> "$TEMP_DIR/combined_textbook.md"
cat docs/isaac/nav2.md >> "$TEMP_DIR/combined_textbook.md"
cat docs/isaac/exercises.md >> "$TEMP_DIR/combined_textbook.md"

echo -e "\n\n# Vision-Language-Action (VLA)\n" >> "$TEMP_DIR/combined_textbook.md"
cat docs/vla/vision-language-action.md >> "$TEMP_DIR/combined_textbook.md"
cat docs/vla/whisper.md >> "$TEMP_DIR/combined_textbook.md"
cat docs/vla/exercises.md >> "$TEMP_DIR/combined_textbook.md"

echo -e "\n\n# Capstone: Autonomous Humanoid Robot\n" >> "$TEMP_DIR/combined_textbook.md"
cat docs/capstone/project.md >> "$TEMP_DIR/combined_textbook.md"
cat docs/capstone/path-planning.md >> "$TEMP_DIR/combined_textbook.md"
cat docs/capstone/manipulation.md >> "$TEMP_DIR/combined_textbook.md"
cat docs/capstone/assessment.md >> "$TEMP_DIR/combined_textbook.md"
cat docs/capstone/capstone_integration_issue.md >> "$TEMP_DIR/combined_textbook.md"

echo -e "\n\n# References\n" >> "$TEMP_DIR/combined_textbook.md"
cat docs/references/citations.md >> "$TEMP_DIR/combined_textbook.md"

# Add the setup guide at the end
echo -e "\n\n# Appendix: Environment Setup Guide\n" >> "$TEMP_DIR/combined_textbook.md"
cat docs/tutorial/setup.md >> "$TEMP_DIR/combined_textbook.md"

# Run pandoc to generate the PDF
echo "Generating PDF with pandoc..."

pandoc "$TEMP_DIR/combined_textbook.md" \
  --output textbook.pdf \
  --from markdown \
  --to pdf \
  --pdf-engine=xelatex \
  --bibliography=docs/references/citations.md \
  --citeproc \
  --table-of-contents \
  --toc-depth=3 \
  --number-sections \
  --highlight-style=tango \
  --standalone \
  --variable=documentclass=report \
  --variable=classoption=oneside \
  --variable=fontsize=12pt \
  --variable=geometry=margin=1in \
  --variable=linkcolor=blue \
  --variable=urlcolor=blue \
  --variable=citecolor=black \
  --include-in-header="$TEMP_DIR/include-header.tex" \
  --metadata=title="Physical AI & Humanoid Robotics Textbook" \
  --metadata=author="Physical AI & Humanoid Robotics Project Team" \
  --metadata=date="2025"

# Create a header file with necessary LaTeX packages
cat > "$TEMP_DIR/include-header.tex" << 'TEX_EOF'
\usepackage{fontspec}
\usepackage{unicode-math}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{multirow}
\usepackage{wrapfig}
\usepackage{float}
\usepackage{colortbl}
\usepackage{pdflscape}
\usepackage{tabu}
\usepackage{threeparttable}
\usepackage{makecell}
\usepackage{xcolor}
\usepackage{listings}
\definecolor{codebg}{rgb}{0.95,0.95,0.95}
\lstset{
  backgroundcolor=\color{codebg},
  basicstyle=\ttfamily\small,
  breaklines=true,
  postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space}
}
TEX_EOF

# Re-run pandoc with the header file
pandoc "$TEMP_DIR/combined_textbook.md" \
  --output textbook.pdf \
  --from markdown \
  --to pdf \
  --pdf-engine=xelatex \
  --bibliography=docs/references/citations.md \
  --citeproc \
  --table-of-contents \
  --toc-depth=3 \
  --number-sections \
  --highlight-style=tango \
  --standalone \
  --include-in-header="$TEMP_DIR/include-header.tex"

echo "PDF export completed successfully!"
echo "Output file: textbook.pdf"

# Clean up
rm -rf "$TEMP_DIR"