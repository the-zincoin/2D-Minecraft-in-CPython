from pathlib import Path

def find_file_in_directory(file_name, directory):
    directory_path = Path(directory)
    for file in directory_path.rglob('.'):  # Searches recursively
        return file.resolve()
    return None

