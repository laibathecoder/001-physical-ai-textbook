@echo off
REM PDF Export Script for Physical AI & Humanoid Robotics Textbook (Windows)
REM This script combines all markdown files into a single PDF with embedded citations

echo Starting PDF export for Physical AI & Humanoid Robotics Textbook...

REM Create a temporary directory for the export
set TEMP_DIR=%TEMP%\textbook_export_%RANDOM%
mkdir "%TEMP_DIR%"
echo Using temporary directory: %TEMP_DIR%

REM Create a combined markdown file with proper frontmatter
echo --- > "%TEMP_DIR%\combined_textbook.md"
echo title: "Physical AI & Humanoid Robotics Textbook" >> "%TEMP_DIR%\combined_textbook.md"
echo author: [Physical AI ^& Humanoid Robotics Project Team] >> "%TEMP_DIR%\combined_textbook.md"
echo date: "2025" >> "%TEMP_DIR%\combined_textbook.md"
echo abstract: ^| >> "%TEMP_DIR%\combined_textbook.md"
echo   A comprehensive guide to embodied intelligence and humanoid control systems that bridges digital AI concepts with real-world humanoid robot behavior. This textbook guides readers from foundational Physical AI concepts to developing a complete simulated humanoid capable of natural interaction. >> "%TEMP_DIR%\combined_textbook.md"
echo --- >> "%TEMP_DIR%\combined_textbook.md"
echo. >> "%TEMP_DIR%\combined_textbook.md"

echo # Introduction >> "%TEMP_DIR%\combined_textbook.md"
type docs\intro\index.md >> "%TEMP_DIR%\combined_textbook.md"

echo. >> "%TEMP_DIR%\combined_textbook.md"
echo # Physical AI ^& Embodied Intelligence >> "%TEMP_DIR%\combined_textbook.md"
type docs\physical-ai\foundations.md >> "%TEMP_DIR%\combined_textbook.md"
type docs\physical-ai\concepts.md >> "%TEMP_DIR%\combined_textbook.md"
type docs\physical-ai\assessment.md >> "%TEMP_DIR%\combined_textbook.md"

echo. >> "%TEMP_DIR%\combined_textbook.md"
echo # ROS 2 - The Robotic Nervous System >> "%TEMP_DIR%\combined_textbook.md"
type docs\ros2\overview.md >> "%TEMP_DIR%\combined_textbook.md"
type docs\ros2\nodes-topics.md >> "%TEMP_DIR%\combined_textbook.md"
type docs\ros2\urdf.md >> "%TEMP_DIR%\combined_textbook.md"
type docs\ros2\launch-files.md >> "%TEMP_DIR%\combined_textbook.md"
type docs\ros2\exercises.md >> "%TEMP_DIR%\combined_textbook.md"

echo. >> "%TEMP_DIR%\combined_textbook.md"
echo # Digital Twin Simulation >> "%TEMP_DIR%\combined_textbook.md"
type docs\simulation\gazebo.md >> "%TEMP_DIR%\combined_textbook.md"
type docs\simulation\unity.md >> "%TEMP_DIR%\combined_textbook.md"
type docs\simulation\sensors.md >> "%TEMP_DIR%\combined_textbook.md"
type docs\simulation\exercises.md >> "%TEMP_DIR%\combined_textbook.md"

echo. >> "%TEMP_DIR%\combined_textbook.md"
echo # NVIDIA Isaac AI Systems >> "%TEMP_DIR%\combined_textbook.md"
type docs\isaac\isaac-sim.md >> "%TEMP_DIR%\combined_textbook.md"
type docs\isaac\isaac-ros.md >> "%TEMP_DIR%\combined_textbook.md"
type docs\isaac\nav2.md >> "%TEMP_DIR%\combined_textbook.md"
type docs\isaac\exercises.md >> "%TEMP_DIR%\combined_textbook.md"

echo. >> "%TEMP_DIR%\combined_textbook.md"
echo # Vision-Language-Action (VLA) >> "%TEMP_DIR%\combined_textbook.md"
type docs\vla\vision-language-action.md >> "%TEMP_DIR%\combined_textbook.md"
type docs\vla\whisper.md >> "%TEMP_DIR%\combined_textbook.md"
type docs\vla\exercises.md >> "%TEMP_DIR%\combined_textbook.md"

