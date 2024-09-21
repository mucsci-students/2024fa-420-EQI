"""
Author : Quang Bui
Created: September 12, 2024

Description:
    Command Line User Interface

List of last date modified:
- September 15, 2024 (By Quang)
- September 20, 2024 (By Quang)
- September 21, 2024 (By Quang)

"""
########################################################################################################

import UML_MANAGER.uml_manager as UML_MANAGER

########################################################################################################

def working_loop():
    UML_MANAGER.prompt_working_menu()
    while True:
        current_active_file: str = UML_MANAGER.get_active_file()
        print(f"\n(Work-Menu) - (Current active file: {current_active_file})\n")
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
        third_param = user_input_component[3] if len(user_input_component) > 3 else None
        # Start the logic
        #################################################### ###
        # Add class
        if command == UML_MANAGER.UMLClassInterfaceOption.ADD_CLASS.value and first_param:
            UML_MANAGER.UML_CLASS.add_class(first_param)
        # Delete class
        elif command == UML_MANAGER.UMLClassInterfaceOption.DELETE_CLASS.value and first_param:
            UML_MANAGER.UML_CLASS.delete_class(first_param)
        # Rename class
        elif (
            command == UML_MANAGER.UMLClassInterfaceOption.RENAME.value
            and first_param
            and second_param
        ):
            UML_MANAGER.UML_CLASS.rename_class(first_param, second_param)

        #######################################################

        # Add attribute
        elif (
            command == UML_MANAGER.UMLClassInterfaceOption.ADD_ATTR.value
            and first_param
            and second_param
        ):
            UML_MANAGER.UML_ATTRIBUTE.add_attr(first_param, second_param)
        # Delete attribute
        elif (
            command == UML_MANAGER.UMLClassInterfaceOption.DELETE_ATTR.value
            and first_param
            and second_param
        ):
            UML_MANAGER.UML_ATTRIBUTE.delete_attr(first_param, second_param)
        # Rename attribute
        elif (
            command == UML_MANAGER.UMLClassInterfaceOption.RENAME_ATTR.value
            and first_param
            and second_param
            and third_param
        ):
            UML_MANAGER.UML_ATTRIBUTE.rename_attr(first_param, second_param, third_param)

        #######################################################

        # Add relationship
        elif (
            command == UML_MANAGER.UMLClassInterfaceOption.ADD_REL.value
            and first_param
            and second_param
            and third_param
        ):
            UML_MANAGER.UML_REL.add_relationship(first_param, second_param, third_param)
        # Delete relationship
        elif (
            command == UML_MANAGER.UMLClassInterfaceOption.DELETE_REL.value
            and first_param
            and second_param
        ):
            UML_MANAGER.UML_REL.remove_relationship(first_param, second_param)

        #######################################################
        # See menu again
        elif command == UML_MANAGER.UMLClassInterfaceOption.HELP.value:
            UML_MANAGER.prompt_working_menu()
        #######################################################
        # Go back to main menu
        elif command == UML_MANAGER.UMLClassInterfaceOption.BACK.value:
            UML_MANAGER.prompt_main_menu()
            break
        else:
            print(
                "Unknown command or wrong argument, see the instruction for more details"
            )


def main_program_loop():
    UML_MANAGER.prompt_main_menu()
    while True:
        current_active_file: str = UML_MANAGER.get_active_file()
        print(f"\n(Main-Menu) - (Current active file: {current_active_file})\n")
        print("\n==> ", end="")
        user_input: str = input()
        # Split the input by space
        user_input_component = user_input.split()
        command = user_input_component[0]
        # Check if command has an associated class name
        first_param = user_input_component[1] if len(user_input_component) > 1 else None
        # Go to the working menu
        if command == UML_MANAGER.InterfaceOptions.WORK.value:
            working_loop()
        # List all the created class names or all class detail
        elif command == UML_MANAGER.InterfaceOptions.LIST_CLASS.value:
            UML_MANAGER.display_wrapper()
        # Show the details of the chosen class
        elif command == UML_MANAGER.InterfaceOptions.CLASS_DETAIL.value and first_param:
            UML_MANAGER.display_single_class_detail(first_param)
        # Show the relationship of the chosen class with others
        elif command == UML_MANAGER.InterfaceOptions.CLASS_REL.value:
            UML_MANAGER.display_relationship_wrapper()
        # Show the list of saved files
        elif command == UML_MANAGER.InterfaceOptions.SAVED_LIST.value:
            UML_MANAGER.display_saved_file_name()
        # Save the data
        elif command == UML_MANAGER.InterfaceOptions.SAVE.value:
            UML_MANAGER.saving_file_wrapper()
        # Load the data
        elif command == UML_MANAGER.InterfaceOptions.LOAD.value:
            UML_MANAGER.loading_file_wrapper()
        # Delete saved file
        elif command == UML_MANAGER.InterfaceOptions.DELETE_SAVED.value:
            UML_MANAGER.delete_saved_file_wrapper()
        # Clear data in current storage
        elif command == UML_MANAGER.InterfaceOptions.CLEAR_DATA.value:
            UML_MANAGER.clear_current_data()
        # Go back to blank program
        elif command == UML_MANAGER.InterfaceOptions.DEFAULT.value:
            UML_MANAGER.end_session()
        # Sort the class list
        elif command == UML_MANAGER.InterfaceOptions.SORT.value:
            UML_MANAGER.sort_class_list()
        # Show the main menu again
        elif command == UML_MANAGER.InterfaceOptions.HELP.value:
            UML_MANAGER.prompt_main_menu()
        # Exit the program
        elif command == UML_MANAGER.InterfaceOptions.EXIT.value:
            break
        else:
            print(
                f"Unknown command '{user_input}'. Type 'help' for a list of commands."
            )
    UML_MANAGER.exit()
    

########################################################################################################