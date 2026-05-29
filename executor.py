import subprocess
import tempfile
import os

def execute_python(code):

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".py",
            mode="w",
            encoding="utf-8"
        ) as temp:

            temp.write(code)

            temp_path = temp.name

        result = subprocess.run(
            ["python", temp_path],
            capture_output=True,
            text=True,
            timeout=5
        )

        os.unlink(temp_path)

        return {
            "output": result.stdout,
            "error": result.stderr
        }

    except subprocess.TimeoutExpired:

        return {
            "output": "",
            "error": "Execution timed out. Possible infinite loop detected."
        }

    except Exception as e:

        return {
            "output": "",
            "error": str(e)
        }