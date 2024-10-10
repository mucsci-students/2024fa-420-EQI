###################################################################################################

from PyQt5 import QtWidgets, QtGui, QtCore

###################################################################################################
# Method Class: Represents a UML method with the ability to add/remove parameters.
# Provides UI components such as add/remove parameter buttons and parameter list text field.
###################################################################################################
class Method(QtWidgets.QGraphicsRectItem):
    def __init__(self, name):
        super().__init__()
        
        self.parameter_name = name
        self.parameters = []  # List to hold parameters for the method
        
        # Parameter Text Item - Interactive Text Field for Parameter Names
        self.param_text = QtWidgets.QGraphicsTextItem(self)
        self.param_text.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)  # Allow editing text
        self.param_text.setDefaultTextColor(QtGui.QColor(0, 0, 0))  # Set text color to black
        self.param_text.setPlainText("\n".join(self.parameters))  # Initialize parameter text
        self.param_text.document().contentsChanged.connect(self.update_param_position)

        # Add/Remove Parameter Buttons
        self.add_param_button = self.create_button("+", self.add_parameter)
        self.remove_param_button = self.create_button("-", self.remove_parameter)
        
        # Proxy Widgets for Buttons
        self.add_param_button_proxy = QtWidgets.QGraphicsProxyWidget(self)
        self.add_param_button_proxy.setWidget(self.add_param_button)

        self.remove_param_button_proxy = QtWidgets.QGraphicsProxyWidget(self)
        self.remove_param_button_proxy.setWidget(self.remove_param_button)

    def create_button(self, label, callback):
        """
        Create and style a QPushButton.

        Parameters:
        - label (str): Button label text.
        - callback (function): Function to be connected to the button's clicked signal.

        Returns:
        - QPushButton: Styled button with assigned click callback.
        """
        button = QtWidgets.QPushButton(label)
        button.setStyleSheet(self.param_button_style())
        button.clicked.connect(callback)
        return button

    def add_parameter(self):
        """Add a new parameter to the method."""
        param_name, ok = QtWidgets.QInputDialog.getText(None, "Add Parameter", "Enter parameter name:")
        if ok and param_name:
            self.parameters.append(param_name)
            self.update_param_text()
            self.notify_parent_class_box()

    def remove_parameter(self):
        """Remove an existing parameter from the method."""
        if self.parameters:
            param_name, ok = QtWidgets.QInputDialog.getItem(None, "Remove Parameter", "Select parameter to remove:", self.parameters, 0, False)
            if ok and param_name:
                self.parameters.remove(param_name)
                self.update_param_text()
                self.notify_parent_class_box()
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "No parameters to remove.")

    def update_param_text(self):
        """Update the displayed text for the method based on the current list of parameters."""
        self.param_text.setPlainText("\n".join(self.parameters))  # Update the text for parameters
        self.update_param_position()  # Update position after text change

    def update_param_position(self):
        """Update the position of the parameter text based on the location of the buttons."""
        # Position the parameter text below the "add parameter" button
        button_y = self.add_param_button_proxy.pos().y()
        param_y = button_y + self.add_param_button_proxy.boundingRect().height()
        self.param_text.setPos(self.pos().x() + 40, param_y)
    
    def notify_parent_class_box(self):
        """
        Notify the UMLClassBox parent to update positions, assuming this Method is part of a UMLClassBox.
        """
        if self.scene():
            for item in self.scene().items():
                if isinstance(item, UMLClassBox):
                    item.update_positions()
                    return

    def param_button_style(self):
        """
        Return button style for uniformity.
        
        Returns:
        - str: Button stylesheet.
        """
        return """
        QPushButton {
            background-color: #55ffff;
            color: black;
            border-radius: 1px;
            padding: 1px;
            border: 1px solid #000000;
            min-width: 7px;
            min-height: 7px;
            font-size: 7px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        """

