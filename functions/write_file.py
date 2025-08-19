import os

def write_file(working_directory, file_path, content):
    try:
        # Resolve absolute paths
        working_directory = os.path.abspath(working_directory)
        file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Check that the path starts with the working directory (prevent traversal)
        if os.path.commonpath([working_directory, file_path]) != working_directory:
            raise ValueError("Error: Directory traversal is not allowed")

        # Ensure the directory exists
        dir_name = os.path.dirname(file_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        # Write content to the file
        with open(file_path, 'w') as file:
            file.write(content)
        
        print(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"Error: {e}")
    return False