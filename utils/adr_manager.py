import json
import os

from datetime import datetime

from utils.project_manager import (
    get_architecture_path
)


def save_architecture_decision(
    project_name,
    user_prompt,
    generation_plan,
    reasoning
):

    adr_file = get_architecture_path(
        project_name
    )

    decision = {

        "timestamp": str(
            datetime.now()
        ),

        "user_prompt": user_prompt,

        "generation_plan": generation_plan,

        "reasoning": reasoning
    }

    existing_decisions = []

    if os.path.exists(
        adr_file
    ):

        try:

            with open(
                adr_file,
                "r"
            ) as file:

                existing_decisions = (
                    json.load(file)
                )

        except Exception:

            existing_decisions = []

    existing_decisions.append(
        decision
    )

    with open(
        adr_file,
        "w"
    ) as file:

        json.dump(
            existing_decisions,
            file,
            indent=4
        )