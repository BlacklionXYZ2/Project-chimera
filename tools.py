import subprocess
import sys
from pathlib import Path

WORKSPACE_DIR = Path(r"f:\GitHub\projects\Chimera\workspace")
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

def _sanitize_path(filename: str) -> Path:
    target_path = (WORKSPACE_DIR / filename).resolve()
    if not str(target_path).startswith(str(WORKSPACE_DIR.resolve())):
        raise PermissionError(f"Access denied: '{filename}' is outside workspace bounds.")
    return target_path

def write_workspace_file(filename: str, content: str) -> str:
    """Saves code/config text directly to disk inside the workspace directory."""
    try:
        target_path = _sanitize_path(filename)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to '{filename}'."
    except Exception as e:
        return f"Error writing file '{filename}': {str(e)}"

def read_workspace_file(filename: str) -> str:
    """Reads full text content of a file from the workspace."""
    try:
        target_path = _sanitize_path(filename)
        if not target_path.exists():
            return f"Error: File '{filename}' does not exist in workspace."
        with open(target_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file '{filename}': {str(e)}"

def run_python_script(filename: str, timeout: int = 10) -> str:
    """Executes a Python script from workspace in a subprocess and captures output."""
    try:
        target_path = _sanitize_path(filename)
        if not target_path.exists():
            return f"Error: Cannot execute '{filename}'. File not found."

        result = subprocess.run(
            [sys.executable, str(target_path)],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(WORKSPACE_DIR)
        )

        output = []
        if result.stdout.strip():
            output.append(f"--- STDOUT ---\n{result.stdout.strip()}")
        if result.stderr.strip():
            output.append(f"--- STDERR ---\n{result.stderr.strip()}")
        output.append(f"--- Exit Code: {result.returncode} ---")
        return "\n".join(output)

    except subprocess.TimeoutExpired:
        return f"Execution Error: '{filename}' timed out after {timeout} seconds."
    except Exception as e:
        return f"Execution Error on '{filename}': {str(e)}"