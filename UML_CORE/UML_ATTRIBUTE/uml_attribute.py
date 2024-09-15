"""
Author : Emily Riley
Created: September 13, 2024

Description:
    A shell to handle atttribute functions

List of last date modified:
- September 15, 2024 (By Quang)

"""


################################################################
# IMPORTED MODULES #

import UML_CORE.UML_CLASS.uml_class as UML_CLASS
import UML_MANAGER.uml_manager as UML_MANAGER
from UML_UTILITY.FORMAT_CHECKING.validators import check_format

################################################################

# GET CLASS AND ITS ATTRIBUTES LIST #
class_and_attr_list = UML_MANAGER.class_and_attr_list

################################################################
# ADD, DELETE, RENAME ATTRIBUTE FUNCTIONS #

# Function to add an attribute to a class #
def add_attr(class_name:str, attr_name:str):
    # Put class name in lowercase
    class_name = class_name.lower()
    # Check if class name exists, 
    # if not, called function will print error, current function stops
    is_class_exist = UML_CLASS.check_class_name(class_name, should_exist=True)
    if not is_class_exist:
        return
    # Get attribute list for specific class
    attr_list = get_attr_list(class_name)
    attr_name = attr_name.lower()
    # Check if attribute already exists
    # if it does, called function will print error, current function ends
    is_attr_exist = check_attr_name(attr_list, attr_name,class_name,False)
    if not is_attr_exist:
        return
    # Make sure user want to add attribute or not
    is_chosen_yes = user_choice(f"add attribute '{attr_name}' to class '{class_name}'")
    if not is_chosen_yes:
        return
    # Create JSON object for attribute
    json_attr = get_attr_json_format(attr_name)
    # Add JSON attribute object to global object that holds classes
    for cls in class_and_attr_list:
        if (cls["class_name"] == class_name):
            cls["attr_list"].append(json_attr)
    # Print successful message 
    print(f"Attribute '{attr_name}' was successfully added to class '{class_name}'!")
     

# Function to delete an attribute from a class #
def delete_attr(class_name:str, attr_name:str):
    # Put class name in lowercase
    class_name = class_name.lower()
    # Check if class name exists, 
    # if not, called function will print error, current function stops
    is_class_exist = UML_CLASS.check_class_name(class_name, should_exist=True)
    if not is_class_exist:
        return
    # Get attribute list for specific class
    attr_list = get_attr_list(class_name)
    # Attribute name lowercase
    attr_name = attr_name.lower()
    # Check if attribute already exists
    # if not, called function will print error, current function ends
    is_attr_exist = check_attr_name(attr_list, attr_name,class_name, True)
    if not is_attr_exist:
        return
    # Make sure user want to delete attribute or not
    is_chosen_yes = user_choice(f"delete attribute '{attr_name}' from class '{class_name}'")
    if not is_chosen_yes:
        return
    # Get attribute object that exists in class object
    attr_object = get_attr_object(attr_list, attr_name)  
    # Find and delete attribute object
    for cls in class_and_attr_list:
        if (cls["class_name"] == class_name):
            cls["attr_list"].remove(attr_object)
    # Print successful message 
    print(f"Attribute '{attr_name}' was successfully deleted from class '{class_name}'!")
    

# Function to rename an attribute in a class
def rename_attr(class_name:str, old_attr_name:str, new_attr_name:str):
    # Put class name in lowercase
    class_name = class_name.lower()
    # Check if class name exists, 
    # if not, called function will print error, current function stops
    is_class_exist = UML_CLASS.check_class_name(class_name, should_exist=True)
    if not is_class_exist:
        return
    # Get attribute list for specific class
    attr_list = get_attr_list(class_name)
    # Lowercase both attributes
    old_attr_name = old_attr_name.lower()
    new_attr_name = new_attr_name.lower()
    # Check if old attribute name already exists
    # if not, called function will print error, current function ends
    is_old_attr_exist = check_attr_name(attr_list, old_attr_name,class_name, True)
    if not is_old_attr_exist:
        return False
    # Check if new attribute name already exists
    # if it does, called function will print error, current function ends
    is_new_attr_exist = check_attr_name(attr_list, new_attr_name,class_name, False)
    if not is_new_attr_exist:
        return
    # Make sure user want to rename attribute or not
    is_chosen_yes = user_choice(f"rename attribute name '{old_attr_name}' to attribute name '{new_attr_name}' from class '{class_name}'")
    if not is_chosen_yes:
        return   
    # Find old attribute and change name to new attribute
    for cls in class_and_attr_list:
        if (cls["class_name"] == class_name):
            for attribute in cls["attr_list"]:
                if attribute["attr_name"] == old_attr_name:
                    attribute["attr_name"] = new_attr_name
    # Print successful message
    print(f"Attribute '{old_attr_name}' was renamed to '{new_attr_name}' in class '{class_name}'!")




################################################################
# CHECK ATTRIBUTE FUNCTIONS #

# Check Attr Name Exist Helper #
def validate_attr_name(attr_list:str, attr_name: str):
    for attribute in attr_list:
        if attribute["attr_name"] == attr_name:
            return True
    return False

# Check if attribute name exists or doesnt exist depending on should_exist param 
# when given list of attributes, attribute name and class name
def check_attr_name(attr_list:str, attr_name:str,class_name:str, should_exist:bool) -> bool:
    # Check format of attr_name, stop function and print error if not correct
    is_format_correct = check_format(attr_name)
    if is_format_correct != "Valid input":
        print(is_format_correct)
        return 
    # Check if attribute exists
    is_attr_exist = validate_attr_name(attr_list, attr_name)
    # If the name should exist but not exist
    if should_exist and not is_attr_exist:
        print(f"Attribute '{attr_name}' not found in class '{class_name}'!")
        return False
    # If the name should not exist but still exist
    elif not should_exist and is_attr_exist:
        print(f"Attribute '{attr_name}' already existed in class '{class_name}'!")
        return False
    # True in any other cases
    return True
    

################################################################
# OTHER HELPER FUNCTIONS #

# Assuming we already know class_name exists, 
# and class_name is in correct format
# Get the attribute list for specific class
def get_attr_list(class_name:str) -> list:
    for cls in class_and_attr_list:
        if (cls["class_name"] == class_name):
            return cls["attr_list"]
        
# Get JSON Format of Attribute #
def get_attr_json_format(attr_name: str) -> dict[str, str]:
    return {
        "attr_name": attr_name
    }

# Get the attribute object from a list of attributes,
# Assuming we know the attribute exists
# ONLY CALL IF YOU ALREADY CHECKED IF ATTRIBUTE EXISTS #
def get_attr_object(attr_list:str, attr_name) -> dict[str, str]:
    for attribute in attr_list:
        if (attribute["attr_name"] == attr_name):
            return attribute
        
# User Decision Making #
def user_choice(action: str) -> bool:
    while True:
        user_input = input(f"Are you sure you want to {action}? (Yes/No): ").lower()
        if user_input in ["yes", "y"]:
            return True
        elif user_input in ["no", "n"]:
            print("Action cancelled.")
            return False
        else:
            print("Invalid input. Please enter 'Yes' or 'No'.")

################################################################

