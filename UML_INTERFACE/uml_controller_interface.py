###################################################################################################
"""
Module: UMLInterface
This module defines the UMLInterface class, which serves as the interface layer between the user and the underlying
UML model and controller. It provides various methods for creating and managing UML classes, fields, methods,
parameters, and relationships. It also facilitates interaction with the model for data retrieval and modification, 
testing, and saving/loading UML diagrams.
"""
###################################################################################################

from rich.console import Console
from typing import List, Dict
from UML_MVC.UML_MODEL.uml_model import UMLModel as Model
from UML_MVC.UML_CONTROLLER.uml_controller import UMLController as Controller, InterfaceOptions
from UML_MVC.UML_CONTROLLER.cli_completer import create_prompt_session
from prompt_toolkit import HTML

###################################################################################################

class UMLInterface:
    """
    UMLInterface is the interface class that bridges the gap between the user interaction and the underlying
    UML model and controller. It defines methods for managing UML components like classes, fields, methods, 
    and relationships. Additionally, it provides utilities for saving/loading data and interacting with the 
    observer pattern.
    """

    # Constructor for UMLInterface #
    def __init__(self, view):
        """
        Initializes the UMLInterface with the specified view. Each UMLInterface instance maintains its 
        own program components, including the model, controller, and console, which makes testing easier.

        Parameters:
            view: The view object responsible for presenting information to the user.
        """
        self.Console = Console()  # Rich console instance for formatted output
        self.View = view  # Reference to the view
        self.Model = Model(self.View, self.Console)  # UML model instance
        self.Controller = Controller(self.Model, view, self.Console)  # UML controller instance
    
        # Initialize prompt_toolkit session for autocompletion
        self.session = create_prompt_session()
        
    #################################################################
    ### INTERFACE FUNCTIONS THAT CONNECT WITH THE MANAGER ###
    
    ## OBJECT CREATION ##
    
    # Class creation method interface #
    def create_class(self, class_name: str):
        """
        Creates a new UML class by delegating the operation to the model.

        Parameters:
            class_name (str): The name of the class to be created.

        Returns:
            Result from the model's class creation operation.
        """
        return self.Model.create_class(class_name)
    
    # Field creation method interface #
    def create_field(self, field_name: str):
        """
        Creates a new field for a UML class by delegating the operation to the model.

        Parameters:
            field_name (str): The name of the field to be created.

        Returns:
            Result from the model's field creation operation.
        """
        return self.Model.create_field(field_name)
    
    # Method creation method interface #
    def create_method(self, method_name: str):
        """
        Creates a new method for a UML class by delegating the operation to the model.

        Parameters:
            method_name (str): The name of the method to be created.

        Returns:
            Result from the model's method creation operation.
        """
        return self.Model.create_method(method_name)
    
    # Parameter creation method interface #
    def create_parameter(self, parameter_name: str):
        """
        Creates a new parameter for a UML method by delegating the operation to the model.

        Parameters:
            parameter_name (str): The name of the parameter to be created.

        Returns:
            Result from the model's parameter creation operation.
        """
        return self.Model.create_parameter(parameter_name)
    
    # Relationship creation method interface #
    def create_relationship(self, source_class: str, destination_class: str, rel_type: str):
        """
        Creates a new relationship between two UML classes by delegating the operation to the model.

        Parameters:
            source_class (str): The name of the source class.
            destination_class (str): The name of the destination class.
            rel_type (str): The type of relationship (e.g., aggregation, composition).

        Returns:
            Result from the model's relationship creation operation.
        """
        return self.Model.create_relationship(source_class, destination_class, rel_type)
    
    ## DATA RELATED FOR GUI AND TESTING ##
    
    # Get chosen relationship #
    def get_chosen_relationship(self, source_class_name: str, destination_class_name: str):
        return self.Model._get_chosen_relationship(source_class_name, destination_class_name)
    
    # Get the relationship type between two classes #
    def get_chosen_relationship_type(self, source_class_name: str, destination_class_name: str):
        return self.Model._get_chosen_relationship_type(source_class_name, destination_class_name)
    
    def get_param_list(self, class_name: str, method_num: str):
        return self.Model._get_param_list(class_name, method_num)
    
    # Check if relationship exist or not #
    def relationship_exist(self, source_class_name: str, destination_class_name: str):
        return self.Model._relationship_exist(source_class_name, destination_class_name)
    
    # Get class list #
    def get_class_list(self):
        """
        Retrieves the list of UML classes from the model.

        Returns:
            A list of class names.
        """
        return self.Model._get_class_list()
    
    # Get storage manager interface #
    def get_storage_manager(self):
        """
        Retrieves the storage manager for handling save/load operations.

        Returns:
            The storage manager instance.
        """
        return self.Model._get_storage_manager()
    
    # Get relationship list interface #
    def get_relationship_list(self) -> List:
        """
        Retrieves the list of relationships between UML classes.

        Returns:
            A list of relationships.
        """
        return self.Model._get_relationship_list()

    # Get main data interface #
    def get_main_data(self) -> Dict:
        """
        Retrieves the main data structure from the model, which includes classes and relationships.

        Returns:
            A dictionary containing UML classes and relationships.
        """
        return self.Model._get_main_data()
    
    # Set main data interface #
    def set_main_data(self, new_data):
        self.Model._set_main_data(new_data)
    
    # Get view #
    def get_user_view(self):
        """
        Retrieves the view that is responsible for displaying UML information.

        Returns:
            The view object.
        """
        return self.Model._get_user_view()
    
    # Extract and process class data #
    def extract_class_data(self, class_data: List[Dict]) -> List:
        """
        Extracts class data from the provided class data dictionary.

        Parameters:
            class_data (List[Dict]): The class data to be extracted.

        Returns:
            A processed list of extracted class data.
        """
        return self.Model._extract_class_data(class_data)
    
    # Validate if UML entities (class, field, method, parameter) exist #
    def validate_entities(
        self,
        class_name: str = None, 
        field_name: str = None, 
        method_name: str = None, 
        parameter_name: str = None, 
        class_should_exist: bool = None, 
        field_should_exist: bool = None,
        method_should_exist: bool = None, 
        parameter_should_exist: bool = None
    ) -> bool:
        """
        Validates the existence of UML entities like class, field, method, or parameter.
        This can be used for testing and verifying the existence of various UML components.

        Parameters:
            class_name (str): The name of the class to check.
            field_name (str): The name of the field to check.
            method_name (str): The name of the method to check.
            parameter_name (str): The name of the parameter to check.
            class_should_exist (bool): Whether the class should exist.
            field_should_exist (bool): Whether the field should exist.
            method_should_exist (bool): Whether the method should exist.
            parameter_should_exist (bool): Whether the parameter should exist.

        Returns:
            bool: True if validation passes, False otherwise.
        """
        return self.Model._validate_entities(
            class_name, field_name, method_name, parameter_name, 
            class_should_exist, field_should_exist, 
            method_should_exist, parameter_should_exist
        )
        
    def get_method_based_on_index(self,class_name: str, method_num: str):
        return self.Model._get_method_based_on_index(class_name, method_num)
    
    def get_param_based_on_index(self, class_name: str, method_num: str, parameter_name: str):
        return self.Model._get_param_based_on_index(class_name, method_num, parameter_name)
    
    def get_rel_type(self, source_class_name: str, destination_class_name: str):
        return self.Model._get_rel_type(source_class_name, destination_class_name)
    ## CLASS RELATED ##
    
    # Add class interface #
    def add_class(self, class_name: str):
        """
        Adds a UML class by delegating the operation to the model.

        Parameters:
            class_name (str): The name of the class to be added.
        """
        return self.Model._add_class(class_name)
        
    # Delete class interface #
    def delete_class(self, class_name: str):
        """
        Deletes a UML class by delegating the operation to the model.

        Parameters:
            class_name (str): The name of the class to be deleted.
        """
        return self.Model._delete_class(class_name)
        
    # Rename class interface #
    def rename_class(self, current_name: str, new_name: str):
        """
        Renames a UML class by delegating the operation to the model.

        Parameters:
            current_name (str): The current name of the class.
            new_name (str): The new name for the class.
        """
        return self.Model._rename_class(current_name, new_name)
        
    ## FIELD RELATED ##
    
    # Add field interface #
    def add_field(self, class_name: str, type: str, field_name: str):
        """
        Adds a field to a UML class by delegating the operation to the model.

        Parameters:
            class_name (str): The name of the class.
            field_name (str): The name of the field to be added.
        """
        return self.Model._add_field(class_name, type, field_name)
        
    # Delete field interface #
    def delete_field(self, class_name: str, field_name: str):
        """
        Deletes a field from a UML class by delegating the operation to the model.

        Parameters:
            class_name (str): The name of the class.
            field_name (str): The name of the field to be deleted.
        """
        return self.Model._delete_field(class_name, field_name)
    
    # Rename field interface #
    def rename_field(self, class_name: str, current_field_name: str, new_field_name: str, current_type=None, new_type=None):
        """
        Renames a field in a UML class by delegating the operation to the model.

        Parameters:
            class_name (str): The name of the class.
            current_field_name (str): The current name of the field.
            new_field_name (str): The new name for the field.
        """
        if current_type and new_type:
            return self.Model._rename_field(class_name, current_field_name, new_field_name, current_type, new_type)
        return self.Model._rename_field(class_name, current_field_name, new_field_name)
        
    # Get chosen field #
    def get_chosen_field_or_method(self, class_name: str, field_name: str, is_field: bool):
        return self.Model._get_chosen_field_or_method(class_name, field_name, is_field)
    
    ## METHOD RELATED ##
    
    # Add method interface #
    def add_method(self, class_name: str, type: str, method_name: str):
        """
        Adds a method to a UML class by delegating the operation to the model.

        Parameters:
            class_name (str): The name of the class.
            method_name (str): The name of the method to be added.
        """
        return self.Model._add_method(class_name, type, method_name)
    
    # Delete method interface #
    def delete_method(self, class_name: str, method_num: int):
        """
        Deletes a method from a UML class by delegating the operation to the model.

        Parameters:
            class_name (str): The name of the class.
            method_name (str): The name of the method to be deleted.
        """
        return self.Model._delete_method(class_name, method_num)
        
    # Rename method interface #
    def rename_method(self, class_name: str, method_num: int, new_name: str):
        """
        Renames a method in a UML class by delegating the operation to the model.

        Parameters:
            class_name (str): The name of the class.
            current_method_name (str): The current name of the method.
            new_method_name (str): The new name for the method.
        """
        return self.Model._rename_method(class_name, method_num, new_name)
        
    ## PARAMETER RELATED ##
    
    # Add parameter interface #
    def add_parameter(self, class_name: str = None, method_num: int = None, param_type: str = None, param_name: str = None):
        """
        Adds a parameter to a UML method by delegating the operation to the model.

        Parameters:
            class_name (str): The name of the class.
            method_name (str): The name of the method.
            parameter_name (str): The name of the parameter to be added.
        """
        return self.Model._add_parameter(class_name, method_num, param_type, param_name)
        
    # Delete parameter interface #
    def delete_parameter(self, class_name: str,  method_num: str, param_name: str):
        """
        Deletes a parameter from a UML method by delegating the operation to the model.

        Parameters:
            class_name (str): The name of the class.
            method_name (str): The name of the method.
            parameter_name (str): The name of the parameter to be deleted.
        """
        return self.Model._delete_parameter(class_name, method_num, param_name)
        
    # Rename parameter interface #
    def rename_parameter(self, class_name: str,  method_num: str, current_param_name: str, new_param_name: str):
        """
        Renames a parameter in a UML method by delegating the operation to the model.

        Parameters:
            class_name (str): The name of the class.
            method_name (str): The name of the method.
            current_parameter_name (str): The current name of the parameter.
            new_parameter_name (str): The new name for the parameter.
        """
        return self.Model._rename_parameter(class_name, method_num, current_param_name, new_param_name)
        
    # Replace parameter list interface #
    def replace_param_list(self, class_name: str, method_num: str, new_param_list: list):
        """
        Replaces the parameter list of a UML method by delegating the operation to the model.

        Parameters:
            class_name (str): The name of the class.
            method_name (str): The name of the method.
        """
        return self.Model._replace_param_list(class_name, method_num, new_param_list)
    
    # Replace parameter list interface for GUI #
    def replace_param_list_gui(self, class_name: str, method_name: str, new_param_list: List):
        """
        Replaces the parameter list of a UML method by delegating the operation to the model.

        Parameters:
            class_name (str): The name of the class.
            method_name (str): The name of the method.
        """
        return self.Model._replace_param_list_gui(class_name, method_name, new_param_list)
        
    ## RELATIONSHIP RELATED ##
    
    # Add relationship interface for CLI#
    def add_relationship_cli(self, source_class_name: str, destination_class_name: str, rel_type: str):
        """
        Adds a relationship between two UML classes by delegating the operation to the model.

        Parameters:
            source_class_name (str): The name of the source class.
            destination_class_name (str): The name of the destination class.
            type (str): The type of relationship.
        """
        return self.Model._add_relationship(source_class_name=source_class_name, destination_class_name=destination_class_name, rel_type=rel_type, is_gui=False)
    
    # Add relationship interface for GUI#
    def add_relationship_gui(self, source_class_name: str, destination_class_name: str, type: str):
        """
        Adds a relationship between two UML classes by delegating the operation to the model.

        Parameters:
            source_class_name (str): The name of the source class.
            destination_class_name (str): The name of the destination class.
            type (str): The type of relationship.
        """
        return self.Model._add_relationship(source_class_name=source_class_name, destination_class_name=destination_class_name, rel_type=type, is_gui=True)
    
    # Delete relationship interface #
    def delete_relationship(self, source_class_name: str, destination_class_name: str):
        """
        Deletes a relationship between two UML classes by delegating the operation to the model.

        Parameters:
            source_class_name (str): The name of the source class.
            destination_class_name (str): The name of the destination class.
        """
        return self.Model._delete_relationship(source_class_name, destination_class_name)
        
    # Change relationship type interface #
    def change_type(self, source_class_name: str, destination_class_name: str, new_type: str):
        """
        Changes the type of a relationship between two UML classes by delegating the operation to the model.

        Parameters:
            source_class_name (str): The name of the source class.
            destination_class_name (str): The name of the destination class.
            new_type (str): The new type of relationship.
        """
        return self.Model._change_type(source_class_name, destination_class_name, new_type)
    
    def change_data_type(self, 
                    class_name: str=None, method_num:int = None, 
                    input_name: str=None, source_class: str=None,
                    dest_class: str=None, new_type: str=None, 
                    is_field: bool=None,is_method: bool=None, 
                    is_param: bool=None, is_rel: bool=None):
        return self.Model._change_data_type(class_name=class_name, input_name=input_name, 
                                            source_class=source_class, dest_class=dest_class, 
                                            new_type=new_type, is_field=is_field, is_method=is_method, 
                                            is_param=is_param, is_rel=is_rel, method_num=method_num)
    
    ## SAVE/LOAD RELATED ##
    
    # Save data #
    def save(self):
        """
        Saves the current UML diagram data by delegating the operation to the model.
        """
        self.Model._save()
        
    # Save data GUI #
    def save_gui(self, file_name, file_path):
        """
        Saves the UML diagram data to a specified file and path for GUI-based saving.

        Parameters:
            file_name: The name of the file to save.
            file_path: The path where the file will be saved.
        """
        self.Model._save_gui(file_name, file_path)
        
    # Load data #
    def load(self):
        """
        Loads the UML diagram data by delegating the operation to the model.
        """
        self.Model._load()
        
    # Load data GUI #
    def load_gui(self, file_name, file_path, graphical_view):
        self.Model._load_gui(file_name, file_path, graphical_view)
    
    # Delete saved file #
    def delete_saved_file(self):
        """
        Deletes a saved UML file by delegating the operation to the model.
        """
        self.Model._delete_saved_file()
        
    # Get active file #
    def get_active_file(self) -> str:
        """
        Retrieves the name of the currently active file in the UML editor.

        Returns:
            str: The name of the active file.
        """
        return self.Model._get_active_file()
    
    # Get active file GUI #
    def get_active_file_gui(self) -> str:
        """
        Retrieves the name of the currently active file in the UML editor.

        Returns:
            str: The name of the active file.
        """
        return self.Model._get_active_file_gui()
    
    # Saved file name check #
    def saved_file_name_check(self, file_name: str) -> bool:
        """
        Checks if the provided file name already exists in the saved files.

        Parameters:
            file_name (str): The name of the file to check.

        Returns:
            bool: True if the file name exists, False otherwise.
        """
        return self.Model._saved_file_name_check(file_name)
    
    # Clear current active data #
    def clear_current_active_data(self):
        """
        Clears the current UML data in the active session by delegating the operation to the model.
        """
        self.Model._clear_current_active_data()
    
    # Go back to blank program #
    def new_file(self):
        """
        Ends the current session and resets the program to a blank state by delegating the operation to the model.
        """
        self.Model._new_file()
        
    # Sort class list #
    def sort_class_list(self):
        """
        Sorts the list of UML classes alphabetically by delegating the operation to the model.
        """
        self.Model._sort_class_list()
        
    # Exit program #
    def exit(self):
        """
        Exits the UML program by delegating the operation to the model.
        """
        self.Model._exit()
        
    # Keep updating main data #
    def update_main_data_for_every_action(self):
        """
        Ensures the main data is updated after every action by delegating the operation to the model.
        """
        self.Model._update_main_data_for_every_action()
        
    ## OBSERVER RELATED ##
    
    # Attach observer
    def attach_observer(self, observer):
        """
        Attaches an observer to the model for the observer pattern implementation.

        Parameters:
            observer: The observer to attach.
        """
        self.Model._attach_observer(observer)
        
    # Detach observer
    def detach_observer(self, observer):
        """
        Detaches an observer from the model for the observer pattern implementation.

        Parameters:
            observer: The observer to detach.
        """
        self.Model._detach_observer(observer)
        
    # Notify observer
    def notify_observer(self):
        """
        Notifies all observers of changes in the model for the observer pattern implementation.
        """
        self.Model._notify_observer()
    
    # Check for valid input
    def is_valid_input(self, class_name=None, field_name=None, 
                        method_name=None, parameter_name=None, 
                        source_class=None, destination_class=None, 
                        type=None, new_name=None):
        """
        Check if the user input contains only letters, numbers, and underscores for all provided parameters.

        Parameters:
            class_name (str, optional): The name of the class to validate.
            field_name (str, optional): The name of the field to validate.
            method_name (str, optional): The name of the method to validate.
            parameter_name (str, optional): The name of the parameter to validate.
            source_class (str, optional): The source class name to validate.
            destination_class (str, optional): The destination class name to validate.
            type (str, optional): The type of relationship.
            new_name (str, optional): The new name to validate (e.g., for renaming a class).

        Returns:
            bool: True if all provided inputs are valid (contain only a-z, A-Z, 0-9, and _), False otherwise.
        """
        return self.Model._is_valid_input(class_name=class_name, field_name=field_name,
                                          method_name=method_name, parameter_name=parameter_name,
                                          source_class=source_class, destination_class=destination_class,
                                          type=type, new_name=new_name)
        
    #################################################################
    
    ## USER INTERFACE ##
    
    # Main program loop #
    def main_program_loop(self):
        """
        The main program loop for interacting with the user. It continuously prompts the user for commands, processes
        those commands via the controller, and displays the appropriate output. This method also handles the help and
        exit commands, displaying a menu or terminating the program accordingly.
        """
        # Display a welcome message and help menu
        self.View._prompt_menu()  # Show initial instructions
        while True:
            # Display the current active file in the interface
            current_active_file: str = self.get_active_file()
            if current_active_file != "No active file!":
                current_active_file = current_active_file + ".json"
            self.Console.print(f"\n[bold yellow](Current active file: [bold white]{current_active_file}[/bold white])[/bold yellow]")
            # self.Console.print("\n[bold yellow]==>[/bold yellow] ", end="")
            
            # Collect input from the user
            user_input: str = self.session.prompt(HTML("<b><style color='#fdca5b'>==></style></b> ")).strip()
            user_input_component = user_input.split()  # Split the input by space

            # Parse command and parameters
            if len(user_input_component) == 0:
                continue
            command = user_input_component[0]
            parameters = user_input_component[1:]
            
            # Handle the 'help' command to show the menu again
            if command == InterfaceOptions.HELP.value:
                self.View._prompt_menu()
            # Handle the 'exit' command to break out of the loop
            elif command == InterfaceOptions.EXIT.value:
                break
            # Pass command and parameters to the controller for processing
            self.Controller._process_command(command, parameters)
        
        # Exit the program after the loop ends
        self.exit()

###################################################################################################