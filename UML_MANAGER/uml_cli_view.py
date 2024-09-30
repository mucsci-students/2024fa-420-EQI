###################################################################################################

from rich.console import Console
from rich.tree import Tree
from rich.table import Table
from rich.panel import Panel
from rich.box import SQUARE
from enum import Enum
from typing import List, Dict

###################################################################################################
### ENUM FOR RELATIONSHIP TYPE ###

class RelationshipType(Enum):
    AGGREGATION = "aggregation"
    COMPOSITION = "composition"
    INHERITANCE = "inheritance"
    REALIZATION = "realization"

# UMLView class for displaying UML data
class UMLView:

    def __init__(self):
        self.console = Console()
        
    def _get_enum_list(self):
        return RelationshipType
        
    # Display the menu
    def _prompt_menu(self):
        banner = r"""[bold yellow]
    ▗▖ ▗▖▗▖  ▗▖▗▖       ▗▄▄▄▖▗▄▄▄ ▗▄▄▄▖▗▄▄▄▖▗▄▖ ▗▄▄▖ 
    ▐▌ ▐▌▐▛▚▞▜▌▐▌       ▐▌   ▐▌  █  █    █ ▐▌ ▐▌▐▌ ▐▌
    ▐▌ ▐▌▐▌  ▐▌▐▌       ▐▛▀▀▘▐▌  █  █    █ ▐▌ ▐▌▐▛▀▚▖
    ▝▚▄▞▘▐▌  ▐▌▐▙▄▄▖    ▐▙▄▄▖▐▙▄▄▀▗▄█▄▖  █ ▝▚▄▞▘▐▌ ▐▌
                                             
        
        Welcome to the UML Management Interface!
    For more information on commands, type "help" for the manual.
        [bold yellow]"""
        # Create a list of commands with their descriptions
        commands = [
            ["[bold yellow]Class Commands[/bold yellow]", ""],
            ["add_class [bright_white]<class_name>[bright_white]", "Add a new class"],
            ["delete_class [bright_white]<class_name>[bright_white]", "Delete an existing class"],
            ["rename_class [bright_white]<class_name> <new_name>[bright_white]", "Rename a class"],

            ["[bold yellow]Field Commands[/bold yellow]", ""],
            ["add_field [bright_white]<class_name> <attr_name>[bright_white]", "Add a field to a class"],
            ["delete_field [bright_white]<class_name> <field_name>[bright_white]", "Delete a field from a class"],
            ["rename_field [bright_white]<class_name> <current_field_name> <new_name>[bright_white]", "Rename a field"],

            ["[bold yellow]Method Commands[/bold yellow]", ""],
            ["add_method [bright_white]<class_name> <method_name>[bright_white]", "Add a method to a class"],
            ["delete_method [bright_white]<class_name> <method_name>[bright_white]", "Delete a method from a class"],
            ["rename_method [bright_white]<class_name> <current_method_name> <new_name>[bright_white]", "Rename a method"],

            ["[bold yellow]Parameter Commands[/bold yellow]", ""],
            ["add_param [bright_white]<class_name> <method_name> <param_name>[bright_white]", "Add a parameter to a method"],
            ["delete_param [bright_white]<class_name> <method_name> <param_name>[bright_white]", "Delete a parameter from a method"],
            ["rename_param [bright_white]<class_name> <method_name> <current_param_name> <new_name>[bright_white]", "Rename a parameter"],
            ["replace_param [bright_white]<class_name> <method_name>[bright_white]", "Replace a method's parameter list"],

            ["[bold yellow]Relationship Commands[/bold yellow]", ""],
            ["add_rel [bright_white]<source_class> <destination_class> <relationship_type>[bright_white]", "Add a relationship between two classes"],
            ["delete_rel [bright_white]<source_class> <destination_class>[bright_white]", "Delete a relationship between two classes"],
            ["type_mod [bright_white]<source_class> <destination_class> <type>[bright_white]", "Modify the type of a relationship"],

            ["[bold yellow]Class-Related Commands[/bold yellow]", ""],
            ["list_class", "List all created classes"],
            ["class_detail [bright_white]<class_name>[bright_white]", "View details of a specific class"],
            ["class_rel", "View relationships between classes"],

            ["[bold yellow]Save/Load Commands[/bold yellow]", ""],
            ["saved_list", "List all saved files"],
            ["save", "Save current data"],
            ["load", "Load data from a saved file"],
            ["delete_saved", "Delete a saved file"],
            ["clear_data", "Clear all data from current storage"],
            ["default", "Reset to a blank program"],

            ["[bold yellow]Other Commands[/bold yellow]", ""],
            ["sort", "Sort the class list alphabetically"],
            ["help", "View instructions"],
            ["exit", "Exit the program"]
        ]
        # Create a table to organize commands and descriptions
        table = Table(title=banner, show_header=True, header_style="bold yellow", border_style="bold dodger_blue2", box=SQUARE)
        table.add_column(f"{'Command':^75}", style="bold dodger_blue2", justify="left", no_wrap=True)
        table.add_column(f"{'Description':^45}", style="bold bold white")
        # Add rows to the table
        for command, description in commands:
            table.add_row(command, description)
        # Create a panel to wrap the table with a welcome message
        panel = Panel.fit(table, border_style="bold dodger_blue2")
        # Print the panel with the commands
        self.console.print(panel)
        
    def _display_wrapper(self, main_data: Dict):
        if len(main_data["classes"]) == 0:
            print("\nNo class to display!")
            return
        is_detail = self._ask_user_choices("print all class detail")
        if is_detail:
            self._display_uml_data(main_data)
        else:
            self._display_class_names(main_data)

    # Display all class detail
    def _display_uml_data(self, main_data: Dict):
        # Main tree to hold UML structure
        tree = Tree("\nUML Classes and Relationships")
        # Add classes to the tree
        classes_tree = tree.add("Classes")
        for cls in main_data["classes"]:
            class_branch = classes_tree.add(f'[bold green]{cls["name"]}[/bold green]')
            self._display_class(class_branch, cls)
        # Add relationships to the tree
        relationships_tree = tree.add("Relationships")
        for relation in main_data["relationships"]:
            relationships_tree.add(
                f'[bold dodger_blue2]{relation["source"]}[/bold dodger_blue2] --{relation["type"]}--> [bold dodger_blue2]{relation["destination"]}[/bold dodger_blue2]'
            )
        # Print the complete tree
        self.console.print(tree)

    # Structure the class detail into branches
    def _display_class(self, class_branch, cls):
        # Add fields of the class
        fields_branch = class_branch.add("[bold yellow]Fields[/bold yellow]")
        for field in cls["fields"]:
            fields_branch.add(f'[bold cyan]{field["name"]}[/bold cyan]')
        # Add methods of the class
        methods_branch = class_branch.add("[bold yellow]Methods[/bold yellow]")
        for method in cls["methods"]:
            # Extract the names of the parameters
            params = ', '.join(param["name"] for param in method["params"])
            methods_branch.add(f'[magenta]{method["name"]}({params})[/magenta]')
    
    # Display class names
    def _display_class_names(self, main_data: Dict):
        # Create a table to display all class names
        table = Table(title="\n[bold white]Class Names[/bold white]", show_header=True, header_style="bold yellow", border_style="bold dodger_blue2")
        table.add_column("Class Name", justify="center", style="bold white")
        # Iterate through all classes and add their names to the table
        for cls in main_data["classes"]:
            table.add_row(cls["name"])
        # Print the table with the class names
        self.console.print(table)
        
    # Display single class detail
    def _display_single_class(self, class_name: str, main_data: Dict):
        # Main tree to hold UML structure
        tree = Tree("\nUML Classes and Relationships")
        # Add classes to the tree
        classes_tree = tree.add("Class")
        for cls in main_data["classes"]:
            if cls["name"] == class_name:
                class_branch = classes_tree.add(f'[bold green]{cls["name"]}[/bold green]')
                self._display_class(class_branch, cls)
        # Add relationships to the tree
        relationships_tree = tree.add("Relationships")
        for relation in main_data["relationships"]:
            if relation["source"] == class_name or relation["destination"] == class_name:
                relationships_tree.add(
                    f'[bold blue]{relation["source"]}[/bold blue] --{relation["type"]}--> [bold blue]{relation["destination"]}[/bold blue]'
                )
        # Print the complete tree
        self.console.print(tree)
        
    # Display relationship
    def _display_relationships(self, main_data):
        # Create a table to display all relationships
        table = Table(title="\n[bold white]Relationships[/bold white]", show_header=True, header_style="bold yellow", border_style="bold dodger_blue2")
        table.add_column("Source Class", style="bold white")
        table.add_column("Relationship Type", style="bold green")
        table.add_column("Destination Class", style="bold white")
        # Iterate through all relationships and add them to the table
        for relation in main_data["relationships"]:
            table.add_row(
                relation["source"],
                relation["type"],
                relation["destination"]
            )
        # Print the table with relationships
        self.console.print(table)
    
    # Display type for relationship
    def _display_type_enum(self):
        # Create a table to display relationship types
        table = Table(title="\n[bold white]Relationship Types[/bold white]", show_header=True, header_style="bold yellow", border_style="bold dodger_blue2")
        table.add_column("Type", justify="center", style="bold white")
        # Iterate through the RelationshipType enum and add each type to the table
        for type_ in RelationshipType:
            table.add_row(type_.value)
        # Print the table with the relationship types
        self.console.print(table)
        
    # Display saved file's names using Rich
    def _display_saved_list(self, saved_list: List):
        # Check if there are any saved files
        if len(saved_list) == 0:
            self.console.print("\n[bold red]No saved file exists![/bold red]")
            return
        # Create a table to display saved file names
        table = Table(title="\n[bold white]Saved Files[bold white]", show_header=True, header_style="bold yellow", border_style="bold dodger_blue2")
        table.add_column("File Name", justify="center", style="bold white")
        # Iterate through saved_list and add each file name to the table
        for dictionary in saved_list:
            for key in dictionary:
                table.add_row(key)
        # Print the table with saved file names
        self.console.print(table)
            
    # Ask For User Choices #
    def _ask_user_choices(self, action: str) -> bool:
        while True:
            user_input = input(f"\nDo you want to {action}? (Yes/No): ").lower()
            if user_input in ["yes", "y"]:
                return True
            elif user_input in ["no", "n"]:
                return False
            else:
                print("Invalid input. Please enter 'Yes' or 'No'.")
                
################################################################################################### 
            