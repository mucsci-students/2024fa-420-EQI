################################################################
#   Author : Quang Bui
#   Created: September 12, 2024
#
#   This file is for the save/load features
################################################################

import json


# Save data to the JSON file
def save_data_from_json(data: dict[str, list[str]], file_path: str):
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}.")
        return None


# Load data from the JSON file
def load_data_from_json(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}.")
        return None
