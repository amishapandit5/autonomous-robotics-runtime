import requests
import ast

from utils.cleaner import (
    clean_planner_output
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


def build_architecture_mode(
    user_prompt
):

    if is_ros_request(user_prompt):

        return """

SYSTEM TYPE:
ROS2 Robotics System

PLANNING RULES:
- Prefer ROS2 node architecture
- Prefer modular robotics separation
- Use dedicated files for sensors, navigation, planning, and coordination
- Prefer modifying existing robotics files when possible
- Avoid ROS1 architecture
"""

    return """

SYSTEM TYPE:
Autonomous Python System

PLANNING RULES:
- Prefer modular Python architecture
- Use clean separation of concerns
- Avoid unnecessary file creation
- Prefer modifying existing files when possible
"""


def create_generation_plan(
    user_prompt,
    project_context,
    relevant_files
):

    architecture_mode = (
        build_architecture_mode(
            user_prompt
        )
    )

    planning_prompt = f"""
You are a senior autonomous systems architect.

Analyze the user's request.

Determine which files should be:
- created
- modified

Return ONLY a valid Python list of dictionaries.

VALID EXAMPLE:

[
    {{
        "file": "launch.py",
        "action": "modify"
    }},
    {{
        "file": "lidar_node.py",
        "action": "create"
    }}
]

STRICT RULES:
- action must ONLY be:
create
modify

- Return ONLY raw Python list
- No markdown
- No explanations
- No triple backticks
- Do not wrap response in json
- Do not generate invalid syntax
- Prefer modifying existing files when possible
- Create new files only when necessary
- Multiple coordinated file modifications are allowed
- Do not hallucinate unrelated files
- Prefer architectural consistency

{architecture_mode}

RELEVANT FILES:
{relevant_files}

EXISTING PROJECT:
{project_context}

USER REQUEST:
{user_prompt}
"""

    ollama_response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL_NAME,
            "prompt": planning_prompt,
            "stream": False
        }
    )

    response_data = ollama_response.json()

    raw_plan = response_data[
        "response"
    ]

    cleaned_plan = clean_planner_output(
        raw_plan
    )

    try:

        parsed_plan = ast.literal_eval(
            cleaned_plan
        )

        # VALIDATE STRUCTURE
        validated_plan = []

        for step in parsed_plan:

            if not isinstance(
                step,
                dict
            ):

                continue

            if (
                "file" not in step
                or
                "action" not in step
            ):

                continue

            if step["action"] not in [
                "create",
                "modify"
            ]:

                continue

            validated_plan.append({
                "file": step["file"],
                "action": step["action"]
            })

        return validated_plan

    except Exception as e:

        print(
            "PLANNER PARSE ERROR:"
        )

        print(e)

        print(
            "RAW PLANNER OUTPUT:"
        )

        print(raw_plan)

        return []