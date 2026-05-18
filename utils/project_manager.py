from pathlib import Path

CURRENT_FILE = Path(
    __file__
).resolve()

PROJECT_ROOT = (
    CURRENT_FILE.parent.parent.parent
)

BASE_WORKSPACE = (
    PROJECT_ROOT
    / "robo-workspace"
)


def sanitize_project_name(
    project_name
):

    return (
        project_name
        .replace("/", "_")
        .replace("\\", "_")
        .replace("..", "_")
        .strip()
    )


def create_project(
    project_name
):

    safe_project_name = (
        sanitize_project_name(
            project_name
        )
    )

    project_path = (
        BASE_WORKSPACE
        / safe_project_name
    )

    project_path.mkdir(
        parents=True,
        exist_ok=True
    )

    return str(project_path)


def get_project_path(
    project_name
):

    safe_project_name = (
        sanitize_project_name(
            project_name
        )
    )

    return str(
        BASE_WORKSPACE
        / safe_project_name
    )


def get_project_index_path(
    project_name
):

    return str(

        Path(
            get_project_path(
                project_name
            )
        )

        / "project_index.json"
    )


def get_architecture_path(
    project_name
):

    return str(

        Path(
            get_project_path(
                project_name
            )
        )

        / "architecture_decisions.json"
    )