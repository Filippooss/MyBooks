import os ,sys


def resource_path(relative_path):
    """
    Get the absolute path of a resource relative to the script's directory.
    """

    try:
        #Pysinstaller creates a temporary folder and stores path in _MEIPASS, also stores the executable in the same folder
        base_path =sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
