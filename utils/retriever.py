import json

from utils.project_manager import (
    get_project_index_path
)


def retrieve_relevant_files(
    user_prompt,
    project_name
):

    try:

        index_path = get_project_index_path(
            project_name
        )

        with open(index_path, "r") as file:

            project_index = json.load(file)

    except Exception:

        return []

    prompt_words = (
        user_prompt
        .lower()
        .split()
    )

    scored_files = []

    for filename, metadata in (
        project_index.items()
    ):

        score = 0

        searchable_text = " ".join([

            filename,

            " ".join(
                metadata["imports"]
            ),

            " ".join(
                metadata["functions"]
            ),

            " ".join(
                metadata["classes"]
            ),

            metadata.get(
                "summary",
                ""
            )

        ]).lower()

        for word in prompt_words:

            if word in searchable_text:

                score += 2

        for imported_module in metadata[
            "imports"
        ]:

            if imported_module.lower() in (
                user_prompt.lower()
            ):

                score += 3
            
            if word in filename.lower():

                score += 5

        scored_files.append({
            "file": filename,
            "score": score
        })

    scored_files.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    top_files = [

        item

        for item in scored_files

        if item["score"] > 0

    ][:3]

    expanded_files = set()

    for item in top_files:

        file_name = item["file"]

        expanded_files.add(
            file_name
        )

        dependencies = project_index[
            file_name
        ].get(
            "depends_on",
            []
        )

        for dependency in dependencies:

            expanded_files.add(
                dependency
            )

    return list(expanded_files)