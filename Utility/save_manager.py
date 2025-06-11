import json
import os
from enum import Enum
import appdirs
import tempfile

APP_NAME = "MyBooks"
APP_AUTHOR = "Team2"

DIRS = {
    "app":appdirs.user_config_dir(APP_NAME,APP_AUTHOR),
    "log":appdirs.user_log_dir(APP_NAME,APP_AUTHOR),
    "user":appdirs.user_cache_dir(APP_NAME,APP_AUTHOR)
}
temp_file_paths:dict = dict()

def save(save_dict:dict, data_type:str = "app"):
    """
    save_dict : ena dictionary me tis plirofories gia apothikeusi
    data_type : o tipos tou save(app , log , user)
    """
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

#https://stackoverflow.com/questions/8577137/how-can-i-create-a-tmp-file-in-python
def write_temp_file(data:dict,file_key):
    #print(tempfile.gettempdir())
    temp_file = tempfile.NamedTemporaryFile(mode="wt",delete=False,prefix=APP_NAME)
    temp_file.write(json.dumps(data))
    temp_file.close()
    temp_file_paths[file_key] = temp_file.name

def load(data_type="app") -> dict:
    if data_type not in DIRS:
        raise ValueError(f"Unknown data_type '{data_type}'. Use: {list(DIRS)}")

    path = DIRS[data_type]

    if not os.path.exists(path):
        print("nothing to load")
        return dict()

    try:
        with open(f"{path}/{data_type}.txt","rt") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return dict()

def read_temp_file(file_key:str,delete_file:bool = True) -> dict:
    try:
        with open(temp_file_paths[file_key],mode="rt") as file:

            data = json.load(file)
        if delete_file:
            os.remove(temp_file_paths[file_key])
        return data

    except FileNotFoundError:
        print("File not found")
        return dict()
    except KeyError:
        print("Key not found")
        return dict()

if __name__ == "__main__":
    #debug
    write_temp_file({"test":"test"},"test")

    result = read_temp_file("test")
    print(f"{result}")
