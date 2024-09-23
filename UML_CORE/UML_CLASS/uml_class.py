"""
Author : Quang Bui
Created: September 12, 2024

Description:
    This shell has UML class deatures

List of date modified:
- September 15, 2024 (By Quang)
- September 19, 2024 (By Quang)

"""

################################################################
# IMPORTED MODULES #

import UML_MANAGER.uml_storage_manager as UML_STORAGE_MANAGER
from UML_UTILITY.FORMAT_CHECKING.validators import check_format

################################################################

# GET DATA FROM JSON FILE #
data_list = UML_STORAGE_MANAGER.data_list
# GET CLASS AND ITS ATTRIBUTES LIST #
class_and_attr_list = UML_STORAGE_MANAGER.class_and_attr_list
# GET RELATIONSHIP LIST #
relationship_list = UML_STORAGE_MANAGER.relationship_list
# GET CLASS NAME LIST #
class_list = UML_STORAGE_MANAGER.class_list

################################################################################
# WORKING WITH CLASSES #


# Add Class #
def add_class(class_name: str):
    # After checking format, check if class_name already existed or not
    # If not, prompt error
    is_name_exist = check_class_name(class_name, should_exist=False)
    if not is_name_exist:
        return
    # Make sure user want to add class or not
    is_chosen_yes = user_choice(f"add class '{class_name}'")
    if not is_chosen_yes:
        return
    # Convert to json object and append to the list
    transformed_json_object = get_class_json_format(class_name)
    class_and_attr_list.append(transformed_json_object)
    class_list.append(class_name)
    print(f"\nAdded class '{class_name}' successfully!")


# Delete Class #
def delete_class(class_name: str):
    # After checking format, check if class_name already existed or not
    # If not, prompt error
    is_name_exist = check_class_name(class_name, should_exist=True)
    if not is_name_exist:
        return
    # Make sure user want to delete class or not
    is_chosen_yes = user_choice(f"delete class '{class_name}'")
    if not is_chosen_yes:
        return
    # If class exist, get the class object and pop from the list
    class_object = get_chosen_class(class_name)
    class_and_attr_list.remove(class_object)
    class_list.remove(class_name)
    clean_up_relationship(class_name)
    print(f"\nSuccessfully removed class '{class_name}'!")


# Rename Class #
def rename_class(class_name: str, new_name: str):
    # If class exist, remove the class, else prompt error'
    able_to_rename = is_able_to_rename(class_name, new_name)
    if not able_to_rename:
        return
    # If it is able to rename, get the object from the list
    class_object = get_chosen_class(class_name)
    # Make sure user want to rename class or not
    is_chosen_yes = user_choice(
        f"change from class name '{class_name}' to '{new_name}'"
    )
    if not is_chosen_yes:
        return
    # Update source/dest name:
    change_name(class_name, new_name)
    # Change to new name
    class_object["class_name"] = new_name
    class_list.remove(class_name)
    class_list.append(new_name)
    print(f"\nSuccessfully changed class name from '{class_name}' to '{new_name}'!")


################################################################################
# CHECKING CLASS NAME #


# Check Class Name Exist Helper #
def validate_class_name(class_name: str):
    for dictionary in class_and_attr_list:
        if dictionary["class_name"] == class_name:
            return True
    return False


# Check Class Name Exist Including Prompting Error Messages #
def check_class_name(class_name: str, should_exist: bool) -> bool:
    is_format_correct = check_format(class_name)
    if is_format_correct != "Valid input":
        print(is_format_correct)
        return False
    is_name_exist: bool = validate_class_name(class_name)
    # If the name should exist but not exist
    if should_exist and not is_name_exist:
        print(f"\nClass '{class_name}' not found!")
        return False
    # If the name should not exist but still exist
    elif not should_exist and is_name_exist:
        print(f"\nClass '{class_name}' has already existed!")
        return False
    # True in any other cases
    return True


# Helper Function To Check Both Current Name And New Name In 'rename_class()' #
def is_able_to_rename(class_name: str, new_name: str) -> bool:
    # Check current class name format
    class_name_result = check_format(class_name)
    if class_name_result != "Valid input":
        # If not valid, prompt error
        print(class_name_result)
        return False
    # Check new class name format
    new_class_name_result = check_format(new_name)
    if new_class_name_result != "Valid input":
        # If not valid, prompt error
        print(new_class_name_result)
        return False
    # After checking format, check if class_name and new_name already existed or not
    is_current_name_exist = check_class_name(class_name, should_exist=True)
    if not is_current_name_exist:
        return False
    is_new_name_exist = check_class_name(new_name, should_exist=False)
    if not is_new_name_exist:
        return False
    return True


# Change Source Class / Dest Class Name #
def change_name(class_name: str, new_name: str):
    for each_dictionary in relationship_list:
        for key, value in each_dictionary.items():
            if value == class_name:
                each_dictionary[key] = new_name


################################################################################
# OTHER HELPER FUNCTIONS #


# Get JSON Format #
# NOTE: Don't call this class if you did not check for class name!!!!!!! #
def get_class_json_format(class_name: str) -> dict[str, list[dict[str, str]]]:
    return {
        "attr_list": [],  # Placeholder for attribute names
        "class_name": class_name,
    }


# Get Chosen Class #
def get_chosen_class(class_name: str) -> dict[str, list[dict[str, str]]]:
    for dictionary in class_and_attr_list:
        if dictionary["class_name"] == class_name:
            return dictionary
    return None


# User Decision Making #
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


# Clean Up Relationship #
def clean_up_relationship(class_name: str):
    # Create a new list that excludes relationships with dest or source equal to class_name
    relationship_list[:] = [
        relationship
        for relationship in relationship_list
        if relationship["dest"] != class_name and relationship["source"] != class_name
    ]


################################################################################
