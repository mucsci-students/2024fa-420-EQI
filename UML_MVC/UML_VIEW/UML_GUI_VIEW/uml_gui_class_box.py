from PyQt5 import QtWidgets, QtGui
from typing import Dict, List

###################################################################################################

from UML_ENUM_CLASS.uml_enum import BoxDefaultStat as Default
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_editable_text_item import UMLEditableTextItem as Text

###################################################################################################

class UMLClassBox(QtWidgets.QGraphicsRectItem):
    """
    UMLClassBox represents a UML class box in a UML diagram.

    This class extends QGraphicsRectItem to create a visual representation of a UML class, including:
    - Class name
    - Fields
    - Methods
    - Parameters

    The UMLClassBox is resizable and movable within the diagram scene.
    It handles the rendering and alignment of text items for class name, fields, and methods.
    It also provides connection points for relationships (arrows) to other UMLClassBoxes.
    """
    def __init__(self, interface, class_name="ClassName", x=None, y=None, parent=None):
        """
        Initialize the UMLClassBox with default settings.

        Parameters:
            interface: The interface object for communication with other UML components.
            class_name (str): The initial name of the class. Defaults to "ClassName".
            x (float): The initial x-coordinate position of the class box. Defaults to None.
            y (float): The initial y-coordinate position of the class box. Defaults to None.
            parent: The parent QGraphicsItem. Defaults to None.
        """
        #################################################################
        # Calling constructor from parent class
        super().__init__(parent)

        # Interface to communicate with other UML components
        self.interface = interface

        #################################################################
        ### INITIALIZING FIELD, METHOD, PARAMETER, HANDLE, AND CONNECTION POINT LISTS ###
        # Initialize dictionaries and lists for fields, methods, parameters, and relationships
        self.field_list: Dict = {}            # Stores field text items with their keys
        self.field_key_list: List = []        # Keeps track of field keys (tuples of type and name)
        
        self.method_list: List = []           # List of methods, each method is a dictionary containing method_key, method_text, and parameters
        
        # Parameter tracking (currently unused)
        self.param_num = 0
        
        self.handles_list: List = []          # List for resize handles (not used since resizing is commented out)
        self.connection_points_list: Dict = {}  # Dictionary of connection points for relationships
        self.arrow_line_list: List = []       # List of arrow lines (relationships)
        
        # Store the position of the box
        self.box_position = {
            "x": x, 
            "y": y
        } 

        #################################################################
        ### UML CLASS BOX DEFAULT SETUP ###
        
        # Default position, dimensions, margin, and sizes for handles and connection points
        self.default_box_x = Default.BOX_DEFAULT_X.value
        self.default_box_y = Default.BOX_DEFAULT_Y.value
        self.default_box_width = Default.BOX_DEFAULT_WIDTH.value
        self.default_box_height = Default.BOX_DEFAULT_HEIGHT.value
        self.default_margin = Default.BOX_DEFAULT_MARGIN.value
        
        # Handle points and connection points size
        self.handle_size = 10
        self.connection_point_size = 6
        
        # Initialize dragging and connection properties
        self.is_box_dragged = False
        # self.is_resizing = False  # Resizing functionality is commented out
        self.is_source_class = False          # Indicates if this class is a source in a relationship
        self.current_handle = None            # Currently active resize handle (unused)

        #################################
        
        # Define bounding rectangle of the class box
        self.setRect(self.default_box_x, self.default_box_y, 
                     self.default_box_width + self.default_margin, 
                     self.default_box_height)
        
        # Set visual appearance of the class box
        self.setPen(QtGui.QPen(QtGui.QColor(30, 144, 255)))       # Border color (Dodger Blue)
        self.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 255)))    # Background color (Cyan)
        
        # Set class box selectable and movable
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        
        # Enable the box to send geometry change events.
        # This allows the box to notify when it moves or is resized.
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
        
        # Enable hover events
        self.setAcceptHoverEvents(True)
        
        # Create the class name text item and position it
        self.class_name_text = self.create_text_item(class_name, selectable=False)
        
        # Connect the text change callback to ensure it re-centers when the text changes.
        self.class_name_text.document().contentsChanged.connect(self.centering_class_name)
        
        # Store default text color and font
        self.text_color = self.class_name_text.defaultTextColor()
        self.text_font = self.class_name_text.font()
        self.font_size = self.text_font.pointSize()
        
        # Create separator below class name
        self.create_separator()
        
        # Center the class name initially
        self.centering_class_name()
        
        # # Create handles for resizing the class box (currently commented out)
        # self.create_resize_handles()
        
        # Create connection points for relationships (arrows)
        self.create_connection_points()

    #################################################################
    ### MEMBER FUNCTIONS ###
    
    #################################
    ## UPDATE BOX AND ITS COMPONENTS ##
    
    def update_box(self):
        """
        Update the dimensions and layout of the UML box based on the contents.

        This method recalculates and updates all aspects of the UML box to fit the content, including:
        - Aligning methods and parameters.
        - Adjusting the box height and width.
        - Repositioning the class name.
        - Aligning fields.
        - Updating connection points and separators.
        - Updating arrow lines and box position.
        """
        # Align methods and their parameters within the UML box
        self.update_method_and_param_alignment()
        
        # Adjust the box's height and width based on its contents
        self.update_box_dimension()

        # Reposition the class name in the center of the UML box
        self.centering_class_name()

        # Align the fields within the UML box
        self.update_field_alignment()

        # # Update the position of the resize handles at the corners of the UML box (if resizing is enabled)
        # self.update_handle_positions()

        # Update the connection points for relationships
        self.update_connection_point_positions()

        # Update the separators between the class name, fields, and methods
        self.update_separators()
        
        # Update the positions of any arrow lines connected to this box
        self.update_arrow_lines()
        
        # Update the stored position of the box
        self.update_box_position()
        
    def update_box_position(self):
        """
        Update the stored position of the box based on its current position.

        This method retrieves the current position of the box and updates the `box_position` dictionary.
        """
        self.box_position["x"] = self.pos().x()
        self.box_position["y"] = self.pos().y()
        print(f"Current location: ({self.box_position['x']} , {self.box_position['y']})")
        
    def set_box_position(self):
        """
        Set the position of the box to the stored position.

        This method moves the box to the x and y coordinates stored in `box_position`.
        If the coordinates are not set, it defaults to (0, 0).
        """
        # Retrieve the desired x and y positions from the box_position dictionary
        new_x = self.box_position.get("x", 0)  # Default to 0 if 'x' not found
        new_y = self.box_position.get("y", 0)  # Default to 0 if 'y' not found
        
        # Set the new position using setPos()
        self.setPos(new_x, new_y)

    def itemChange(self, change, value):
        """
        Overridden method to handle item changes, such as position changes.

        Parameters:
            change (GraphicsItemChange): The type of change.
            value: The new value.

        Returns:
            The result of the superclass's itemChange method.
        """
        if change == QtWidgets.QGraphicsItem.ItemPositionChange:
            # Update arrow positions when the position of the box changes
            self.update_arrow_lines()
            self.update_box_position()
        return super().itemChange(change, value)
    
    def update_arrow_lines(self):
        """
        Update the positions of all arrow lines connected to this box.

        This method iterates through the list of arrow lines and calls their `update_position` method.
        """
        for arrow_line in self.arrow_line_list:
            arrow_line.update_position()

    def update_box_dimension(self):
        """
        Recalculate and update the dimensions of the UML box based on its contents.

        The box will be resized to fit the class name, fields, methods, and parameters,
        shrinking or growing as necessary.
        """
        # Get total height and maximum width based on the current content
        total_height = self.get_total_height() + 3  # Add extra margin
        max_width = self.get_maximum_width()

        # Ensure the box shrinks as well as expands
        # Check if the box's current size is larger than needed and adjust accordingly
        default_width = self.default_box_width + self.default_margin
        
        # Allow the box to shrink when content decreases
        if max_width < default_width:
            # Shrink the box dimensions
            self.setRect(self.rect().x(), self.rect().y(), default_width, total_height)
        else:
            # Expand the box dimensions to fit the content
            self.setRect(self.rect().x(), self.rect().y(), max_width, total_height)
            
    def centering_class_name(self):
        """
        Center the class name text inside the UML class box horizontally.

        This method calculates the position of the class name text based on the width of the UML class box 
        and the width of the text. It adjusts the position of the text so that it is horizontally centered 
        within the class box. The vertical position is fixed using a default margin.
        """
        # Get the current width of the UML class box
        box_width = self.rect().width()

        # Get the width of the class name text using its bounding rectangle
        class_name_width = self.class_name_text.boundingRect().width()

        # If the class name is longer than the box, resize the box to fit the name
        if class_name_width > box_width:
            # Adjust the width of the UML class box to fit the class name
            new_box_width = class_name_width + self.default_margin  # Add some margin to the width
            self.setRect(self.rect().x(), self.rect().y(), new_box_width, self.rect().height())

        # Recalculate the box width after potential resizing
        box_width = self.rect().width()

        # Calculate the x-position to center the class name horizontally
        class_name_x_pos = self.rect().topLeft().x() + (box_width - class_name_width) / 2
        
        # Calculate y-position for the class name (fixed at top with margin)
        class_name_y_pos = self.rect().topLeft().y() + self.default_margin / 2

        # Set the class name's position, ensuring it stays horizontally centered
        self.class_name_text.setPos(class_name_x_pos, class_name_y_pos)
        
        # Update the positions of the separators
        self.update_separators()
        
    def update_separators(self):
        """
        Update positions of the separator lines based on current box size.

        This function keeps the separator anchored at a fixed y-position relative to the class name.
        """
        if hasattr(self, 'separator_line1'):
            # Update the separator line based on the current size of the UML box
            class_name_height = self.class_name_text.boundingRect().height()
            y_pos = self.rect().topLeft().y() + class_name_height + self.default_margin
            # Set the new position of the separator line
            self.separator_line1.setLine(
                self.rect().topLeft().x(), y_pos, 
                self.rect().topRight().x(), y_pos
            )
            self.separator_line1.setPen(QtGui.QPen(QtGui.QColor(30, 144, 255)))  # Set line color (Dodger Blue)
             
        if hasattr(self, 'separator_line2') and self.separator_line2.scene() == self.scene():
            if len(self.method_list) > 0:
                # Update the second separator line if there are methods
                class_name_height = self.class_name_text.boundingRect().height()
                field_section_height = self.get_field_text_height()
                y_pos = self.rect().topLeft().y() + class_name_height + field_section_height + self.default_margin
                self.separator_line2.setLine(
                    self.rect().topLeft().x(), y_pos, 
                    self.rect().topRight().x(), y_pos
                )
                self.separator_line2.setPen(QtGui.QPen(QtGui.QColor(30, 144, 255)))  # Set line color (Dodger Blue)
            else:
                # Remove the second separator if there are no methods
                self.scene().removeItem(self.separator_line2)
                
    # The method update_handle_positions is commented out and ignored as per your request

    def update_connection_point_positions(self):
        """
        Update the positions of the connection points based on the size of the UML box.

        Connection points are positioned at the center of the edges (top, bottom, left, right).
        """
        rect = self.rect()
        # Set positions of connection points relative to the box
        self.connection_points_list['top'].setPos(rect.center().x(), rect.top() - 1)
        self.connection_points_list['bottom'].setPos(rect.center().x(), rect.bottom() + 5)
        self.connection_points_list['left'].setPos(rect.left() - 1, rect.center().y())
        self.connection_points_list['right'].setPos(rect.right() + 5, rect.center().y() + 2)
        
    def update_field_alignment(self):
        """
        Align field text items in the UML class box row by row.

        Each field will be displayed on a new line, aligned to the left of the box.
        """
        # Starting y-position for the first field (below the class name)
        y_offset = self.class_name_text.boundingRect().height() + self.default_margin

        for field_name in self.field_key_list:
            # Get the text item for the field
            field_text = self.field_list[field_name]
        
            # Calculate the x-position to align the field text to the left
            field_x_pos = self.rect().topLeft().x() + self.default_margin
        
            # Set the position of the field text, each field below the previous one
            field_text.setPos(field_x_pos, self.rect().topLeft().y() + y_offset)
        
            # Increment y_offset for the next field (adding field height)
            y_offset += field_text.boundingRect().height()
            
    def update_method_and_param_alignment(self):
        """
        Align methods and parameters in the UML class box row by row.

        Each method will be displayed on a new line, with its parameters included in the method signature.
        """
        # Starting y-position for the first method (below the class name and fields)
        y_offset = self.class_name_text.boundingRect().height() + self.get_field_text_height() + self.default_margin

        # Iterate through each method and align them, along with their parameters
        for method_entry in self.method_list:
            method_key = method_entry["method_key"]     # Tuple (return_type, method_name)
            method_text = method_entry["method_text"]   # Text item for the method
            param_list = method_entry["parameters"]     # List of parameters (type, name)
            
            # Calculate the x-position for the method text (aligned to the left)
            method_x_pos = self.rect().topLeft().x() + self.default_margin
            # Set the position of the method text item
            method_text.setPos(method_x_pos, self.rect().topLeft().y() + y_offset)
            
            # Build the method signature with parameters
            if len(param_list) == 0:
                # No parameters, just method name with empty parentheses
                method_text.setPlainText(f"{method_key[0]} {method_key[1]}()")
            else:
                # Parameters exist, include them in the signature
                param_text_str = ", ".join(f"{ptype} {pname}" for ptype, pname in param_list)
                method_with_params = f"{method_key[0]} {method_key[1]}({param_text_str})"
                method_text.setPlainText(method_with_params)

            # Update y_offset for the next method (incremented by the height of this method)
            y_offset += method_text.boundingRect().height()
                
    #################################
    ### CREATION METHODS ###
    
    def create_separator(self, is_first=True, is_second=True):
        """
        Create separator lines between different sections of the UML class box.

        This method is used to visually separate the class name, fields, and methods in the UML class box.
        It creates horizontal lines that span the width of the UML box and adjusts their positions based on 
        the content (class name and fields).

        Parameters:
            is_first (bool): 
                - If True, creates the first separator line below the class name.
            is_second (bool):
                - If True, creates the second separator line below the fields.
        """
        
        # Check if it's the first separator (placed below the class name)
        if is_first:
            # Calculate the height of the class name text item
            class_name_height = self.class_name_text.boundingRect().height()

            # Set the y-position for the separator line just below the class name
            y_pos = self.rect().topLeft().y() + class_name_height + self.default_margin

            # Create the first separator as a horizontal line spanning the box width
            self.separator_line1 = QtWidgets.QGraphicsLineItem(
                self.rect().topLeft().x(),  # Starting x-coordinate (left side of the box)
                y_pos,                      # Y-coordinate (below the class name)
                self.rect().topRight().x(),  # Ending x-coordinate (right side of the box)
                y_pos,                      # Keep the same y-coordinate to make the line horizontal
                self  # Set the UML class box as the parent
            )

        # If it's the second separator, create it (placed below the fields section)
        elif is_second:
            # Calculate the height of the class name and fields
            class_name_height = self.class_name_text.boundingRect().height()
            field_section_height = self.get_field_text_height()

            # Set the y-position for the second separator line just below the fields
            y_pos = self.rect().topLeft().y() + class_name_height + field_section_height + self.default_margin

            # Create the second separator as a horizontal line spanning the box width
            self.separator_line2 = QtWidgets.QGraphicsLineItem(
                self.rect().topLeft().x(),  # Starting x-coordinate (left side of the box)
                y_pos,                      # Y-coordinate (below the fields)
                self.rect().topRight().x(),  # Ending x-coordinate (right side of the box)
                y_pos,                      # Keep the same y-coordinate
                self  # Set the UML class box as the parent
            )
            
    # The method create_resize_handles is commented out and ignored as per your request

    def create_connection_points(self):
        """
        Create four connection points (top, bottom, left, right) for linking arrows between UML boxes.

        Each connection point is represented by a small ellipse at the edge of the UML box.
        """
        self.connection_points_list = {
            'top': QtWidgets.QGraphicsEllipseItem(self),
            'bottom': QtWidgets.QGraphicsEllipseItem(self),
            'left': QtWidgets.QGraphicsEllipseItem(self),
            'right': QtWidgets.QGraphicsEllipseItem(self),
        }

        for point_name, cp_item in self.connection_points_list.items():
            # Set the size of the connection point
            cp_item.setRect(-5, -5, self.connection_point_size, self.connection_point_size)

            # Set the appearance of the connection point
            cp_item.setPen(QtGui.QPen(QtGui.QColor(30, 144, 255)))  # Border color (Dodger Blue)
            cp_item.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))  # Fill color (White)

            # Disable movement and selection of connection points
            cp_item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
            cp_item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)

        # Update the positions of the connection points based on the size of the box
        self.update_connection_point_positions()

    #################################
    ## CLASS NAME TEXT RELATED ##
    
    def create_text_item(self, text: str, selectable=False, is_field=None, is_method=None, is_parameter=None, color=None, font=None):
        """
        Create and return a UMLEditableTextItem with specified properties.

        Parameters:
            text (str): The initial text of the item.
            selectable (bool): Whether the text item is selectable and focusable.
            is_field (bool): Indicates if the text item is a field (unused here).
            is_method (bool): Indicates if the text item is a method (unused here).
            is_parameter (bool): Indicates if the text item is a parameter (unused here).
            color (QColor): The color of the text.
            font (QFont): The font of the text.

        Returns:
            UMLEditableTextItem: The created text item.
        """
        # Create the text item with specified color and font
        if color is not None and font is not None:
            text_item = Text(text=text, parent=self, color=color, font=font)  
            self.text_color = color
            self.text_font = font
        elif color is not None:
            text_item = Text(text=text, parent=self, color=color) 
            self.text_color = color 
        elif font is not None:
            text_item = Text(text=text, parent=self, font=font)  
            self.text_font = font
        else:
            text_item = Text(text=text, parent=self)  
        
        # Set the text item selectable and focusable if specified
        if selectable:
            text_item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
            text_item.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)
        return text_item
                  
    #################################
    ## MOUSE EVENT RELATED ##

    # The mouse event methods are commented out and ignored as per your request

    def mouseReleaseEvent(self, event):
        """
        Handle mouse release events to stop dragging the UML box.
        
        This method stops the dragging action once the mouse is released.

        Parameters:
            event (QGraphicsSceneMouseEvent): The mouse event.
        """
        if self.is_box_dragged:
            self.is_box_dragged = False  # Reset dragging flag
            event.accept()
        super().mouseReleaseEvent(event)  # Call the parent method

    #################################################################
    ### UTILITY FUNCTIONS ###

    def get_field_text_height(self):
        """
        Calculate the total height of all field text items in the box.
        
        Returns:
            float: The total height of all field text items.
        """
        field_text_height = 0
        # Sum the heights of all field text items
        for field_text in self.field_list.values():
            field_text_height += field_text.boundingRect().height()
        return field_text_height

    def get_method_text_height(self):
        """
        Calculate the total height of all method text items in the box.
        
        Returns:
            float: The total height of all method text items.
        """
        method_text_height = 0
        # Sum the heights of all method text items
        for method_entry in self.method_list:
            # Get the method text item
            method_text = method_entry["method_text"]
            method_text_height += method_text.boundingRect().height()
        return method_text_height

    def get_maximum_width(self):
        """
        Calculate the maximum width of the UML box based on the widths of its contents.

        This function ensures that the box has enough width to display all content without truncation.

        Returns:
            float: The maximum width required for the box based on its contents.
        """
        # Get the width of the class name text item
        max_class_name_width = self.class_name_text.boundingRect().width()
        
        # Get the maximum width of all field text items
        max_field_width = max(
            [self.field_list[field_key].boundingRect().width() for field_key in self.field_key_list],
            default=0
        )
        
        # Get the maximum width of all method text items
        max_method_width = max(
            [
                method_entry["method_text"].boundingRect().width() 
                for method_entry in self.method_list
            ],
            default=0
        )
        
        # Determine the largest width among all components
        content_max_width = max(
            max_class_name_width,
            max_field_width,
            max_method_width
        )
        
        # Return the largest width plus margins
        return content_max_width + self.default_margin * 2
    
    def get_total_height(self):
        """
        Calculate the total height of the UML box based on its contents.

        Returns:
            float: The total height required for the box, including margins.
        """
        # Default height for margins
        default_height = self.default_margin * 2
        
        # Get the height of the class name text
        class_name_height = self.class_name_text.boundingRect().height()

        # Get the total height of the fields section
        fields_text_height = self.get_field_text_height()

        # Get the total height of the methods section
        method_text_height = self.get_method_text_height()

        # Calculate the total height required for the box, including margins
        total_height = (class_name_height 
                        + fields_text_height 
                        + method_text_height 
                        + default_height)
        
        return total_height

###################################################################################################
