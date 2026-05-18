from pathlib import Path

CURRENT_FILE = Path(
    __file__
).resolve()

PROJECT_ROOT = (
    CURRENT_FILE.parent.parent
)

WORKSPACE_PATH = str(
    PROJECT_ROOT
    / "robo-workspace"
)