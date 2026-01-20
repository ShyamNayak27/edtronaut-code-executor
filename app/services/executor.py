import subprocess
import sys
import time
import io
from contextlib import redirect_stdout, redirect_stderr

def execute_python_code(code: str, timeout: int = 5):
    """
    Executes a string of Python code and returns the results.
    We use a subprocess to ensure that 'exit()' or 'infinite loops' 
    don't crash our main server.
    """
    start_time = time.time()
    
    try:
        # We run the code using the same python interpreter currently running
        # 'timeout' ensures the requirement 'Enforce Time limits' is met
        process = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        return {
            "status": "COMPLETED",
            "stdout": process.stdout,
            "stderr": process.stderr,
            "execution_time_ms": execution_time_ms
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "TIMEOUT",
            "stdout": "",
            "stderr": f"Error: Execution exceeded {timeout} seconds.",
            "execution_time_ms": timeout * 1000
        }
    except Exception as e:
        return {
            "status": "FAILED",
            "stdout": "",
            "stderr": str(e),
            "execution_time_ms": 0
        }