import os
import ast
import json

from services.ai_services import (summarize_file)

from utils.project_manager import (
    get_project_path,
    get_project_index_path
)


def build_project_index(project_name):

    workspace_folder = get_project_path(
        project_name
    )

    project_index = {}

    for filename in os.listdir(
        workspace_folder
    ):

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

        if not os.path.isfile(file_path):

            continue

        try:

            with open(file_path, "r") as file:

                content = file.read()

            file_info = {
                "file_name": filename,
                "imports": [],
                "functions": [],
                "classes": [],
                "summary": "",
                "depends_on": []
            }

            if filename.endswith(".py"):

                tree = ast.parse(content)

                for node in ast.walk(tree):

                    # IMPORTS
                    if isinstance(
                        node,
                        ast.Import
                    ):

                        for alias in node.names:

                            file_info[
                                "imports"
                            ].append(
                                alias.name
                            )

                            possible_file = (
                                f"{alias.name}.py"
                            )

                            if possible_file in os.listdir(
                                workspace_folder
                            ):

                                file_info[
                                    "depends_on"
                                ].append(
                                    possible_file
                                )

                    # FROM IMPORTS
                    elif isinstance(
                        node,
                        ast.ImportFrom
                    ):

                        if node.module:

                            file_info[
                                "imports"
                            ].append(
                                node.module
                            )

                            possible_file = (
                                f"{node.module}.py"
                            )

                            if possible_file in os.listdir(
                                workspace_folder
                            ):

                                file_info[
                                    "depends_on"
                                ].append(
                                    possible_file
                                )

                    # FUNCTIONS
                    elif isinstance(
                        node,
                        ast.FunctionDef
                    ):

                        file_info[
                            "functions"
                        ].append(
                            node.name
                        )

                    # CLASSES
                    elif isinstance(
                        node,
                        ast.ClassDef
                    ):

                        file_info[
                            "classes"
                        ].append(
                            node.name
                        )

            summary = summarize_file(
                filename,
                content
            )

            file_info[
                "summary"
            ] = summary

            project_index[
                filename
            ] = file_info

        except Exception as e:

            print(
                f"Indexing failed for {filename}: {e}"
            )

    index_path = get_project_index_path(
        project_name
    )

    with open(index_path, "w") as file:

        json.dump(
            project_index,
            file,
            indent=4
        )

    return project_index