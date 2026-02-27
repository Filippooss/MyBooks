import os, sys


def resource_path(relative_path: str) -> str:
    """
    Get the absolute path of a resource relative to the script's directory.
    """

    try:
        # Pysinstaller creates a temporary folder and stores path in _MEIPASS, also stores the executable in the same folder
        base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
