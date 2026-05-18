
def clean_workspace_code(code):

    code = (
        code
        .replace("```python", "")
        .replace("```Python", "")
        .replace("```py", "")
        .replace("```json", "")
        .replace("```JSON", "")
        .replace("```", "")
        .replace("'''python", "")
        .replace("'''", "")
        .strip()
    )

    lines = code.split("\n")

    cleaned_lines = []

    previous_line_empty = False

    for line in lines:

        stripped_line = line.rstrip()

        # SKIP EXPLANATION-LIKE TEXT
        if stripped_line.startswith(
            "Here is"
        ):

            continue

        if stripped_line.startswith(
            "Explanation:"
        ):

            continue

        # REMOVE EXCESS EMPTY LINES
        if stripped_line == "":

            if previous_line_empty:

                continue

            previous_line_empty = True

        else:

            previous_line_empty = False

        cleaned_lines.append(
            stripped_line
        )

    return "\n".join(
        cleaned_lines
    ).strip()


def clean_planner_output(text):

    text = (
        text
        .replace("```python", "")
        .replace("```Python", "")
        .replace("```py", "")
        .replace("```json", "")
        .replace("```JSON", "")
        .replace("``` json", "")
        .replace("```", "")
        .strip()
    )

    return text