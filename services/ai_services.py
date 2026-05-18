import requests

from utils.cleaner import (
    clean_workspace_code
)


MODEL_NAME = "qwen2.5-coder:3b"


def is_ros_request(user_prompt):

    robotics_keywords = [

        "ros2",
        "rclpy",
        "lidar",
        "laserscan",
        "tf2",
        "nav2",
        "odometry",
        "occupancy grid",
        "robot",
        "drone",
        "navigation",
        "slam"
    ]

    prompt_lower = user_prompt.lower()

    return any(

        keyword in prompt_lower

        for keyword in robotics_keywords
    )


def build_capability_rules(user_prompt):

    if is_ros_request(user_prompt):

        return """

ROS2 RULES:
- Use ROS2 only
- Use rclpy instead of rospy
- Never use ROS1 APIs
- Use geometry_msgs.msg.Twist for velocity control
- Use sensor_msgs.msg.LaserScan for lidar
- Use nav_msgs.msg.Odometry for odometry
- Use ROS2-compatible imports only
- Use ROS2 node architecture when appropriate
- Use timers instead of blocking loops
- Programs should run autonomously

"""

    return """

PYTHON AUTONOMOUS SYSTEM RULES:
- Prefer modular Python architecture
- Avoid unnecessary external dependencies
- Avoid interactive input()
- Programs should execute autonomously
- Use clean separation of concerns
- Avoid infinite blocking loops

"""


def generate_file(
    file_name,
    user_prompt,
    project_context,
    existing_file_content,
    action
):

    capability_rules = build_capability_rules(
        user_prompt
    )

    prompt = f"""
You are an expert autonomous systems engineer.

You are working on an EXISTING project.

TASK TYPE:
{action}

FILE NAME:
{file_name}

STRICT RULES:
- Output ONLY executable file contents
- Do NOT explain anything
- Do NOT add markdown
- Do NOT add notes
- Do NOT add descriptions
- Do NOT add triple backticks
- Your response will be written directly into a file
- Any extra text will break the system
- Preserve architectural consistency
- Do not hallucinate imports
- Only import files that exist in the provided project context

{capability_rules}

EXISTING PROJECT FILES:
{project_context}

EXISTING FILE CONTENT:
{existing_file_content}

USER REQUEST:
{user_prompt}
"""

    ollama_response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    response_data = ollama_response.json()

    workspace_code = response_data["response"]

    return clean_workspace_code(
        workspace_code
    )


def repair_code(
    file_name,
    broken_code,
    error_message
):

    repair_prompt = f"""
You are fixing Python syntax issues.

FILE:
{file_name}

ERROR:
{error_message}

BROKEN CODE:
{broken_code}

RULES:
- Return ONLY corrected executable code
- No explanations
- No markdown
- No triple backticks
- Preserve original functionality
"""

    ollama_response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL_NAME,
            "prompt": repair_prompt,
            "stream": False
        }
    )

    response_data = ollama_response.json()

    repaired_code = response_data["response"]

    return clean_workspace_code(
        repaired_code
    )


def repair_runtime_error(
    file_name,
    broken_code,
    runtime_error
):

    repair_prompt = f"""
You are fixing a Python runtime error.

FILE:
{file_name}

RUNTIME ERROR:
{runtime_error}

BROKEN CODE:
{broken_code}

TASK:
Fix the runtime issue while preserving architecture.

STRICT RULES:
- Return ONLY corrected executable code
- No explanations
- No markdown
- No triple backticks
- Preserve existing architecture
- Do not hallucinate missing imports
"""

    ollama_response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL_NAME,
            "prompt": repair_prompt,
            "stream": False
        }
    )

    response_data = ollama_response.json()

    repaired_code = response_data["response"]

    return clean_workspace_code(
        repaired_code
    )


def summarize_file(
    file_name,
    file_content
):

    summary_prompt = f"""
You are analyzing a software system file.

FILE NAME:
{file_name}

FILE CONTENT:
{file_content}

TASK:
Summarize the purpose of this file in ONE sentence.

RULES:
- Be concise
- Focus on functionality
- No markdown
- No bullet points
"""

    ollama_response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL_NAME,
            "prompt": summary_prompt,
            "stream": False
        }
    )

    response_data = ollama_response.json()

    return response_data[
        "response"
    ].strip()


def modify_file(
    file_name,
    existing_content,
    user_prompt
):

    capability_rules = build_capability_rules(
        user_prompt
    )

    modify_prompt = f"""
You are modifying an EXISTING autonomous systems file.

FILE NAME:
{file_name}

EXISTING FILE CONTENT:
{existing_content}

USER REQUEST:
{user_prompt}

TASK:
Modify the existing file while preserving architecture.

STRICT RULES:
- Preserve working code
- Only make necessary modifications
- Do NOT remove unrelated functionality
- Maintain modular architecture
- Output ONLY executable code
- No markdown
- No explanations
- No hallucinated imports

{capability_rules}
"""

    ollama_response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL_NAME,
            "prompt": modify_prompt,
            "stream": False
        }
    )

    response_data = ollama_response.json()

    return clean_workspace_code(
        response_data["response"]
    )


def generate_architecture_reasoning(
    user_prompt,
    generation_plan
):

    reasoning_prompt = f"""
You are analyzing an autonomous systems engineering decision.

USER REQUEST:
{user_prompt}

GENERATION PLAN:
{generation_plan}

TASK:
Explain why these architectural decisions make sense.

RULES:
- One short paragraph
- Focus on modularity
- Mention separation of concerns if relevant
- No markdown
"""

    ollama_response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL_NAME,
            "prompt": reasoning_prompt,
            "stream": False
        }
    )

    response_data = ollama_response.json()

    return response_data[
        "response"
    ].strip()