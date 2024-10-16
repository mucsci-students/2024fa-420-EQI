###################################################################################################
# Import necessary modules from PyQt5 and custom UML classes
###################################################################################################

from PyQt5 import uic
from PyQt5 import QtWidgets
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_grid import GridGraphicsView
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_class_box import UMLClassBox
from UML_MVC.uml_observer import UMLObserver as Observer

###################################################################################################

class MainWindow(QtWidgets.QMainWindow, Observer):
    """
    Main application window that loads the UI and sets up interactions.
    Inherits from QMainWindow for managing the graphical interface and from Observer to receive updates
    from the core UML system.
    """

    def __init__(self, interface):
        """
        Initializes a new MainWindow instance, loading the GUI and setting up the interface.

        Parameters:
        - interface: The interface to communicate with UMLCoreManager (business logic layer).
        """
        super().__init__()
        self.interface = interface  # Interface to communicate with UMLCoreManager

        # Load the UI file to set up the layout and widgets of the main window
        uic.loadUi('prototype_gui.ui', self)

        # Create a grid view where UML class boxes and relationships will be displayed, and set it as the central widget
        self.grid_view = GridGraphicsView(self.interface)
        self.setCentralWidget(self.grid_view)
        self.box = UMLClassBox(self.interface)

        #################################################################
        ### BUTTONS SETUP ###
        # Find and connect buttons to their respective actions for user interaction
        # These buttons control the visibility and appearance of the UML grid and handle adding/removing UML components

        ## GRID/VIEW BUTTONS ##
        self.toggle_grid_button = self.findChild(QtWidgets.QAction, "toggle_grid")  # Toggle grid visibility
        self.change_grid_color_button = self.findChild(QtWidgets.QAction, "change_grid_color")  # Change grid color
        self.reset_view_button = self.findChild(QtWidgets.QAction, "reset_view")  # Reset the view
        self.toggle_mode_button = self.findChild(QtWidgets.QAction, "toggle_mode")  # Toggle light/dark mode

        # Connect grid/view actions to their respective methods
        self.toggle_grid_button.triggered.connect(self.toggle_grid_method)
        self.change_grid_color_button.triggered.connect(self.change_gridColor_method)
        self.reset_view_button.triggered.connect(self.reset_view_method)
        self.toggle_mode_button.triggered.connect(self.toggle_mode_method)

        ## UML DIAGRAM BUTTONS ##
        # Actions for adding, deleting, and renaming UML classes, fields, methods, and parameters
        self.add_class_action = self.findChild(QtWidgets.QAction, "add_class")  # Add class
        self.delete_class_action = self.findChild(QtWidgets.QAction, "delete_class")  # Delete class
        self.rename_class_action = self.findChild(QtWidgets.QAction, "rename_class")  # Rename class

        # Connect UML class actions to their respective methods
        self.add_class_action.triggered.connect(self.add_class_gui)
        self.delete_class_action.triggered.connect(self.delete_class_gui)
        self.rename_class_action.triggered.connect(self.rename_class_gui)

        #################################################################
        # Actions for managing fields (add, delete, rename)
        self.add_field_action = self.findChild(QtWidgets.QAction, "add_field")  # Add field
        self.delete_field_action = self.findChild(QtWidgets.QAction, "delete_field")  # Delete field
        self.rename_field_action = self.findChild(QtWidgets.QAction, "rename_field")  # Rename field

        # Connect UML field actions to their respective methods
        self.add_field_action.triggered.connect(self.add_field_gui)
        self.delete_field_action.triggered.connect(self.delete_field_gui)
        self.rename_field_action.triggered.connect(self.rename_field_gui)

        #################################################################
        # Actions for managing methods (add, delete, rename)
        self.add_method_action = self.findChild(QtWidgets.QAction, "add_method")  # Add method
        self.delete_method_action = self.findChild(QtWidgets.QAction, "delete_method")  # Delete method
        self.rename_method_action = self.findChild(QtWidgets.QAction, "rename_method")  # Rename method

        # Connect UML method actions to their respective methods
        self.add_method_action.triggered.connect(self.add_method_gui)
        self.delete_method_action.triggered.connect(self.delete_method_gui)
        self.rename_method_action.triggered.connect(self.rename_method_gui)

        #################################################################
        # Actions for managing parameters (add, delete, rename, replace)
        self.add_param_action = self.findChild(QtWidgets.QAction, "add_param")  # Add parameter
        self.delete_param_action = self.findChild(QtWidgets.QAction, "delete_param")  # Delete parameter
        self.rename_param_action = self.findChild(QtWidgets.QAction, "rename_param")  # Rename parameter
        self.replace_param_action = self.findChild(QtWidgets.QAction, "replace_param")  # Replace parameter

        # Connect UML parameter actions to their respective methods
        self.add_param_action.triggered.connect(self.add_param_gui)
        self.delete_param_action.triggered.connect(self.delete_param_gui)
        self.rename_param_action.triggered.connect(self.rename_param_gui)
        self.replace_param_action.triggered.connect(self.replace_param_gui)
        
        #################################################################
        # Actions for managing relationship (add, delete, replace type)
        self.add_rel_action = self.findChild(QtWidgets.QAction, "add_rel")  # Add relationship
        self.delete_rel_action = self.findChild(QtWidgets.QAction, "delete_rel")  # Delete relationship
        self.change_rel_type_action = self.findChild(QtWidgets.QAction, "change_type")  # Delete relationship
        
        # Connect UML relationship actions to their respective methods
        self.add_rel_action.triggered.connect(self.add_rel_gui)
        self.delete_rel_action.triggered.connect(self.delete_rel_gui)
        self.change_rel_type_action.triggered.connect(self.change_rel_type)
         
        #################################################################
        # File management actions (open folder, save, save as)
        self.open_folder_action = self.findChild(QtWidgets.QAction, "Open")  # Open folder
        self.save_as_action = self.findChild(QtWidgets.QAction, "SaveAs")  # Save as new file
        self.save_action = self.findChild(QtWidgets.QAction, "Save")  # Save current file

        # Connect file management actions to their respective methods
        self.open_folder_action.triggered.connect(self.open_folder_gui)
        self.save_as_action.triggered.connect(self.save_as_gui)
        self.save_action.triggered.connect(self.save_gui)

        #################################################################
        # Action to reset to default state (session end)
        self.default_state_action = self.findChild(QtWidgets.QAction, "default_state")  # End session and reset
        self.default_state_action.triggered.connect(self.end_session_gui)

        #################################################################
        # Actions for exporting diagrams as images (PDF/PNG)
        self.export_pdf_action = self.findChild(QtWidgets.QAction, "export_pdf")  # Export as PDF
        self.export_png_action = self.findChild(QtWidgets.QAction, "export_png")  # Export as PNG

        # Connect export actions to their respective methods
        self.export_pdf_action.triggered.connect(self.export_pdf_gui)
        self.export_png_action.triggered.connect(self.export_png_gui)

    #################################################################
    ### EVENT FUNCTIONS ###
    # These functions manage events triggered by the user, such as adding/deleting UML components, toggling grid settings, and saving files.

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
        Replace an existing parameter in a method with a new one.
        """
        self.grid_view.replace_param()
    
    #################################################################
    ## RELATIONSHIP EVENTS ##
    def add_rel_gui(self):
        """
        Add a relationship from source class to destination class with type.
        """
        self.grid_view.add_relationship()
        
    def delete_rel_gui(self):
        """
        Delete a relationship from source class to destination class.
        """
        self.grid_view.delete_relationship()
        
    def change_rel_type(self):
        """
        Change a relationship type of an existing relationship.
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

    def end_session_gui(self):
        """
        End the current session and reset to the default state.
        """
        self.grid_view.end_session()

    #################################################################
    ## GRID EVENTS ##
    def toggle_grid_method(self, checked):
        """
        Toggle the visibility of the grid in the view.

        Parameters:
        - checked (bool): True if the grid should be visible, False otherwise.
        """
        self.grid_view.set_grid_visible(checked)

    def change_gridColor_method(self):
        """
        Open a color dialog to change the grid color.
        """
        color = QtWidgets.QColorDialog.getColor(
            initial=self.grid_view.grid_color,
            parent=self,
            title="Select Grid Color"
        )
        if color.isValid():
            self.grid_view.set_grid_color(color)

    def reset_view_method(self):
        """
        Reset the grid view to the default state (default zoom, pan, etc.).
        """
        self.grid_view.reset_view()

    def toggle_mode_method(self):
        """
        Toggle between light and dark modes in the application.
        """
        self.grid_view.toggle_mode()

    #################################################################
    ## EXPORT EVENTS ##
    def export_pdf_gui(self):
        """
        Export the UML diagram as a PDF.
        """
        self.grid_view.export_pdf()

    def export_png_gui(self):
        """
        Export the UML diagram as a PNG image.
        """
        self.grid_view.export_png()

    #################################################################
    ## WINDOW EVENTS ##
    def closeEvent(self, event):
        """
        Handle the close event when the user attempts to close the window.

        Parameters:
        - event (QCloseEvent): The event that occurs when closing the window.
        """
        reply = QtWidgets.QMessageBox.question(self, "Exit",
                                               "Are you sure you want to quit?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        # If the user chooses 'Yes', the program will exit
        if reply == QtWidgets.QMessageBox.Yes:
            print("Program is exiting...")
            self.interface.exit()  # Call interface exit logic
            event.accept()  # Accept the close event to exit the application
        else:
            event.ignore()  # Ignore the close event to keep the application running