###################################################################################################
# UMLClassBox Class: Represents a UML class box with editable sections for class name, fields, and methods.
# Inherits from QGraphicsRectItem to allow graphical representation in a QGraphicsScene.
###################################################################################################
class UMLClassBox(QtWidgets.QGraphicsRectItem):
    def __init__(self, interface, class_name="ClassName", field=None, methods=None, parent=None):
        super().__init__(parent)
        
        # Interface to communicate with UMLCoreManager
        self.interface = interface  
        
        # Default properties for attributes (fields) and methods if not provided
        self.field = field if field is not None else []
        self.methods = methods if methods is not None else []

        # Initialize UML Class Box properties
        self.default_width = 150
        self.default_margin = 10
        self.max_width = self.default_width
        self.min_height = 0

        # Define bounding rectangle of the class box
        self.setRect(0, 0, self.default_width, 250)
        self.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))  # Set black border
        self.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 255)))  # Set cyan background

        # Create editable text items for class name, fields, and methods
        self.class_name_text = self.create_text_item(class_name, self.update_positions)
        self.fields_label = self.create_text_item("Fields")
        self.field_text = self.create_text_item("\n".join(self.field), self.update_positions, True)
        self.methods_label = self.create_text_item("Methods")
        self.methods_text = self.create_text_item(self.format_methods(), self.update_positions, True)

        # Initialize resizing and connection properties
        self.is_box_dragged = False
        self.is_resizing = False
        self.current_handle = None
        self.handle_size = 12
        self.is_typing = False
        self.create_resize_handles()
        self.arrows = []  # List to keep track of connected arrows
        self.create_connection_points()

        # Create add/remove buttons for fields and methods
        self.add_field_button = self.create_button("+", self.add_field)
        self.remove_field_button = self.create_button("-", self.remove_field)
        self.add_method_button = self.create_button("+", self.add_method)
        self.remove_method_button = self.create_button("-", self.remove_method)

        # Add button proxies to the scene and position them
        self.add_field_button_proxy = self.add_button_proxy(self.add_field_button, self.default_margin + 34, self.default_margin + 30)
        self.remove_field_button_proxy = self.add_button_proxy(self.remove_field_button, self.default_margin + 49, self.default_margin + 30)
        self.add_method_button_proxy = self.add_button_proxy(self.add_method_button, self.default_margin + 48, self.default_margin + 105)
        self.remove_method_button_proxy = self.add_button_proxy(self.remove_method_button, self.default_margin + 63, self.default_margin + 105)

        # Update initial positions of all elements based on the current box size
        self.update_positions()

    def create_text_item(self, text, change_callback=None, editable=False):
        """
        Create and return a QGraphicsTextItem.

        Parameters:
        - text (str): The initial text of the item.
        - change_callback (function): Optional function to call when text content changes.
        - editable (bool): Whether the text item is editable.

        Returns:
        - QGraphicsTextItem: The created text item.
        """
        text_item = QtWidgets.QGraphicsTextItem(self)
        text_item.setDefaultTextColor(QtGui.QColor(0, 0, 0))  # Set text color to black
        text_item.setPlainText(text)  # Set initial text
        if editable:
            text_item.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)  # Allow text editing
        if change_callback:
            text_item.document().contentsChanged.connect(change_callback)
        return text_item

    def create_button(self, label, callback):
        """
        Create a QPushButton with a given label and callback function.

        Parameters:
        - label (str): Text to display on the button.
        - callback (function): The function to connect to the button's click signal.

        Returns:
        - QPushButton: The created button.
        """
        button = QtWidgets.QPushButton(label)
        button.setStyleSheet(self.button_style())
        button.clicked.connect(callback)
        return button

    def add_button_proxy(self, button, x, y):
        """
        Add a QPushButton to the scene via a QGraphicsProxyWidget and set its position.

        Parameters:
        - button (QPushButton): The button to add.
        - x (float): X coordinate for the button.
        - y (float): Y coordinate for the button.

        Returns:
        - QGraphicsProxyWidget: The proxy widget containing the button.
        """
        proxy = QtWidgets.QGraphicsProxyWidget(self)
        proxy.setWidget(button)
        proxy.setPos(x, y)
        return proxy

    def add_field(self):
        """Add a new field to the UML class."""
        field_name, ok = QtWidgets.QInputDialog.getText(None, "Add Field", "Enter field name:")
        if ok and field_name:
            self.field.append(field_name)  # Append the new field name
            self.update_field_text()  # Update the graphical representation of fields

    def remove_field(self):
        """Remove an existing field from the UML class."""
        if self.field:
            field_name, ok = QtWidgets.QInputDialog.getItem(None, "Remove Field", "Select field to remove:", self.field, 0, False)
            if ok and field_name:
                self.field.remove(field_name)
                self.update_field_text()  # Update the graphical representation of fields
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "No fields to remove.")

    def add_method(self):
        """Add a new method to the UML class."""
        method_name, ok = QtWidgets.QInputDialog.getText(None, "Add Method", "Enter method name:")
        if ok and method_name:
            new_method = Method(method_name + "()")  # Create a Method instance
            self.methods.append(new_method)
            self.add_method_buttons_to_scene(new_method)
            self.scene().addItem(new_method)  # Add method to the scene
            self.update_method_text()

    def add_method_buttons_to_scene(self, method: Method):
        """Add the parameter buttons from the Method object to the UMLClassBox scene."""
        self.scene().addItem(method.add_param_button_proxy)
        self.scene().addItem(method.remove_param_button_proxy)

    def update_field_text(self):
        """Update the displayed text for the fields based on the current list of fields."""
        self.field_text.setPlainText("\n".join(self.field))
        self.update_positions()

    def update_method_text(self):
        """Update the displayed text for the methods based on the current list of methods."""
        self.methods_text.setPlainText(self.format_methods())
        self.update_positions()

    def format_methods(self):
        """
        Format the methods for display with parameters.

        Returns:
        - str: Formatted methods as a string.
        """
        method_lines = []
        for method_obj in self.methods:
            method_lines.append(method_obj.parameter_name)
            for each_param in method_obj.parameters:
                method_lines.append(f"    {each_param}")  # Indent parameters
        return "\n".join(method_lines)  # Return formatted methods as a string

    def button_style(self):
        """
        Return button style for uniformity.
        
        Returns:
        - str: Button stylesheet.
        """
        return """
        QPushButton {
            background-color: #55ffff;
            color: black;
            border-radius: 1px;
            padding: 1px;
            border: 1px solid #000000;
            min-width: 8px;
            min-height: 8px;
            font-size: 10px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        """

    def method_y_position(self, index):
        """Calculate the Y position for the method based on its index."""
        return (index * 13) + self.default_margin + 125

    def remove_method(self):
        if len(self.methods) > 0:
            # Extract method names from the methods list
            method_name_list = [method.parameter_name for method in self.methods if method]
            method_name, ok = QtWidgets.QInputDialog.getItem(None, "Remove Field", "Select field to remove:", method_name_list, 0, False)
            if ok and method_name:
                # Remove the method name directly
                for each_method in self.methods:
                    if each_method.parameter_name == method_name:
                        # Remove the button proxies from the scene
                        self.scene().removeItem(each_method.add_param_button_proxy)
                        self.scene().removeItem(each_method.remove_param_button_proxy)
                        self.methods.remove(each_method)
                        self.update_method_text()
                        return
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "No methods to remove.")
            
    def remove_all_method(self):
        if len(self.methods) > 0:
            # Create a copy of the methods list to avoid modifying the list while iterating
            for each_method in self.methods[:]:  # Using slicing [:] to create a copy
                # Remove the button proxies from the scene
                self.scene().removeItem(each_method.add_param_button_proxy)
                self.scene().removeItem(each_method.remove_param_button_proxy)
                # Remove the method from the list
                self.methods.remove(each_method)
            self.update_method_text()  # Update the graphical representation of methods
            
    #################################################################
    ### MEMBER FUNCTIONS ###

    ## BOX RELATED ##

    def create_resize_handles(self):
        """
        Create resize handles at the bottom-right corner of the class box.
        """
        self.handles = {
            'bottom_right': QtWidgets.QGraphicsEllipseItem(
                0, 0, self.handle_size, self.handle_size, self
            )
        }

        for handle in self.handles.values():
            handle.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 255)))  # Set handle color
            handle.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
            handle.setAcceptHoverEvents(True)  # Enable hover events
            handle.hoverEnterEvent = self.handle_hoverEnterEvent
            handle.hoverLeaveEvent = self.handle_hoverLeaveEvent

    def update_positions(self):
        """
        Update the positions of text items, handles, and connection points.
        """
        # Calculate heights of all text sections
        class_name_height = self.class_name_text.boundingRect().height()
        fields_label_height = self.fields_label.boundingRect().height()
        fields_text_height = self.field_text.boundingRect().height()
        methods_label_height = self.methods_label.boundingRect().height()
        methods_text_height = self.methods_text.boundingRect().height()

        # Set positions of text items relative to each other #
        self.centering_class_name()
        self.fields_label.setPos(self.default_margin, class_name_height + 2 * self.default_margin)
        self.field_text.setPos(self.default_margin + 10, class_name_height + fields_label_height + 3 * self.default_margin)
        self.methods_label.setPos(self.default_margin, class_name_height + fields_label_height + fields_text_height + 4 * self.default_margin)
        self.methods_text.setPos(self.default_margin + 10, class_name_height + fields_label_height + fields_text_height + methods_label_height + 5 * self.default_margin)
        self.add_field_button_proxy.setPos(self.default_margin + 34, class_name_height + 21)
        self.remove_field_button_proxy.setPos(self.default_margin + 49, class_name_height + 21)
        self.add_method_button_proxy.setPos(self.default_margin + 48, class_name_height + fields_text_height + 62)
        self.remove_method_button_proxy.setPos(self.default_margin + 63, class_name_height + fields_text_height + 62)

        # Update positions for each method's buttons
        for i, method in enumerate(self.methods):
            button_y_pos = self.method_y_position(i)
            method.add_param_button_proxy.setPos(self.methods_text.boundingRect().width() + self.pos().x() + self.default_margin + 20, self.pos().y() + button_y_pos)
            method.remove_param_button_proxy.setPos(self.methods_text.boundingRect().width() + self.pos().x() + self.default_margin + 33, self.pos().y() + button_y_pos)
            method.update_param_position()
            
        # Get param button's height
        param_button_height = 0
        if len(self.methods) > 0:
            param_button_height = self.get_param_text_height(len(self.methods) - 1)
        
        # Calculate total height of the box
        total_height = (
            class_name_height + fields_label_height + fields_text_height + methods_label_height + methods_text_height + 6 * self.default_margin + param_button_height
        )

        # Calculate maximum width based on content
        max_width_button = self.get_longest_button_width() + 30
        max_param_length = self.get_longest_param_text() + 30
        
        self.max_width = max(
            self.default_width,
            self.class_name_text.boundingRect().width() + 2 * self.default_margin,
            self.fields_label.boundingRect().width() + 2 * self.default_margin,
            self.field_text.boundingRect().width() + 2 * self.default_margin,
            self.methods_label.boundingRect().width() + 2 * self.default_margin,
            self.methods_text.boundingRect().width() + 2 * self.default_margin,
            max_width_button + 2 * self.default_margin, 
            max_param_length + 2 * self.default_margin
        )
        
        print(f"Max width = {self.max_width}")

        # Update the box size only if not being resized manually
        if not self.is_resizing and not self.is_box_dragged:
            self.setRect(0, 0, self.max_width, total_height)
            self.user_width = self.max_width  # Keep track of current user-defined width
            self.user_height = total_height  # Keep track of current user-defined height

        # Update the positions of the separator lines
        self.update_separators()

        # Position the resize handle
        self.handles['bottom_right'].setPos(
            self.rect().width() - self.handle_size // 2,
            self.rect().height() - self.handle_size // 2
        )

        # Update positions of connection points
        self.update_connection_point_positions()
        
    def centering_class_name(self):
        # Get the width of the class box
        box_width = self.rect().width()
        class_name_width = self.class_name_text.boundingRect().width()
        class_name_x_pos = (box_width - class_name_width) / 2
        self.class_name_text.setPos(class_name_x_pos, self.default_margin)
        
    def get_param_text_height(self, index: int):
        return self.methods[index].param_text.boundingRect().height()
        
    def get_longest_button_width(self):
        # Initialize variables to track the maximum width and corresponding method
        max_width_button = 0

        # Iterate through each method to find the one with the maximum button width
        for method in self.methods:
            button_width = method.remove_param_button_proxy.boundingRect().width() + self.methods_text.boundingRect().width() + 2 * self.default_margin
            if button_width > max_width_button:  # Check if this button is wider than the current max
                max_width_button = button_width  # Update max width 
        return max_width_button
    
    def get_longest_param_text(self):
        # Initialize variables to track the maximum length
        max_param_length = 0
        # Iterate through each method to find the longest parameter
        for method in self.methods:
            for each_param in method.parameters:
                current_length = len(each_param) + method.remove_param_button_proxy.boundingRect().width() + method.param_text.boundingRect().width() + 2 * self.default_margin
                if current_length >= max_param_length:
                    max_param_length = current_length
        return max_param_length

    def update_separators(self):
        """
        Update positions of the separator lines based on current box size.
        """
        rect = self.rect()
        if hasattr(self, 'separator_line1'):
            # Update existing separator lines
            self.separator_line1.setLine(0, self.class_name_text.boundingRect().height() + self.default_margin, rect.width(), self.class_name_text.boundingRect().height() + self.default_margin)  # Line below class name
            self.separator_line2.setLine(0, self.class_name_text.boundingRect().height() + self.fields_label.boundingRect().height() + self.field_text.boundingRect().height() + 3 * self.default_margin, rect.width(), self.class_name_text.boundingRect().height() + self.fields_label.boundingRect().height() + self.field_text.boundingRect().height() + 3 * self.default_margin)  # Line below fields
        else:
            # Create separator lines if they don't exist
            self.separator_line1 = QtWidgets.QGraphicsLineItem(
                0, self.class_name_text.boundingRect().height() + self.default_margin, rect.width(), self.class_name_text.boundingRect().height() + self.default_margin, self
            )
            self.separator_line2 = QtWidgets.QGraphicsLineItem(
                0, self.class_name_text.boundingRect().height() + self.fields_label.boundingRect().height() + self.field_text.boundingRect().height() + 3 * self.default_margin, rect.width(), self.class_name_text.boundingRect().height() + self.fields_label.boundingRect().height() + self.field_text.boundingRect().height() + 3 * self.default_margin, self
            )
            self.separator_line1.setPen(QtGui.QPen(QtCore.Qt.black))
            self.separator_line2.setPen(QtGui.QPen(QtCore.Qt.black))

    #################################################################
    ### CONNECTION POINTS AND ARROWS ###

    def create_connection_points(self):
        """
        Create connection points (dots) for arrow connections.
        """
        self.connection_points = {}  # Dictionary to store positions
        self.connection_point_items = {}  # Dictionary to store the ellipse items

        # Create connection points at 'top', 'bottom', 'left', 'right' of the box
        for key in ['top', 'bottom', 'left', 'right']:
            cp_item = QtWidgets.QGraphicsEllipseItem(-5, -5, 10, 10, self)
            cp_item.setBrush(QtGui.QBrush(QtGui.QColor(0, 150, 0)))  # Dark green color
            cp_item.setPen(QtGui.QPen(QtCore.Qt.black))
            cp_item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
            cp_item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
            self.connection_point_items[key] = cp_item  # Store the item

        self.update_connection_point_positions()  # Position the connection points

    def update_connection_point_positions(self):
        """
        Update positions of the connection point items based on box size.
        """
        rect = self.rect()

        # Calculate positions for 'top', 'bottom', 'left', 'right' points
        self.connection_points = {
            'top': QtCore.QPointF(rect.center().x(), rect.top()),
            'bottom': QtCore.QPointF(rect.center().x(), rect.bottom()),
            'left': QtCore.QPointF(rect.left(), rect.center().y()),
            'right': QtCore.QPointF(rect.right(), rect.center().y())
        }

        # Move the ellipse items to the calculated positions
        self.connection_point_items['top'].setPos(self.connection_points['top'])
        self.connection_point_items['bottom'].setPos(self.connection_points['bottom'])
        self.connection_point_items['left'].setPos(self.connection_points['left'])
        self.connection_point_items['right'].setPos(self.connection_points['right'])

    def getConnectionPoints(self):
        """
        Return the scene positions of the connection points.

        Returns:
        - dict: A dictionary with keys as connection point names and values as QPointF positions.
        """
        scenePoints = {}
        for key, cp_item in self.connection_point_items.items():
            # Adjust position to center of the ellipse
            scenePoints[key] = cp_item.scenePos() + QtCore.QPointF(5, 5)
        return scenePoints

    def addArrow(self, arrow):
        """
        Add an arrow to the list of connected arrows.

        Parameters:
        - arrow (Arrow): The arrow to add.
        """
        self.arrows.append(arrow)

    def removeArrow(self, arrow):
        """
        Remove an arrow from the list of connected arrows.

        Parameters:
        - arrow (Arrow): The arrow to remove.
        """
        if arrow in self.arrows:
            self.arrows.remove(arrow)

    def itemChange(self, change, value):
        """
        Override to update arrows when the class box moves.

        Parameters:
        - change (GraphicsItemChange): The type of change.
        - value (Any): The value associated with the change.

        Returns:
        - Any: The result of the base class itemChange method.
        """
        if change == QtWidgets.QGraphicsItem.ItemPositionHasChanged:
            for arrow in self.arrows:
                arrow.updatePosition()
        return super().itemChange(change, value)

    #################################################################
    ## MOUSE RELATED ##

    def handle_hoverEnterEvent(self, event):
        """
        Change cursor to resize when hovering over the resize handle.

        Parameters:
        - event (QGraphicsSceneHoverEvent): The hover event.
        """
        self.setCursor(QtCore.Qt.SizeFDiagCursor)  # Set cursor to diagonal resize
        event.accept()

    def handle_hoverLeaveEvent(self, event):
        """
        Reset cursor when leaving the resize handle.

        Parameters:
        - event (QGraphicsSceneHoverEvent): The hover event.
        """
        self.setCursor(QtCore.Qt.ArrowCursor)  # Reset cursor to default arrow
        event.accept()

    def mousePressEvent(self, event):
        """
        Handle mouse press events for dragging or resizing.

        Parameters:
        - event (QGraphicsSceneMouseEvent): The mouse event.
        """
        if event.button() == QtCore.Qt.LeftButton:
            if self.isUnderMouse() and not any(
                handle.isUnderMouse() for handle in self.handles.values()
            ):
                self.is_box_dragged = True  # Start dragging the box
            elif any(handle.isUnderMouse() for handle in self.handles.values()):
                # Determine which handle is being pressed for resizing
                for handle_name, handle in self.handles.items():
                    if handle.isUnderMouse():
                        self.current_handle = handle_name
                        self.is_resizing = True
                        break
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """
        Handle mouse move events for dragging or resizing.

        Parameters:
        - event (QGraphicsSceneMouseEvent): The mouse event.
        """
        if self.is_resizing and self.current_handle is not None:
            new_rect = self.rect()

            # Calculate new width and height based on mouse position
            new_width = event.pos().x() - new_rect.x()
            new_height = event.pos().y() - new_rect.y()
            
            # Get param button's height
            param_button_height = 0
            if len(self.methods) > 0:
                param_button_height = self.get_param_text_height(len(self.methods) - 1)

            # Set minimum width and height
            min_height = (
                self.class_name_text.boundingRect().height()
                + self.fields_label.boundingRect().height()
                + self.field_text.boundingRect().height()
                + self.methods_label.boundingRect().height()
                + self.methods_text.boundingRect().height()
                + 6 * self.default_margin
                + param_button_height
            )
            
            self.min_height = min_height
            
           # Calculate the maximum width needed based on the longest text in each section #
    
            # Calculate maximum width based on content
            max_width_button = self.get_longest_button_width() + 10
            max_param_length = self.get_longest_param_text()
            
            longest_string_width = max(
                self.class_name_text.boundingRect().width(),
                self.fields_label.boundingRect().width(),
                self.field_text.boundingRect().width(),
                self.methods_label.boundingRect().width(),
                self.methods_text.boundingRect().width(),
                max_width_button, max_param_length
            ) + 20  # Add some padding

            
            # Ensure the box does not overlap with text (min_width now depends on text length)
            if new_width >= longest_string_width:
                new_rect.setWidth(new_width)
            else:
                new_rect.setWidth(longest_string_width)

            if new_height >= min_height:
                new_rect.setHeight(new_height)
            
            # Apply new size and update positions
            self.setRect(new_rect)
            self.update_positions()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Handle mouse release events to stop dragging or resizing.

        Parameters:
        - event (QGraphicsSceneMouseEvent): The mouse event.
        """
        if self.is_box_dragged:
            self.snap_to_grid()  # Snap box to grid
            event.accept()
            self.is_box_dragged = False  # Reset dragging flag
        elif self.is_resizing:
            self.is_resizing = False  # Reset resizing flag
            self.current_handle = None  # Reset current handle

        super().mouseReleaseEvent(event)

    def snap_to_grid(self, current_grid_size=20):
        """
        Snap the class box to the nearest grid position.

        Parameters:
        - current_grid_size (int): The size of the grid to snap to.
        """
        grid_size = current_grid_size * self.transform().m11()  # Adjust for zoom
        pos = self.pos()

        # Calculate new x and y positions
        new_x = round(pos.x() / grid_size) * grid_size
        new_y = round(pos.y() / grid_size) * grid_size

        # Set new position and update
        self.setPos(new_x, new_y)
        self.update_positions()