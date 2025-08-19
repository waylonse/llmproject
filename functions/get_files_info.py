import os

def get_files_info(working_directory, directory="."):
    try:
        # Resolve absolute paths
        working_directory = os.path.abspath(working_directory)
        the_path = os.path.abspath(os.path.join(working_directory, directory))

        # Check that the path starts with the working directory (prevent traversal)
        if os.path.commonpath([working_directory, the_path]) != working_directory:
            raise ValueError("Error: Directory traversal is not allowed")

        # Check if the path exists and is a directory
        if not os.path.exists(the_path):
            raise FileNotFoundError(f'Error: Directory "{directory}" does not exist')
        if not os.path.isdir(the_path):
            raise NotADirectoryError(f'Error: "{directory}" is not a directory')

        # List files and gather file information
        file_info = []
        for file_name in os.listdir(the_path):
            file_path = os.path.join(the_path, file_name)
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            file_info.append(f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}")

        for entry in file_info:
            print(entry)

        return file_info

    except ValueError as ve:
        print(ve)
    except FileNotFoundError as fnfe:
        print(fnfe)
    except NotADirectoryError as nde:
        print(nde)
    except Exception as e:
        print(f"Unexpected error: {e}")
