################################################################
#   Author : Quang Bui
#   Created: September 12, 2024
#
#   This file is for the CLI
################################################################

from enum import Enum

import UML_CORE.UML_CLASS.uml_class as UML_MANAGER
import UML_UTILITY.SAVE_LOAD.save_load as SAVE_LOAD


class InterfaceOptions(Enum):
    WORK = "work"
    LIST_CLASS = "list_class"
    CLASS_DETAIL = "class_detail"
    CLASS_REL = "class_rel"
    SAVE = "save"
    SORT = "sort"
    SHOW_MENU = "show_menu"
    HELP = "help"
    EXIT = "exit"


class UMLClassInterfaceOption(Enum):
    ADD_CLASS = "add_class"
    DELETE_CLASS = "delete_class"
    RENAME = "rename_class"
    ADD_ATTR = "add_attr"
    DELETE_ATTR = "delete_attr"
    RENAME_ATTR = "rename_attr"
    ADD_REL = "add_rel"
    DELETE_REL = "delete_rel"
    SHOW_MENU = "show_menu"
    BACK = "back"


def prompt_main_menu():
    print("Welcome To Our UML Program!")
    print("Type 'work' start working with class(es)")
    print("Type 'list_class' to see the list of all created class(es)")
    print("Type 'class_detail <class_name>' to see the detail of the chosen class")
    print(
        "Type 'class_rel <class_name>' to see the relationships between the chosen class and other class(es)"
    )
    print("Type 'save' to save data")
    print("Type 'sort' to sort the class list in alphabetical order")
    print("Type 'show_menu' to see the menu again")
    print("Type 'help' to see the instructions")
    print("Type 'exit' to quit program")


def prompt_working_menu():
    # Class
    print("Type 'add_class <class_name>' to add a class")
    print("Type 'delete_class <class_name>' to delete a class")
    print("Type 'rename_class <class_name> <new_name>' to rename a class")
    # Attribute
    print(
        "Type 'add_attr <class_name> <access_specifier> <data_type> <attr_name>' to add an attribute"
    )
    print(
        "Type 'delete_attr <class_name> <attr_name>' to delete an attribute from the chosen class"
    )
    print(
        "Type 'rename_attr <attr_name> <current_attribute_name> <new_name>' to rename an attribute"
    )
    # Relationship
    print(
        "Type 'add_rel <source_class> <destination_class_name> <relationship_level>' to add relationship and relationship level"
    )
    print(
        "Type 'delete_rel <chosen_class_name> <destination_class_name>' to delete a relationship"
    )
    print("Type 'show_menu' to see the menu again")
    print("Type 'back' to go back to main menu'")


def working_loop():
    prompt_working_menu()
    while True:
        print("\n==> ", end="")
        user_input: str = input()
        # Split the input by space
        user_input_component = user_input.split()
        # Get separate command and class name part
        command = user_input_component[0]
        first_param = user_input_component[1] if len(user_input_component) > 1 else None
        second_param = (
            user_input_component[2] if len(user_input_component) > 2 else None
        )
        # third_param = user_input_component[3] if len(user_input_component) > 3 else None
        # fourth_param = (
        #     user_input_component[4] if len(user_input_component) > 4 else None
        # )
        # Start the logic
        #######################################################
        # Add class
        if command == UMLClassInterfaceOption.ADD_CLASS.value and first_param:
            UML_MANAGER.add_class(first_param)
        # Delete class
        elif command == UMLClassInterfaceOption.DELETE_CLASS.value and first_param:
            UML_MANAGER.delete_class(first_param)
        # Rename class
        elif (
            command == UMLClassInterfaceOption.RENAME.value
            and first_param
            and second_param
        ):
            UML_MANAGER.rename_class(first_param, second_param)

        #######################################################

        # Add attribute

        # Delete attribute

        #######################################################

        # Add relationship

        # Delete relationship

        #######################################################
        # See menu again
        elif command == UMLClassInterfaceOption.SHOW_MENU.value:
            prompt_working_menu()
        #######################################################
        # Go back to main menu
        elif command == UMLClassInterfaceOption.BACK.value:
            prompt_main_menu()
            break
        else:
            print(
                "Unknown command or wrong argument, see the instruction for more details"
            )


def main_program_loop():
    prompt_main_menu()
    while True:
        print("\n==> ", end="")
        user_input: str = input()
        # Split the input by space
        user_input_component = user_input.split()
        command = user_input_component[0]
        # Check if command has an associated class name
        first_param = user_input_component[1] if len(user_input_component) > 1 else None
        # Go to the working menu
        if command == InterfaceOptions.WORK.value:
            working_loop()
        # # List all the created class names
        elif command == InterfaceOptions.LIST_CLASS.value:
            display_class_list()
        # # Show the details of the chosen class
        elif command == InterfaceOptions.CLASS_DETAIL.value and first_param:
            display_class_detail(first_param)
        #######################################################
        # # Show the relationship of the chosen class with others
        # elif command == InterfaceOptions.CLASS_REL.value and first_param:
        #     class_rel(first_param)
        #######################################################
        # Show the instructions for this program
        elif command == InterfaceOptions.HELP.value:
            help()
        # Sort the class list
        elif command == InterfaceOptions.SORT.value:
            sort_class_list()
        # Save the data
        elif command == InterfaceOptions.SAVE.value:
            SAVE_LOAD.save_data_from_json(UML_MANAGER.data_list, "data.json")
        # Show the main menu again
        elif command == UMLClassInterfaceOption.SHOW_MENU.value:
            prompt_main_menu()
        # Exit the program
        elif command == InterfaceOptions.EXIT.value:
            break
        else:
            print(
                f"Unknown command '{user_input}'. Type 'help' for a list of commands."
            )
    exit()


########################################################################################################
# MAIN MENU #
def class_rel(class_name: str):
    print("Inside relationship\n")


def help():
    print("Inside help\n")


def exit():
    print("Exited Program")


########################################################################################################


# Display Class List #
def display_class_list():
    print("\n===================")
    print("--Class List--")
    for class_name in UML_MANAGER.class_list:
        print(class_name)
    print("===================")


# Display Class Details #
def display_class_detail(class_name: str):
    class_object = UML_MANAGER.get_chosen_class(class_name)
    print("\n===================")
    print("--Class Name--")
    print(f"{class_object['class_name']}")  # Center with 20 spaces
    print("*******************")
    attr_list = class_object["attr_list"]
    print("--Class Attribute--")
    for element in attr_list:
        for key, val in element.items():
            print(f"{val}")
    print("===================")


# Sorting Class List #
def sort_class_list():
    UML_MANAGER.class_list.sort()
    display_class_list()
