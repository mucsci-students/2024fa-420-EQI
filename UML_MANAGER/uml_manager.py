"""
Author : Quang Bui
Created: September 15, 2024

Description:
    This shell will manage uml_class, uml_attribute
    and uml_relationship shells by sharing the data list
    to ensure the consistency between each shell

List of last date modified:
- September 15, 2024 (By Quang)

"""

################################################################
# IMPORTED MODULES #

import UML_UTILITY.SAVE_LOAD.save_load as SAVE_LOAD

################################################################

# LOADING DATA FROM JSON FILE TO GLOBAL DICTIONARY #
data_list = SAVE_LOAD.load_data_from_json("data.json")
# Create a class so that we can display it or sort it alphabetically easily
class_list: list[str] = []
# If there is no data in json file
# Provides an empty list if "classes" key is missing
if data_list is None:
    data_list = [[], []]

# Get list of classes and its attributes
class_and_attr_list = data_list[0]
# Get list of relationships
relationship_list = data_list[1]
# Add class name to class_list
for dictionary in class_and_attr_list:
    class_list.append(dictionary["class_name"])
