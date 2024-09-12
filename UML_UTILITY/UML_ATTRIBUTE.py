# A shell to connect the CLI Application when editing attributes to the data manager


# Function to add an attribute to a class
def add_attr(class_name:str, attr_name:str):
    # Check if class_name and attr_name are in the right format
    if (check_format(class_name) == True):
        if (check_format(attr_name) == True):   
            # Make both class_name and attr_name in only lowercase letters
            class_name = class_name.lower()
            attr_name = attr_name.lower()
            # Call the data manager to create the new attribute 
            # write.add_attr(class_name, attr_name)

# Function to delete an attribute from a class
def delete_attr(class_name:str, attr_name:str):
    # Check if class_name and attr_name are in the right format
    if (check_format(class_name) == True):
        if (check_format(attr_name) == True):   
            # Make both class_name and attr_name in only lowercase letters
            class_name = class_name.lower()
            attr_name = attr_name.lower()
            # Call the data manager to delete the attribute 
            # write.delete_attr(class_name, attr_name)


# Function to rename an attribute in a class
def rename_attr(class_name:str, old_attr_name:str, new_attr_name:str):
    # Check if class_name, old and new attr_name are in the right format
    if (check_format(class_name) == True):
        if (check_format(old_attr_name) == True):
            if (check_format(new_attr_name) == True):    
                # Make class_name, old and new attr_name in only lowercase letters
                class_name = class_name.lower()
                old_attr_name = old_attr_name.lower()
                new_attr_name = new_attr_name.lower()
                # Call the data manager to delete the attribute 
                ## write.rename_attr(class_name, old_attr_name, new_attr_name)


# Function that will check if the format of a string is correct (only alphabetical)
# Function will be moved to a different shell and imported
def check_format(word:str):
    pass