
###################################################################################################

from typing import List, Dict
from enum import Enum
from UML_MANAGER.uml_core_manager import UMLCoreManager as Manager

###################################################################################################

# Global manager #
ProgramManager = Manager()

###################################################################################################
### ENUM VALUES FOR THE INTERFACE ###

class InterfaceOptions(Enum):
    ADD_CLASS = "add_class"
    DELETE_CLASS = "delete_class"
    RENAME = "rename_class"
    ADD_FIELD = "add_field"
    DELETE_FIELD = "delete_field"
    RENAME_FIELD = "rename_field"
    ADD_METHOD = "add_method"
    DELETE_METHOD = "delete_method"
    RENAME_METHOD = "rename_method"
    ADD_REL = "add_rel"
    DELETE_REL = "delete_rel"
    LIST_CLASS = "list_class"
    CLASS_DETAIL = "class_detail"
    CLASS_REL = "class_rel"
    SAVED_LIST = "saved_list"
    SAVE = "save"
    LOAD = "load"
    DELETE_SAVED = "delete_saved"
    CLEAR_DATA = "clear_data"
    DEFAULT = "default"
    SORT = "sort"
    HELP = "help"
    EXIT = "exit"    
    
###################################################################################################

class UMLCommandLineInterface:
    
    # Constructor for interface #
    def __init__(self):
        pass
    #################################################################
    ### INTERFACE FUNCTIONS THAT CONNECT WITH THE MANAGER ###
    
    ## DATA RELATED FOR GUI ##

    # Get main data #
    def get_main_data(self) -> Dict:
        return ProgramManager._get_main_data()
    
    # Get relationship list #
    def get_relationship_list(self) -> List:
        return ProgramManager._get_relationship_list()
    
    # Get storage manager #
    def get_storage_manager(self):
        return ProgramManager._get_storage_manager()
    
    # Extract and and a list of UML class data #
    """class_data can be retrieved using get_main_data()
       main_data =  get_main_data()
       class_data = main_data["classes"]
    """
    def extract_class_data(self, class_data: List[Dict]) -> List: 
        return ProgramManager._extract_class_data(class_data)
    
    ## CLASS RELATED ##
    
    # Add class interface #
    def add_class(self, class_name: str):
        ProgramManager._add_class(class_name, is_loading=False)
        
    # Delete class interface #
    def delete_class(self, class_name: str):
        ProgramManager._delete_class(class_name, is_loading=False)
        
    # Rename class interface #
    def rename_class(self, current_name: str, new_name: str):
        ProgramManager._rename_class(current_name, new_name, is_loading=False)
        
    ## ATTRIBUTE RELATED ##
    
    # Add attribute interface #
    def add_attribute(self, class_name: str, attribute_name: str):
        ProgramManager._add_field(class_name, attribute_name, is_loading=False)
        
    # Delete attribute interface #
    def delete_attribute(self, class_name: str, attribute_name: str):
        ProgramManager._delete_field(class_name, attribute_name, is_loading=False)
    
    # Rename attribute interface #
    def rename_attribute(self, class_name: str, current_attribute_name: str, new_attribute_name: str):
        ProgramManager._rename_field(class_name, current_attribute_name, new_attribute_name, is_loading=False)
        
    ## METHOD RELATED ##
    
    # Add method interface #
    def add_method(self, class_name: str, method_name: str):
        ProgramManager._add_method(class_name, method_name, is_loading=False)
    
    # Delete method interface #
    def delete_method(self, class_name: str, method_name: str):
        ProgramManager._delete_method(class_name, method_name, is_loading=False)
        
    # Rename method interface #
    def rename_method(self, class_name: str, current_method_name: str, new_method_name: str):
        ProgramManager._rename_method(class_name, current_method_name, new_method_name, is_loading=False)
        
    ## RELATIONSHIP RELATED ##
    
    # Add relationship interface #
    def add_relationship_wrapper(self):
        """We use this one for our program, which has user input"""
        ProgramManager._add_relationship_wrapper(is_loading=False)
        
    # Add relationship interface #
    """We use this one for Unit Test to avoid the user input mock"""
    def add_relationship(self, source_class_name: str, destination_class_name: str, type: str):
        ProgramManager._add_relationship(source_class_name, destination_class_name, type, is_loading=False)
    
    # Delete relationship interface #
    def delete_relationship(self, source_class_name: str, destination_class_name: str):
        ProgramManager._delete_relationship(source_class_name, destination_class_name, is_loading=False)
    
    ## DISPLAY RELATED ##
    
    # Display saved file list #
    def display_saved_list(self):
        ProgramManager._display_saved_list()
        
    # Display classes #
    def display_classes(self):
        ProgramManager._display_wrapper()
        
    # Display single class #
    def display_single_class(self, class_name: str):
        ProgramManager._display_single_class_detail(class_name)
        
    # Display relationship #
    def display_relationship(self):
        ProgramManager._display_relationship_list()
    
    ## SAVE/LOAD RELATED ##
    
    # Save data #
    def save(self):
        ProgramManager._save()
        
    # Load data #
    def load(self):
        ProgramManager._load()
    
    # Delete saved file #
    def delete_saved_file(self):
        ProgramManager._delete_saved_file()
        
    # Get active file #
    def get_active_file(self) -> str:
        return ProgramManager._get_active_file()
    
    # Saved file name check #
    def saved_file_name_check(self, file_name: str) -> bool:
        return ProgramManager._saved_file_name_check(file_name)
    
    # Clear current active data #
    def clear_current_active_data(self):
        ProgramManager._clear_current_active_data()
    
    # Go back to blank program #
    def end_session(self):
        ProgramManager._end_session()
        
    # Sort class list #
    def sort_class_list(self):
        ProgramManager._sort_class_list()
        
    # Turn off all file statuses when exiting program #
    def exit(self):
        ProgramManager._exit()

    #################################################################   
    def __prompt_menu(self):
        print("Welcome To Our UML Program!\n")
        # Class
        print("Type 'add_class <class_name>' to add a class")
        print("Type 'delete_class <class_name>' to delete a class")
        print("Type 'rename_class <class_name> <new_name>' to rename a class\n")
        # Attribute
        print("Type 'add_field <class_name> <attr_name>' to add a field")
        print("Type 'delete_field <class_name> <field_name>' to delete a field from the chosen class")
        print("Type 'rename_field <class_name> <current_field_name> <new_name>' to rename a field\n")
        # Method
        print("Type 'add_method <class_name> <method_name>' to add a method")
        print("Type 'delete_method <class_name> <method_name>' to delete a method from the chosen class")
        print("Type 'rename_method <class_name> <current_method_name> <new_name>' to rename a method\n")
        # Relationship
        print("Type 'add_rel to add relationship and relationship level")
        print("Type 'delete_rel <chosen_class_name> <destination_class_name>' to delete a relationship\n")
        # Class related commands
        print("Type 'list_class' to see the list of all created class(es)")
        print("Type 'class_detail <class_name>' to see the detail of the chosen class")
        print("Type 'class_rel' to see the relationships between class(es)\n")
        # Save/Load related commands
        print("Type 'saved_list' to see the list of saved files")
        print("Type 'save' to save data")
        print("Type 'load' to load data from saved files")
        print("Type 'delete_saved' to delete saved file")
        print("Type 'clear_data' to delete all the data in the current storage")
        print("Type 'default' to go back to blank program\n")
        # Other tasks
        print("Type 'sort' to sort the class list in alphabetical order")
        print("Type 'help' to see the instructions")
        print("Type 'exit' to quit program")

    def main_program_loop(self):
        self.__prompt_menu()
        while True:
            current_active_file: str = self.get_active_file()
            if current_active_file != "No active file!":
                current_active_file = current_active_file + ".json"
            print(f"\n(Current active file: {current_active_file})")
            print("\n==> ", end="")
            user_input: str = input()
            # Split the input by space
            # Split the input by space
            user_input_component = user_input.split()
            # Get separate command and class name part
            command = user_input_component[0]
            first_param = user_input_component[1] if len(user_input_component) > 1 else None
            second_param = (user_input_component[2] if len(user_input_component) > 2 else None)
            third_param = user_input_component[3] if len(user_input_component) > 3 else None
            # Start the logic
            #######################################################
            
            # Add class
            if command == InterfaceOptions.ADD_CLASS.value and first_param:
                self.add_class(first_param)
            # Delete class
            elif command == InterfaceOptions.DELETE_CLASS.value and first_param:
                self.delete_class(first_param)
            # Rename class
            elif (
                command == InterfaceOptions.RENAME.value
                and first_param
                and second_param
            ):
                self.rename_class(first_param, second_param)

            #######################################################

            # Add attribute #
            elif (
                command == InterfaceOptions.ADD_FIELD.value
                and first_param
                and second_param
            ):
                self.add_attribute(first_param, second_param)
            # Delete attribute #
            elif (
                command == InterfaceOptions.DELETE_FIELD.value
                and first_param
                and second_param
            ):
                self.delete_attribute(first_param, second_param)
            # Rename attribute #
            elif (
                command == InterfaceOptions.RENAME_FIELD.value
                and first_param
                and second_param
                and third_param
            ):
                self.rename_attribute(first_param, second_param, third_param)

            #######################################################
            
            # Add method #
            elif (
                command == InterfaceOptions.ADD_METHOD.value
                and first_param
                and second_param
            ):
                self.add_method(first_param, second_param)
            # Delete method #
            elif (
                command == InterfaceOptions.DELETE_METHOD.value
                and first_param
                and second_param
            ):
                self.delete_method(first_param, second_param)
            # Rename method #
            elif (
                command == InterfaceOptions.RENAME_METHOD.value
                and first_param
                and second_param
                and third_param
            ):
                self.rename_method(first_param, second_param, third_param)
            
            #######################################################

            # Add relationship
            elif command == InterfaceOptions.ADD_REL.value:
                self.add_relationship_wrapper()
            # Delete relationship #
            elif (
                command == InterfaceOptions.DELETE_REL.value
                and first_param
                and second_param
            ):
                self.delete_relationship(first_param, second_param)
                
            #######################################################
                
            # List all the created class names or all class detail #
            elif command == InterfaceOptions.LIST_CLASS.value:
                self.display_classes() 
            # Show the details of the chosen class #
            elif command == InterfaceOptions.CLASS_DETAIL.value and first_param:
                self.display_single_class(first_param)
            # Show the relationship of the chosen class with others #
            elif command == InterfaceOptions.CLASS_REL.value:
                self.display_relationship()
            # Show the list of saved files #
            elif command == InterfaceOptions.SAVED_LIST.value:
                self.display_saved_list()
            # Save the data #
            elif command == InterfaceOptions.SAVE.value:
                self.save()
            # Load the data #
            elif command == InterfaceOptions.LOAD.value:
                self.load()
            # Delete saved file #
            elif command == InterfaceOptions.DELETE_SAVED.value:
                self.delete_saved_file()
            # Clear data in current storage #
            elif command == InterfaceOptions.CLEAR_DATA.value:
                self.clear_current_active_data()
            # Go back to blank program #
            elif command == InterfaceOptions.DEFAULT.value:
                self.end_session()
            # Sort the class list #
            elif command == InterfaceOptions.SORT.value:
                self.sort_class_list()
            # Show the main menu again #
            elif command == InterfaceOptions.HELP.value:
                self.__prompt_menu()
            # Exit the program #
            elif command == InterfaceOptions.EXIT.value:
                break
            else:
                print(f"\nUnknown command '{user_input}'. Type 'help' for a list of commands.")
        self.exit()