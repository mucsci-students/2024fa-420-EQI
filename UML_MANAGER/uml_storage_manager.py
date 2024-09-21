"""
Author : Quang Bui
Created: September 21, 2024

Description:
    This shell will manage the storages for all the data
    of the UML program including saving/loading

List of last date modified:


"""

################################################################
# IMPORTED MODULES #
import json
import os


################################################################
# Load all saved file names from the JSON file "NAME_LIST.json"
def load_name():
    file_path = "UML_UTILITY/SAVED_FILES/NAME_LIST.json"
    try:
        # Check if the file is empty
        if os.stat(file_path).st_size == 0:
            return []
        # Load data from the JSON file
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        # Handle the case where the file is not found
        print(f"File {file_path} not found.")
        return None
    except json.JSONDecodeError:
        # Handle JSON decoding errors (e.g., if the file is not in proper JSON format)
        print(f"Error decoding JSON from {file_path}.")
        return None


# Update the global data variables after loading from a saved file
def update_data(new_data_list: list):
    # Declare global variables that will be updated
    global data_list, class_list, class_and_attr_list, relationship_list
    # Update the global data list with the new data
    data_list = new_data_list
    # Extract the class and attribute list from the new data
    class_and_attr_list = data_list[0]
    # Extract the relationship list from the new data
    relationship_list = data_list[1]
    # Clear the class list before repopulating it
    class_list.clear()
    # Loop through the class and attribute list and extract class names into the class list
    for dictionary in class_and_attr_list:
        class_list.append(dictionary["class_name"])


# Save the current data to a JSON file
def save_data_to_json(file_name: str, is_clear: bool = False):
    file_path = f"UML_UTILITY/SAVED_FILES/{file_name}.json"
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            # If the file doesn't exist, create it and write the data list
            with open(file_path, "w") as json_file:
                json.dump(data_list, json_file, indent=4)
                print("Successfully saved data!")
                return
        # If the file exists and the file name is in the saved list, update the data
        for dictionary in saved_file_name_list:
            if file_name in dictionary:
                # Open the file and load its current data
                with open(file_path, "r") as file:
                    data = json.load(file)
                    # Overwrite the loaded data with the current data list
                    data = data_list
                # Save the updated data to the file
                with open(file_path, "w") as file:
                    json.dump(data, file, indent=4)
                if not is_clear:
                    print("Successfully saved data!")
    except json.JSONDecodeError:
        # Handle JSON decoding errors (e.g., if the file is not in proper JSON format)
        print(f"Error decoding JSON from {file_path}.")
        return None


# Load data from the specified JSON file
def load_data_from_json(file_name: str):
    file_path = f"UML_UTILITY/SAVED_FILES/{file_name}.json"
    try:
        # Open the file and load the data from JSON
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        # Handle the case where the file is not found
        print(f"File {file_path} not found.")
        return None
    except json.JSONDecodeError:
        # Handle JSON decoding errors (e.g., if the file is not in proper JSON format)
        print(f"Error decoding JSON from {file_path}.")
        return None


# Save the list of file names to the "NAME_LIST.json" file
def save_name_list(name_list: list[str]):
    file_path = "UML_UTILITY/SAVED_FILES/NAME_LIST.json"
    try:
        # Open the file and save the name list in JSON format
        with open(file_path, "w") as file:
            json.dump(name_list, file, indent=4)
    except FileNotFoundError:
        # Handle the case where the file is not found
        print(f"File {file_path} not found.")
        return None
    except json.JSONDecodeError:
        # Handle JSON decoding errors (e.g., if the file is not in proper JSON format)
        print(f"Error decoding JSON from {file_path}.")
        return None


# LOADING SAVED FILE'S NAMES FROM JSON FILE TO GLOBAL LIST #
saved_file_name_list = load_name()
# LOADING DATA FROM JSON FILE TO GLOBAL DICTIONARY #
data_list = [[], []]
# Create a class so that we can display it or sort it alphabetically easily
class_list: list[str] = []
# Get list of classes and its attributes
class_and_attr_list = data_list[0]
# Get list of relationships
relationship_list = data_list[1]
# Add class name to class_list
for dictionary in class_and_attr_list:
    class_list.append(dictionary["class_name"])
