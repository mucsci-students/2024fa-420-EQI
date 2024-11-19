###################################################################################################
# Import necessary modules from PyQt5 and custom UML classes
###################################################################################################

from PyQt5 import uic
from PyQt5 import QtWidgets
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_canvas import UMLGraphicsView as GUICanvas
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_class_box import UMLClassBox
from UML_MVC.uml_observer import UMLObserver as Observer

###################################################################################################

class MainWindow(QtWidgets.QMainWindow, Observer):
    """
    Main application window that loads the UI and sets up interactions for the UML diagram editor.
    
    Inherits from QMainWindow for managing the graphical interface and from Observer to receive updates
    from the core UML system. This class implements the Singleton pattern to ensure only one instance
    of the main window exists.
    
    Attributes:
        interface: The interface to communicate with UMLCoreManager (business logic layer).
        grid_view (GUICanvas): The canvas where UML class boxes and relationships are displayed.
        box (UMLClassBox): An instance of a UML class box.
    """
    
    _instance = None  # Class variable to hold the single instance

    def __new__(cls, *args, **kwargs):
        """
        Implement the Singleton pattern to ensure only one instance of MainWindow is created.
        """
        if cls._instance is None:
            cls._instance = super(MainWindow, cls).__new__(cls)
        else:
            raise RuntimeError("Only one instance of MainWindow is allowed!")
        return cls._instance

    def __init__(self, interface):
        """
        Initializes a new MainWindow instance, loading the GUI and setting up the interface.

        Parameters:
            interface: The interface to communicate with UMLCoreManager (business logic layer).
        """
        super().__init__()
        
        # Prevent reinitialization if already initialized
        if hasattr(self, 'initialized'):
            return
        
        self.initialized = True  # Mark as initialized
        
        self.interface = interface  # Interface to communicate with UMLCoreManager

        # Load the UI file to set up the layout and widgets of the main window
        uic.loadUi('prototype_gui.ui', self)

        # Create a grid view where UML class boxes and relationships will be displayed
        self.grid_view = GUICanvas(self.interface)
        self.grid_view.set_grid_visible(False)  # Initially hide the grid lines
        self.setCentralWidget(self.grid_view)   # Set the grid view as the central widget
        self.box = UMLClassBox(self.interface)  # Create an instance of UMLClassBox

        #################################################################
        ### BUTTONS SETUP ###
        # Find and connect buttons to their respective actions for user interaction
        # These buttons control the visibility and appearance of the UML grid and handle adding/removing UML components

        ## DARK/LIGHT MODE BUTTONS ##
        self.toggle_mode_button = self.findChild(QtWidgets.QAction, "toggle_mode")  # Toggle light/dark mode
        # Connect grid/view actions to their respective methods
        self.toggle_mode_button.triggered.connect(self.toggle_mode_method)

        ## UML DIAGRAM BUTTONS ##
        # Actions for adding, deleting, and renaming UML classes
        self.add_class_action = self.findChild(QtWidgets.QAction, "add_class")         # Add class
        self.delete_class_action = self.findChild(QtWidgets.QAction, "delete_class")   # Delete class
        self.rename_class_action = self.findChild(QtWidgets.QAction, "rename_class")   # Rename class

        # Connect UML class actions to their respective methods
        self.add_class_action.triggered.connect(self.add_class_gui)
        self.delete_class_action.triggered.connect(self.delete_class_gui)
        self.rename_class_action.triggered.connect(self.rename_class_gui)

        #################################################################
        # Actions for managing fields (add, delete, rename)
        self.add_field_action = self.findChild(QtWidgets.QAction, "add_field")         # Add field
        self.delete_field_action = self.findChild(QtWidgets.QAction, "delete_field")   # Delete field
        self.rename_field_action = self.findChild(QtWidgets.QAction, "rename_field")   # Rename field

        # Connect UML field actions to their respective methods
        self.add_field_action.triggered.connect(self.add_field_gui)
        self.delete_field_action.triggered.connect(self.delete_field_gui)
        self.rename_field_action.triggered.connect(self.rename_field_gui)

        #################################################################
        # Actions for managing methods (add, delete, rename)
        self.add_method_action = self.findChild(QtWidgets.QAction, "add_method")       # Add method
        self.delete_method_action = self.findChild(QtWidgets.QAction, "delete_method") # Delete method
        self.rename_method_action = self.findChild(QtWidgets.QAction, "rename_method") # Rename method

        # Connect UML method actions to their respective methods
        self.add_method_action.triggered.connect(self.add_method_gui)
        self.delete_method_action.triggered.connect(self.delete_method_gui)
        self.rename_method_action.triggered.connect(self.rename_method_gui)

        #################################################################
        # Actions for managing parameters (add, delete, rename, replace)
        self.add_param_action = self.findChild(QtWidgets.QAction, "add_param")         # Add parameter
        self.delete_param_action = self.findChild(QtWidgets.QAction, "delete_param")   # Delete parameter
        self.rename_param_action = self.findChild(QtWidgets.QAction, "rename_param")   # Rename parameter
        self.replace_param_action = self.findChild(QtWidgets.QAction, "replace_param") # Replace parameter

        # Connect UML parameter actions to their respective methods
        self.add_param_action.triggered.connect(self.add_param_gui)
        self.delete_param_action.triggered.connect(self.delete_param_gui)
        self.rename_param_action.triggered.connect(self.rename_param_gui)
        self.replace_param_action.triggered.connect(self.replace_param_gui)
        
        #################################################################
        # Actions for managing relationships (add, delete, change type)
        self.add_rel_action = self.findChild(QtWidgets.QAction, "add_rel")             # Add relationship
        self.delete_rel_action = self.findChild(QtWidgets.QAction, "delete_rel")       # Delete relationship
        self.change_rel_type_action = self.findChild(QtWidgets.QAction, "change_type") # Change relationship type
        
        # Connect UML relationship actions to their respective methods
        self.add_rel_action.triggered.connect(self.add_rel_gui)
        self.delete_rel_action.triggered.connect(self.delete_rel_gui)
        self.change_rel_type_action.triggered.connect(self.change_rel_type)
         
        #################################################################
        # File management actions (open folder, save, save as)
        self.open_folder_action = self.findChild(QtWidgets.QAction, "Open")            # Open folder
        self.save_as_action = self.findChild(QtWidgets.QAction, "SaveAs")              # Save as new file
        self.save_action = self.findChild(QtWidgets.QAction, "Save")                   # Save current file

        # Connect file management actions to their respective methods
        self.open_folder_action.triggered.connect(self.open_folder_gui)
        self.save_as_action.triggered.connect(self.save_as_gui)
        self.save_action.triggered.connect(self.save_gui)

        #################################################################
        # Action for creating a new file (resetting the current session)
        self.new_file_action = self.findChild(QtWidgets.QAction, "New")
        self.new_file_action.triggered.connect(self.new_file_gui)
        
        #################################################################
        # Help action to display instructions
        self.help_action = self.findChild(QtWidgets.QAction, "Help")
        self.help_action.triggered.connect(self.show_instructions)
        
        #################################################################
        # Undo and Redo actions
        self.undo_action = self.findChild(QtWidgets.QAction, "Undo")
        self.redo_action = self.findChild(QtWidgets.QAction, "Redo")
        
        # Connect Undo and Redo actions to their respective methods
        self.undo_action.triggered.connect(self.undo_gui)
        self.redo_action.triggered.connect(self.redo_gui)

    #################################################################
    ### EVENT FUNCTIONS ###
    # These functions manage events triggered by the user, such as adding/deleting UML components,
    # toggling grid settings, and saving files.

    ## UML BOX EVENTS ##
    def add_class_gui(self):
        """
        Add a new UML class box to the grid scene.
        """
        self.grid_view.add_class()

    def delete_class_gui(self):
        """
        Delete the selected UML class or arrow from the diagram.
        """
        self.grid_view.delete_class()

    def rename_class_gui(self):
        """
        Rename the selected UML class in the grid scene.
        """
        self.grid_view.rename_class()

    #################################################################
    ## FIELD EVENTS ##
    def add_field_gui(self):
        """
        Add a new field to the selected UML class.
        """
        self.grid_view.add_field()

    def delete_field_gui(self):
        """
        Delete a field from the selected UML class.
        """
        self.grid_view.delete_field()

    def rename_field_gui(self):
        """
        Rename a field in the selected UML class.
        """
        self.grid_view.rename_field()

    #################################################################
    ## METHOD EVENTS ##
    def add_method_gui(self):
        """
        Add a new method to the selected UML class.
        """
        self.grid_view.add_method()

    def delete_method_gui(self):
        """
        Delete a method from the selected UML class.
        """
        self.grid_view.delete_method()

    def rename_method_gui(self):
        """
        Rename a method in the selected UML class.
        """
        self.grid_view.rename_method()

    #################################################################
    ## PARAMETER EVENTS ##
    def add_param_gui(self):
        """
        Add a new parameter to a method in the selected UML class.
        """
        self.grid_view.add_param()

    def delete_param_gui(self):
        """
        Delete a parameter from a method in the selected UML class.
        """
        self.grid_view.delete_param()

    def rename_param_gui(self):
        """
        Rename a parameter in a method of the selected UML class.
        """
        self.grid_view.rename_param()

    def replace_param_gui(self):
        """
        Replace the parameter list of a method with a new list.
        """
        self.grid_view.replace_param()
    
    #################################################################
    ## RELATIONSHIP EVENTS ##
    def add_rel_gui(self):
        """
        Add a relationship from the source class to the destination class with a specified type.
        """
        self.grid_view.add_relationship()
        
    def delete_rel_gui(self):
        """
        Delete a relationship from the source class to the destination class.
        """
        self.grid_view.delete_relationship()
        
    def change_rel_type(self):
        """
        Change the type of an existing relationship.
        """
        self.grid_view.change_relationship_type()
        
    #################################################################
    ## FILE MANAGEMENT ##
    def open_folder_gui(self):
        """
        Open a folder to load UML files.
        """
        self.grid_view.open_folder_gui()

    def save_as_gui(self):
        """
        Save the UML diagram as a new file.
        """
        self.grid_view.save_as_gui()

    def save_gui(self):
        """
        Save the UML diagram to the current file.
        """
        self.grid_view.save_gui()
        
    def undo_gui(self):
        """
        Undo the last action performed.
        """
        self.grid_view.undo()
    
    def redo_gui(self):
        """
        Redo the last undone action.
        """
        self.grid_view.redo()

    def new_file_gui(self):
        """
        End the current session and reset to the default state.
        """
        self.grid_view.new_file()

    #################################################################
    ## DARK/LIGHT MODE EVENTS ##
    def toggle_mode_method(self):
        """
        Toggle between light and dark modes in the application.
        """
        self.grid_view.toggle_mode()

    #################################################################
    ## WINDOW EVENTS ##
    def closeEvent(self, event):
        """
        Handle the close event when the user attempts to close the window.

        Parameters:
            event (QCloseEvent): The event that occurs when closing the window.
        """
        reply = QtWidgets.QMessageBox.question(
            self,
            "Exit",
            "Any unsaved work will be deleted! Are you sure you want to quit?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Save
        )

        # If the user chooses 'Yes', the program will exit
        if reply == QtWidgets.QMessageBox.Yes:
            print("Program is exiting...")
            self.interface.exit()  # Call interface exit logic
            event.accept()  # Accept the close event to exit the application
        elif reply == QtWidgets.QMessageBox.Save:
            self.grid_view.save_gui()
            event.ignore()  # Ignore the close event to allow saving
        else:
            event.ignore()  # Ignore the close event to keep the application running
            
    def show_instructions(self):
        """
        Display a pop-up window with instructions on how to use the application.
        """
        instruction_text = """
        Instructions:
        1. Use the left mouse button to select and drag class boxes.
        2. Right-click to open the context menu with additional options.
        3. Use the toolbar for more actions like save, load, and edit.
        4. Press Ctrl+S to quickly save your progress.
        """
        
        # Create the pop-up window
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Instructions")
        msg_box.setText(instruction_text)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        
        # Show the pop-up window
        msg_box.exec_()
