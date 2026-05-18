import subprocess


def install_dependency(package_name):

    try:

        result = subprocess.run(
            ["pip", "install", package_name],
            capture_output=True,
            text=True,
            timeout=120
        )

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except Exception as e:

        return {
            "success": False,
            "stdout": "",
            "stderr": str(e)
        }