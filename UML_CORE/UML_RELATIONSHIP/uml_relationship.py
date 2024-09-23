import UML_MANAGER.uml_storage_manager as UML_STORAGE_MANAGER
from UML_UTILITY.FORMAT_CHECKING.validators import check_format

"""
Author : Israel Gonzalez
Created: September 12, 2024
Version: 1.1

Description: 
This script manages relationships between classes by allowing you to add or remove relationships. 
It loads data from a JSON file to keep track of existing relationships and validates class names 
for correctness and existence.

List of last date modified:
- September 15, 2024 (By Quang)

"""
################################################################################

# GET DATA FROM JSON FILE #
data_list = UML_STORAGE_MANAGER.data_list
# GET CLASS AND ITS ATTRIBUTES LIST #
class_and_attr_list = UML_STORAGE_MANAGER.class_and_attr_list
# GET RELATIONSHIP LIST #
relationship_list = UML_STORAGE_MANAGER.relationship_list
# GET CLASS NAME LIST #
class_list = UML_STORAGE_MANAGER.class_list

################################################################################
# WORKING WITH RELATIONSHIPS #

def add_relationship(source: str, dest: str, relation: str):
    # Ensure source and destination are not the same
    if source == dest:
        print("\nSource and destination classes cannot be the same.")
        return
    
    # Validate source and destination class names
    if not check_class_name(source, should_exist=True) or not check_class_name(dest, should_exist=True):
        return
    
     # Validate relationship type format
    format_check_message = check_format(relation)
    if format_check_message != "Valid input":
        print(format_check_message)
        return
    
    # Check if the relationship already exists
    if any(rel for rel in relationship_list if rel["source"] == source and rel["dest"] == dest):
        print(f"\nRelationship between '{source}' and '{dest}' already exists!")
        return
    
     # Confirm addition action
    if not user_choice(f"add relationship from '{source}' to '{dest}' of type '{relation}'"):
        return

    # Add the new relationship
    relationship_list.append({"source": source, "dest": dest, "relation": relation})
    print(f"\nAdded relationship from '{source}' to '{dest}' of type '{relation}'.")


def remove_relationship(source: str, dest: str):
    # Validate source and destination class names
    if not check_class_name(source, should_exist=True) or not check_class_name(dest, should_exist=True):
        return

    # Confirm removal action
    if not user_choice(f"remove relationship between '{source}' and '{dest}'"):
        return

    # Remove the relationship from the list if it exists
    initial_len = len(relationship_list)
    relationship_list[:] = [rel for rel in relationship_list if not (rel["source"] == source and rel["dest"] == dest)]

    # Check if a relationship was removed
    if len(relationship_list) < initial_len:
        print(f"\nRemoved relationship from '{source}' to '{dest}'.")
    else:
        print(f"\nNo relationship exists between '{source}' and '{dest}'.")


################################################################################
# CHECKING CLASS NAME #

# def validate_class_name(class_name: str) -> bool:
#     # Load the data again if necessary
#     data_list = UML_STORAGE_MANAGER.data_list
#     class_and_attr_list = data_list[0] if data_list else []

#     # Check if class exists in the list
#     return any(cls for cls in class_and_attr_list if cls["class_name"] == class_name)

def validate_class_name(class_name: str) -> bool:
    for dictionary in class_and_attr_list:
        if dictionary["class_name"] == class_name:
            return True
    return False


def check_class_name(class_name: str, should_exist: bool) -> bool:
    # Validate format and print the specific error message if format is incorrect
    format_check_message = check_format(class_name)
    
    if format_check_message != "Valid input":
        print(format_check_message)  # This prints the specific error message
        return False

    # Check if the class name exists in the data
    is_name_exist = validate_class_name(class_name)

    if should_exist and not is_name_exist:
        print(f"\nClass '{class_name}' not found!")
        return False

    return True


################################################################################
# OTHER HELPER FUNCTIONS #

def user_choice(action: str) -> bool:
    while True:
        user_input = input(f"\nAre you sure you want to {action}? (Yes/No): ").lower()
        if user_input in ["yes", "y"]:
            return True
        elif user_input in ["no", "n"]:
            print("\nAction cancelled.")
            return False
        else:
            print("\nInvalid input. Please enter 'Yes' or 'No'.")