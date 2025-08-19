import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    try:
        # Resolve absolute paths
        working_directory = os.path.abspath(working_directory)
        complete_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Prevent directory traversal
        if os.path.commonpath([working_directory, complete_file_path]) != working_directory:
            raise ValueError(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')

        # Check if the file exists and is a Python file
        if not os.path.exists(complete_file_path):
            raise FileNotFoundError(f'Error: File "{file_path}" not found.')
        if not file_path.endswith('.py'):
            raise ValueError(f'Error: "{file_path}" is not a Python file')

        # Build the command
        command = ["python", complete_file_path] + args

        # Run the command
        result = subprocess.run(command, cwd=working_directory, timeout=30, capture_output=True, text=True)

        # Check result
        if result.returncode == 0:
            print(f'Successfully executed "{file_path}"')
            print(f'STDOUT: {result.stdout}')
            return result.stdout
        else:
            print(f'Error executing "{file_path}"')
            print(f'STDERR: {result.stderr}')
            return result.stderr

    except ValueError as ve:
        print(ve)
    except FileNotFoundError as fnfe:
        print(fnfe)
    except Exception as e:
        print(f"Error: executing Python file: {e}")
    return False
