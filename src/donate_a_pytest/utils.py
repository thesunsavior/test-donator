import os


def find_paths_with_substring(
    directory: str,
    substring: str,
    file_extension: str = None,
    exclude_substring: str = None,
) -> list:
    """
    Walk through a directory and collect paths that contain a particular substring in their name.

    Args:
        directory (str): The directory to search in
        substring (str): The substring to look for in file/directory names
        file_extension (str, optional): If provided, only return files with this extension

    Returns:
        list: A list of paths (as strings) that contain the substring
    """
    matching_paths = []

    for root, _, files in os.walk(directory):
        # Check files
        for file in files:
            if substring in file:
                # If file_extension is specified, check if the file has that extension
                if file_extension is not None:
                    if not file.endswith(file_extension):
                        continue

                if exclude_substring is not None:
                    if exclude_substring in file:
                        continue

                full_path = os.path.join(root, file)
                matching_paths.append(full_path)

        # Optionally, you can also check directory names
        # for dir_name in dirs:
        #     if substring in dir_name:
        #         full_path = os.path.join(root, dir_name)
        #         matching_paths.append(full_path)

    return matching_paths
