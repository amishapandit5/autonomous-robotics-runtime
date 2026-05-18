import subprocess

from services.docker_runtime import (
    ensure_runtime_container
)


def execute_in_docker(
    project_name,
    file_name
):

    ensure_runtime_container()

    print(
        f"Running {file_name} inside project {project_name}"
    )

    command = [

        "docker",
        "exec",

        "robocursor-runtime",

        "bash",
        "-c",

        (
            "source /opt/ros/humble/setup.bash && "
            f"python3 -u /workspace/{project_name}/{file_name}"
        )
    ]

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=20
        )

        return {

            "success": (
                result.returncode == 0
            ),

            "stdout": result.stdout,

            "stderr": result.stderr
        }

    except subprocess.TimeoutExpired:

        return {

            "success": True,

            "stdout": (
                "Execution timed out safely."
            ),

            "stderr": ""
        }