################################################################
#   Author : Emily Riley
#   Created: September 12, 2024
#
#   A shell to handle atttributes
################################################################


################################################################
# IMPORTED MODULES #

import UML_UTILITY.SAVE_LOAD.save_load as SAVE_LOAD
import UML_CLASS.uml_class as UML_CLASS
from UML_UTILITY.FORMAT_CHECKING.validators import check_format

################################################################
# LOADING DATA FROM CLASS FILE #

# Get class and attr list from UML_CLASS
class_and_attr_list = UML_CLASS.class_and_attr_list

################################################################
# ADD, DELETE, RENAME ATTRIBUTE FUNCTIONS #

# Function to add an attribute to a class #
def add_attr(class_name:str, attr_name:str):
    # Check if class name exists, 
    # if not, called function will print error, current function stops
    is_class_exist = UML_CLASS.check_class_name(class_name, should_exist=True)
    if not is_class_exist:
        return
    # Put class name in lowercase
    class_name = class_name.lower()
    # Get attribute list for specific class
    attr_list = get_attr_list(class_name)
    # Check if attribute already exists
    # if it does, called function will print error, current function ends
    is_attr_exist = check_attr_name(attr_list, attr_name, False)
    if not is_attr_exist:
        return
    # Create JSON object for attribute
    json_attr = get_attr_json_format(attr_name)
    # Add JSON attribute object to global object that holds classes
    for cls in class_and_attr_list:
        if (cls["class_name"] == class_name):
            cls["attr_list"].append(json_attr)
    print(f"Attribute '{attr_name}' was successfully added!")
    
    
    
    
    
    

# Function to delete an attribute from a class
def delete_attr(class_name:str, attr_name:str):
    pass

# Function to rename an attribute in a class
def rename_attr(class_name:str, old_attr_name:str, new_attr_name:str):
    pass

################################################################
# CHECK ATTRIBUTE FUNCTIONS #

# Check Attr Name Exist Helper #
def validate_attr_name(attr_list:str, attr_name: str):
    for attribute in attr_list:
        if attribute["attr_name"] == attr_name:
            return True
    return False

def check_attr_name(attr_list:str, attr_name:str, should_exist:bool) -> bool:
    is_format_correct = check_format(attr_name)
    if is_format_correct != "Valid input":
        print(is_format_correct)
        return 
    is_attr_exist = validate_attr_name(attr_list, attr_name)
    # If the name should exist but not exist
    if should_exist and not is_attr_exist:
        print(f"Attribute '{attr_name}' not found!")
        return False
    # If the name should not exist but still exist
    elif not should_exist and is_attr_exist:
        print(f"Attribute '{attr_name}' has already existed!")
        return False
    # True in any other cases
    return True
    

################################################################
# OTHER HELPER FUNCTIONS #

# Assuming we already know class_name exists, 
# and class_name is in correct format
def get_attr_list(class_name:str) -> list:
    for cls in class_and_attr_list:
        if (cls["class_name"] == class_name):
            return cls["attr_list"]
        
# Get JSON Format #
#  #
def get_attr_json_format(attr_name: str) -> dict[str, str]:
    return {
        "attr_name": attr_name
    }

################################################################

