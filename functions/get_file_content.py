import os

def get_file_content(working_directory, file_path):
    try:
        # Resolve absolute paths
        working_directory = os.path.abspath(working_directory)
        file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Check that the path starts with the working directory (prevent traversal)
        if os.path.commonpath([working_directory, file_path]) != working_directory:
            raise ValueError("Error: Directory traversal is not allowed")

        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'Error: File "{file_path}" does not exist')

        # Read and return the file content
        with open(file_path, 'r') as file:
            content = file.read(10000)
        print(content)
        return content

    except ValueError as ve:
        print(ve)
    except FileNotFoundError as fnfe:
        print(fnfe)
    except Exception as e:
        print(f"Error: {e}")