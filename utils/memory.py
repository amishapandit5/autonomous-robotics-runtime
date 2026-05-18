import os

from utils.project_manager import (
    get_project_path
)


def build_project_context(
    relevant_files=None,
    project_name=None
):

    context = ""

    if project_name is None:

        return context

    workspace_folder = get_project_path(
        project_name
    )

    if not os.path.exists(
        workspace_folder
    ):

        return context

    for filename in os.listdir(
        workspace_folder
    ):

        if relevant_files is not None:

            if filename not in relevant_files:

                continue

        if filename.startswith("."):

            continue

        if filename == "project_index.json":

            continue

        if filename == "architecture_decisions.json":

            continue

        file_path = os.path.join(
            workspace_folder,
            filename
        )

        if not os.path.isfile(
            file_path
        ):

            continue

        try:

            with open(file_path, "r") as file:

                content = file.read()

            context += f"""

FILE: {filename}

CONTENT:
{content}

"""

        except Exception as e:

            print(
                f"Context loading failed for {filename}: {e}"
            )

    return context