echo. >> "%TEMP_DIR%\combined_textbook.md"
echo # Capstone: Autonomous Humanoid Robot >> "%TEMP_DIR%\combined_textbook.md"
type docs\capstone\project.md >> "%TEMP_DIR%\combined_textbook.md"
type docs\capstone\path-planning.md >> "%TEMP_DIR%\combined_textbook.md"
type docs\capstone\manipulation.md >> "%TEMP_DIR%\combined_textbook.md"
type docs\capstone\assessment.md >> "%TEMP_DIR%\combined_textbook.md"
type docs\capstone\capstone_integration_issue.md >> "%TEMP_DIR%\combined_textbook.md"

echo. >> "%TEMP_DIR%\combined_textbook.md"
echo # References >> "%TEMP_DIR%\combined_textbook.md"
type docs\references\citations.md >> "%TEMP_DIR%\combined_textbook.md"

echo. >> "%TEMP_DIR%\combined_textbook.md"
echo # Appendix: Environment Setup Guide >> "%TEMP_DIR%\combined_textbook.md"
type docs\tutorial\setup.md >> "%TEMP_DIR%\combined_textbook.md"

REM Create a header file with necessary LaTeX packages
echo \usepackage{fontspec} > "%TEMP_DIR%\include-header.tex"
echo \usepackage{unicode-math} >> "%TEMP_DIR%\include-header.tex"
echo \usepackage{booktabs} >> "%TEMP_DIR%\include-header.tex"
echo \usepackage{longtable} >> "%TEMP_DIR%\include-header.tex"
echo \usepackage{array} >> "%TEMP_DIR%\include-header.tex"
echo \usepackage{multirow} >> "%TEMP_DIR%\include-header.tex"
echo \usepackage{wrapfig} >> "%TEMP_DIR%\include-header.tex"
echo \usepackage{float} >> "%TEMP_DIR%\include-header.tex"
echo \usepackage{colortbl} >> "%TEMP_DIR%\include-header.tex"
echo \usepackage{pdflscape} >> "%TEMP_DIR%\include-header.tex"
echo \usepackage{tabu} >> "%TEMP_DIR%\include-header.tex"
echo \usepackage{threeparttable} >> "%TEMP_DIR%\include-header.tex"
echo \usepackage{makecell} >> "%TEMP_DIR%\include-header.tex"
echo \usepackage{xcolor} >> "%TEMP_DIR%\include-header.tex"
echo \usepackage{listings} >> "%TEMP_DIR%\include-header.tex"
echo \definecolor{codebg}{rgb}{0.95,0.95,0.95} >> "%TEMP_DIR%\include-header.tex"
echo \lstset{ >> "%TEMP_DIR%\include-header.tex"
echo   backgroundcolor=\color{codebg}, >> "%TEMP_DIR%\include-header.tex"
echo   basicstyle=\ttfamily\small, >> "%TEMP_DIR%\include-header.tex"
echo   breaklines=true, >> "%TEMP_DIR%\include-header.tex"
echo   postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space} >> "%TEMP_DIR%\include-header.tex"
echo } >> "%TEMP_DIR%\include-header.tex"

REM Run pandoc to generate the PDF
echo Generating PDF with pandoc...

pandoc "%TEMP_DIR%\combined_textbook.md" ^
  --output textbook.pdf ^
  --from markdown ^
  --to pdf ^
  --pdf-engine=xelatex ^
  --bibliography=docs/references/citations.md ^
  --citeproc ^
  --table-of-contents ^
  --toc-depth=3 ^
  --number-sections ^
  --highlight-style=tango ^
  --standalone ^
  --include-in-header="%TEMP_DIR%\include-header.tex" ^
  --metadata=title="Physical AI ^& Humanoid Robotics Textbook" ^
  --metadata=author="Physical AI ^& Humanoid Robotics Project Team" ^
  --metadata=date="2025"

if %ERRORLEVEL% EQU 0 (
    echo PDF export completed successfully!
    echo Output file: textbook.pdf
) else (
    echo PDF export failed. Please ensure pandoc and xelatex are installed and in your PATH.
    echo On Windows, you can install:
    echo 1. MiKTeX (for xelatex): https://miktex.org/
    echo 2. Pandoc: https://pandoc.org/installing.html
)

REM Clean up
rmdir /s /q "%TEMP_DIR%"