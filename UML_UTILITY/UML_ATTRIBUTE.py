# Author: Emily Riley
# Date: 09/12/2024
# A shell to connect the CLI Application when editing attributes to the data manager

# Import check_format function
from validators import check_format


# Function to add an attribute to a class
def add_attr(class_name:str, attr_name:str):
    # Check if class_name and attr_name are in the right format
    class_format = check_format(class_name)
    if (class_format == "Valid input"):
        attr_format = check_format(attr_name)
        if (attr_format == "Valid input"):   
            # Make both class_name and attr_name in only lowercase letters
            class_name = class_name.lower()
            attr_name = attr_name.lower()
            # Call the data manager to create the new attribute 
            # write.add_attr(class_name, attr_name)
        else:
            print("Issue with attribute name: " + attr_format)
    else:
        print("Issue with class name: " + class_format)

# Function to delete an attribute from a class
def delete_attr(class_name:str, attr_name:str):
    # Check if class_name and attr_name are in the right format
    class_format = check_format(class_name)
    if (class_format == "Valid input"):
        attr_format = check_format(attr_name)
        if (attr_format == "Valid input"):  
            # Make both class_name and attr_name in only lowercase letters
            class_name = class_name.lower()
            attr_name = attr_name.lower()
            # Call the data manager to delete the attribute 
            # write.delete_attr(class_name, attr_name)
        else:
            print("Issue with attribute name: " + attr_format)
    else:
        print("Issue with class name: " + class_format)

# Function to rename an attribute in a class
def rename_attr(class_name:str, old_attr_name:str, new_attr_name:str):
    # Check if class_name, old and new attr_name are in the right format
    class_format = check_format(class_name)
    if (class_format == "Valid input"):
        old_attr_format = check_format(old_attr_name)
        if (old_attr_format == "Valid input"):
            new_attr_format = check_format(new_attr_name)
            if (new_attr_format == "Valid input"):    
                # Make class_name, old and new attr_name in only lowercase letters
                class_name = class_name.lower()
                old_attr_name = old_attr_name.lower()
                new_attr_name = new_attr_name.lower()
                # Call the data manager to delete the attribute 
                ## write.rename_attr(class_name, old_attr_name, new_attr_name)
            else:
                print("Issue with new attribute name: " + new_attr_format)
        else:
            print("Issue with previous attribute name: " + old_attr_format)
    else:
        print("Issue with class name: " + class_format)
