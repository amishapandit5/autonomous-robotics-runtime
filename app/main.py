from fastapi import FastAPI
from pydantic import BaseModel
import ast

from services.ai_services import (
    generate_file,
    repair_code,
    repair_runtime_error,
    modify_file,
    generate_architecture_reasoning
)

from utils.memory import (
    build_project_context
)

from utils.project_manager import (
    create_project
)

from services.planner_services import (
    create_generation_plan
)

from services.docker_executor import (
    execute_in_docker
)

from utils.dependency_installer import (
    install_dependency
)

from utils.dependency_classifier import (
    classify_dependency
)

from utils.project_indexer import (
    build_project_index
)

from utils.retriever import (
    retrieve_relevant_files
)

from utils.adr_manager import (
    save_architecture_decision
)

app = FastAPI()


class PromptRequest(BaseModel):

    project: str
    prompt: str


@app.get("/")
def home():

    return {
        "message": "RoboCursor backend is running"
    }


def is_valid_python(code):

    try:

        ast.parse(code)

        return True

    except Exception:

        return False


@app.post("/generate")
def generate_code(request: PromptRequest):

    project_name = request.project

    project_path = create_project(
        project_name
    )

    created_files = []

    # RETRIEVAL
    relevant_files = retrieve_relevant_files(
        request.prompt,
        project_name
    )

    print(
        "Relevant files:",
        relevant_files
    )

    # PROJECT CONTEXT
    project_context = build_project_context(
        relevant_files,
        project_name
    )

    # PLANNING
    generation_plan = create_generation_plan(
        request.prompt,
        project_context,
        relevant_files
    )

    print(generation_plan)

    # ARCHITECTURE REASONING
    architecture_reasoning = (
        generate_architecture_reasoning(
            request.prompt,
            generation_plan
        )
    )

    save_architecture_decision(
        project_name,
        request.prompt,
        generation_plan,
        architecture_reasoning
    )

    # EXECUTION LOOP
    for step in generation_plan:

        file_name = step["file"]

        action = step["action"]

        print(
            f"Executing {action} on {file_name}"
        )

        file_path = (
            f"{project_path}/{file_name}"
        )

        generated_code = ""

        # MODIFY FLOW
        if action == "modify":

            try:

                with open(file_path, "r") as file:

                    existing_code = file.read()

                generated_code = modify_file(
                    file_name,
                    existing_code,
                    request.prompt
                )

            except FileNotFoundError:

                print(
                    f"{file_name} not found. Switching to create mode."
                )

                action = "create"

        # CREATE FLOW
        if action == "create":

            generated_code = generate_file(
                file_name,
                request.prompt,
                project_context,
                "",
                action
            )

        # PYTHON VALIDATION
        if file_name.endswith(".py"):

            if not is_valid_python(
                generated_code
            ):

                print(
                    f"Repairing syntax for {file_name}"
                )

                generated_code = repair_code(
                    file_name,
                    generated_code,
                    "Invalid Python syntax"
                )

        # SAVE FILE
        with open(file_path, "w") as file:

            file.write(generated_code)

        execution_result = None

        # DOCKER EXECUTION
        if file_name.endswith(".py"):

            execution_result = execute_in_docker(
                project_name,
                file_name
            )

            print(execution_result)

            runtime_error = execution_result[
                "stderr"
            ]

            # DEPENDENCY HANDLING
            if "ModuleNotFoundError" in runtime_error:

                try:

                    missing_package = runtime_error.split(
                        "No module named "
                    )[1]

                    missing_package = (
                        missing_package
                        .replace("'", "")
                        .replace('"', "")
                        .strip()
                    )

                    dependency_type = classify_dependency(
                        missing_package
                    )

                    print(
                        f"Dependency type: {dependency_type}"
                    )

                    # PIP PACKAGE
                    if dependency_type == "pip":

                        print(
                            f"Installing pip dependency: {missing_package}"
                        )

                        install_result = install_dependency(
                            missing_package
                        )

                        print(install_result)

                        execution_result = (
                            execute_in_docker(
                                project_name,
                                file_name
                            )
                        )

                    # ROS PACKAGE
                    elif dependency_type == "ros":

                        print(
                            f"{missing_package} is a ROS dependency."
                        )

                        print(
                            "ROS dependency already handled by Docker image."
                        )

                    # BUILT-IN PACKAGE
                    elif dependency_type == "built_in":

                        print(
                            f"{missing_package} is built-in."
                        )

                    # UNKNOWN PACKAGE
                    elif dependency_type == "unknown":

                        print(
                            f"Unknown dependency: {missing_package}"
                        )

                except Exception as e:

                    print(
                        f"Dependency classification failed: {e}"
                    )

            # RUNTIME REPAIR LOOP
            max_retries = 3

            retry_count = 0

            while (

                not execution_result["success"]

                and

                retry_count < max_retries
            ):

                print(
                    f"Runtime repair attempt {retry_count + 1}"
                )

                generated_code = repair_runtime_error(

                    file_name,

                    generated_code,

                    execution_result["stderr"]
                )

                with open(file_path, "w") as file:

                    file.write(generated_code)

                execution_result = execute_in_docker(

                    project_name,

                    file_name
                )

                print(
                    "AFTER RUNTIME REPAIR:"
                )

                print(execution_result)

                retry_count += 1

        created_files.append(file_path)

    # PROJECT INDEXING
    project_index = build_project_index(
        project_name
    )

    print(project_index)

    return {

        "message": "Files created successfully",

        "files": created_files
    }