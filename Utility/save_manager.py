import json
import os
from enum import Enum
import appdirs

APP_NAME = "MyBooks"
APP_AUTHOR = "Team2"

DIRS = {
    "app":appdirs.user_config_dir(APP_NAME,APP_AUTHOR),
    "log":appdirs.user_log_dir(APP_NAME,APP_AUTHOR),
    "user":appdirs.user_cache_dir(APP_NAME,APP_AUTHOR)
}

def save(save_dict,data_type="app"):
    if data_type not in DIRS:
        raise ValueError(f"Unknown data_type '{data_type}'. Use: {list(DIRS)}")
    
    path = DIRS[data_type]

    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except FileExistsError:
            print(f"Directory '{path}' already exists.")

    with open(f"{path}/{data_type}.txt","wt") as file:
        json_string = json.dumps(save_dict)
        print(json_string)
        file.write(json_string)

def load(data_type="app") -> dict:
    if data_type not in DIRS:
        raise ValueError(f"Unknown data_type '{data_type}'. Use: {list(DIRS)}")
    
    path = DIRS[data_type]

    if not os.path.exists(path):
        print("nothing to load")
        return None
    
    try:
        with open(f"{path}/{data_type}.txt","rt") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return None

if __name__ == "__main__":
    pass