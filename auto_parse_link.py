import os
import pprint
from pathlib import Path

def getFileName(base_dir: str, url: str):
    """
    Retrieves a list of file name from a given base directory and parse url path.

    Args:
        base_dir (str): The base directory to search for images.

    Returns:
        list: A list of file name found in the base directory.

    Notes:
        This function uses the `os` module to walk the directory tree and find file files.
        It returns a list of file name, where each path is a string representing the full path to an file.
    """
    directory = os.walk(base_dir)
   
    # Initialize an empty list to store file name
    fileLists = []
    count = 0
    # Walk the directory tree starting from the base directory
    for path, subdirs, files in directory:
        # Iterate over each file in the current directory
        for file in files:
            # count += 1
            file_path = Path(file)
            # Construct the url + file name to the file
            # sampleDict = {
            #     "title": f"{file_path.stem.split("-")[0]}",
            #     "path": f"{url + "/" + file_path.stem}",
            #     "icon": "cog",
            #     "external": True
            # }
            parsePath = url + "/" + file_path.stem # parsePath = url + "/" + file
            # Add the file path to list
            if (file_path.stem != "index"):
                # fileLists.append(parsePath)
                fileLists.append({
                "title": f"{file_path.stem.split("-")[0]}",
                "path": f"{url + "/" + file_path.stem}",
                "icon": "cog",
                "external": True
            })

        
    return pprint.pformat(fileLists, indent=2)

print(getFileName("./docs", "/snippets"))