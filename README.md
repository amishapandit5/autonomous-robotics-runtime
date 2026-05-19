# RoboCursor

Autonomous Robotics Engineering Infrastructure for ROS2 and Physical AI Systems.

RoboCursor is an autonomous software engineering backend built specifically for robotics workflows. RoboCursor focuses on ROS2-native orchestration, autonomous runtime debugging, project-aware memory, multi-file architecture generation, and robotics infrastructure execution.Unlike other platforms which are editor first this system is Runtime First which is AI runtime system built around execution infrastructure itself.


# Vision

RoboCursor is being built to understand robotics systems.

The goal is to create an autonomous engineering system capable of:
- generating robotics architectures
- orchestrating ROS2 systems
- autonomously debugging runtime failures
- managing multi-file robotics projects
- evolving through long-term engineering memory


# Current Features

## Autonomous Multi-File Code Generation
- Generates coordinated robotics systems across multiple files
- Supports modular ROS2 architectures
- Handles planner-driven file creation/modification

## Project-Aware Memory
- Each project maintains isolated architecture memory
- Retrieval system understands existing project structure
- Prevents cross-project memory contamination

## ROS2 Runtime Execution
- Executes generated ROS2 Python systems inside Dockerized ROS2 environments
- Supports rclpy-based robotics workflows

## Autonomous Runtime Repair
- Detects runtime failures
- Attempts iterative self-repair
- Re-executes systems automatically

## Dependency Intelligence
- Differentiates between:
  - ROS dependencies
  - pip dependencies
  - built-in Python modules
- Prevents invalid dependency installations

## Architecture Decision Tracking
- Stores architectural reasoning and project decisions
- Builds project-level engineering memory

---

# Architecture

User Prompt 
↓
Planner System
↓
Relevant File Retrieval
↓
Project Context Builder
↓
Multi-File Code Generation(local models)
↓
Dockerized ROS2 Runtime(sandboxed execution)
↓
Runtime Error Detection
↓
Autonomous Repair Loop
↓
Project Indexing + Architecture Memory
↓
Project stored on local device


Demo
Demo video:
(https://drive.google.com/file/d/1UppKruS8y1JU8iHm4NmLQVQtdxoijboL/view?usp=drivesdk)

# Example Prompt
{
  "project": "autonomous_drone_system",
  "prompt": "Create a ROS2 autonomous drone patrol system with separate files for drone navigation, lidar obstacle detection, mission coordination, and launch management."
}

Tech Stack
- Python
- FastAPI
- Docker
- ROS2 Humble
- Ollama
- Qwen2.5-Coder
- Autonomous Runtime Orchestration

# Future Roadmap:
- Simulation environments (Gazebo / Isaac Sim)
- Multi-container robotics orchestration
- GPU execution infrastructure
- Autonomous testing pipelines
- Long-term engineering memory
- Distributed runtime systems
- Solo CLI integration
- Multi-agent engineering systems
