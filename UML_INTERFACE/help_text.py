import pydoc  # For cross-platform paging

help_text = """
*** NAME ***
    UML Management Interface - A tool for managing UML classes and fields.

*** DESCRIPTION ***
    This program allows users to effectively manage UML classes along with 
    their attributes, methods, and relationships. It provides commands to 
    add, delete, and rename classes, attributes, methods, and relationships.
    Users can also perform file operations to save, load, and clear data, 
    making it suitable for maintaining UML diagrams and documentation in a 
    structured manner.

    **Note:** Allowed characters for names (classes, fields, methods) are 
    [a-zA-Z0-9_].


*** COMMANDS ***

    Manage Classes:
        add_class <class_name>
            Add a new class with the specified name.

        delete_class <class_name>
            Delete the specified class.

        rename_class <old_class_name> <new_name>
            Rename a class from the old name to the new name.


    Manage field:
        add_field <class_name> <field_name>
            Add a new field to the specified class.

        delete_field <class_name> <field_name>
            Delete the specified field from the chosen class.

        rename_field <class_name> <current_field_name> <new_field_name>
            Rename an field within the specified class.

            
    Manage method:
        add_method <class_name> <method_name>
            Add a new method to the specified class.

        delete_method <class_name> <method_name>
            Delete the specified method from the chosen class.

        rename_method <class_name> <current_method_name> <new_method_name>
            Rename an method within the specified class.

            
    Manage Relationships:
        add_rel <source_class> <destination_class_name> <relationship_level>
            Add a relationship from the source class to the destination class with the specified relationship level.

        delete_rel <chosen_class_name> <destination_class_name>
            Delete the relationship between the chosen class and the specified destination class.

            
    File Operations:
        saved_list
            Show the list of saved files.

        save
            Save current data.

        load
            Load data from saved files.

        delete_saved
            Delete a saved file.

        clear_data
            Delete all data in the current storage.

        default
            Go back to a blank program state.

            
    Miscellaneous:
        list_class
            Display the list of all created class(es).

        class_detail <class_name>
            Show the detail of the specified class.

        class_rel <class_name>
            Show the relationship of a specified class.

        help
            Display this help text.

        sort
            Sort the class list in alphabetical order.

        exit
            Quit the program.

*** SEE ALSO ***
    For more information, refer to the README.md documentation on our github.

"""

def show_help():
    """Display the help text directly."""
    print(help_text)

def show_manual():
    """Display the manual with pagination."""
    manual_text = "Press 'q' to exit manual.\n\n" + help_text
    pydoc.pager(manual_text)

# Usage example
if __name__ == "__main__":
    show_manual()
