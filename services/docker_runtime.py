import subprocess

from utils.config import (
    WORKSPACE_PATH
)

CONTAINER_NAME = (
    "robocursor-runtime"
)

IMAGE_NAME = (
    "robocursor-runtime"
)


def ensure_runtime_container():

    inspect_command = [

        "docker",
        "inspect",

        "-f",
        "{{.State.Running}}",

        CONTAINER_NAME
    ]

    inspect_result = subprocess.run(
        inspect_command,
        capture_output=True,
        text=True
    )

    # CONTAINER ALREADY RUNNING
    if (
        inspect_result.returncode == 0
        and
        inspect_result.stdout.strip() == "true"
    ):

        return

    # CONTAINER EXISTS BUT STOPPED
    check_command = [

        "docker",
        "ps",
        "-a",

        "--filter",
        f"name={CONTAINER_NAME}",

        "--format",
        "{{.Names}}"
    ]

    check_result = subprocess.run(
        check_command,
        capture_output=True,
        text=True
    )

    existing_container = (
        check_result.stdout.strip()
    )

    if existing_container == CONTAINER_NAME:

        print(
            "Starting existing runtime container..."
        )

        start_command = [

            "docker",
            "start",

            CONTAINER_NAME
        ]

        subprocess.run(start_command)

        return

    # CREATE NEW CONTAINER
    print(
        "Creating new runtime container..."
    )

    create_command = [

        "docker",
        "run",

        "-dit",

        "--name",
        CONTAINER_NAME,

        "-v",
        f"{WORKSPACE_PATH}:/workspace",

        IMAGE_NAME,

        "bash"
    ]

    subprocess.run(create_command)