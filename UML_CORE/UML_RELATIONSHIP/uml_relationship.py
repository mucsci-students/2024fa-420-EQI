import UML_UTILITY.SAVE_LOAD.save_load as SAVE_LOAD
from UML_UTILITY.FORMAT_CHECKING.validators import check_format

"""
Author : Israel Gonzalez
Created: September 12, 2024
Version: 1.0

Description: 
This script manages relationships between classes by allowing you to add or remove relationships. 
It loads data from a JSON file to keep track of existing relationships and validates class names 
for correctness and existence.

"""
################################################################################

# LOADING DATA FROM JSON FILE TO GLOBAL DICTIONARY #
data_list = SAVE_LOAD.load_data_from_json("data.json")

# Initialize relationships list with proper error handling
if data_list and len(data_list) == 2:
    classes, relationships = data_list
else:
    classes = []
    relationships = []

################################################################################

def add_relationship(source: str, dest: str, relation: str):

    # Check if both source and dest classes exist
    if not check_class_name(source, should_exist=True) or not check_class_name(dest, should_exist=True):
        print("One or both classes do not exist. Relationship not added.")
        return

    
    # Check if the relationship already exists
    if any(rel for rel in relationships if rel["source"] == source and rel["dest"] == dest):
        print(f"Relationship between '{source}' and '{dest}' already exists!")
        return
    
    # Add the new relationship to the list
    relationships.append({"source": source, "dest": dest, "relation": relation})
    print(f"Added relationship from '{source}' to '{dest}' of type '{relation}'.")


def remove_relationship(source: str, dest: str):
    # Check if both source and destination classes exist
    if not check_class_name(source, should_exist=True) or not check_class_name(dest, should_exist=True):
        print("One or both classes do not exist. Relationship not removed.")
        return
    
     # Remove the relationship from the list if it exists
    global relationships
    relationships = [rel for rel in relationships if not (rel["source"] == source and rel["dest"] == dest)]
    print(f"Removed relationship from '{source}' to '{dest}'.")


################################################################################
# CHECKING CLASS NAME #

def validate_class_name(class_name: str) -> bool:

    data_list = SAVE_LOAD.load_data_from_json("data.json")

    class_and_attr_list = data_list[0]

    for dictionary in class_and_attr_list:
        if dictionary["class_name"] == class_name:
            return True
        
    return False

def check_class_name(class_name: str, should_exist: bool) -> bool:

    is_format_correct = check_format(class_name)

    if is_format_correct != "Valid input":
        return False
    is_name_exist = validate_class_name(class_name)

    if should_exist and not is_name_exist:
        print(f"Class '{class_name}' not found!")
        return False
    
    return True
