###################################################################################################

from PyQt5 import QtWidgets, QtGui, QtCore
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_class_box import UMLClassBox
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_arrow_line import Arrow
from UML_MVC.UML_VIEW.UML_GUI_VIEW.uml_gui_class_box import Method

###################################################################################################

class GridGraphicsView(QtWidgets.QGraphicsView):
    """
    A custom graphics view that displays a grid pattern and handles user interactions.
    Inherits from QGraphicsView.
    """

    #################################################################
    ### CONSTRUCTOR ###

    def __init__(self, interface, parent=None, grid_size=20, color=QtGui.QColor(200, 200, 200)):
        """
        Initializes a new GridGraphicsView instance.

        Parameters:
        - parent (QWidget): The parent widget.
        - grid_size (int): The spacing between grid lines in pixels.
        - color (QColor): The color of the grid lines.
        """
        super().__init__(QtWidgets.QGraphicsScene(parent), parent)

        # Interface to communicate with UMLCoreManager
        self.interface = interface  
        
        # Initialize grid properties
        self.grid_visible = True  # Flag to show/hide the grid
        self.is_dark_mode = False  # Flag for light/dark mode
        self.grid_size = grid_size  # Grid spacing
        self.grid_color = color  # Grid line color

        # Set initial view properties
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setSceneRect(-5000, -5000, 10000, 10000)  # Large scene size
        self.setScene(self.scene())

        # Panning state variables
        self.is_panning = False  # Flag to indicate if panning is active
        self.last_mouse_pos = None  # Last mouse position during panning

        # Track selected class or arrow
        self.selected_class = None
        self.selected_arrow = None  # NEW: Track selected arrow

        # Variables for arrow drawing
        self.startItem = None
        self.endItem = None
        self.startPoint = None
        self.endPoint = None
        self.startKey = None
        self.endKey = None
        self.line = None

    #################################################################
    ## GRID VIEW RELATED ##

    def scale(self, sx, sy):
        """
        Override scale method to resize class boxes when zooming.

        Parameters:
        - sx (float): Scaling factor in x-direction.
        - sy (float): Scaling factor in y-direction.
        """
        super().scale(sx, sy)

        # Resize UMLClassBox items in the scene
        for item in self.scene().items():
            if isinstance(item, UMLClassBox):
                current_rect = item.rect()
                new_width = current_rect.width() * sx
                new_height = current_rect.height() * sy
                item.setRect(0, 0, new_width, new_height)
                item.update_positions()

    def drawBackground(self, painter, rect):
        """
        Draw the background grid pattern.

        Parameters:
        - painter (QPainter): The painter object.
        - rect (QRectF): The area to be painted.
        """
        # Fill background based on mode
        if self.is_dark_mode:
            painter.fillRect(rect, QtGui.QColor(30, 30, 30))
        else:
            painter.fillRect(rect, QtGui.QColor(255, 255, 255))

        if self.grid_visible:
            # Set pen for grid lines
            pen = QtGui.QPen(self.grid_color)
            pen.setWidth(1)
            painter.setPen(pen)

            # Calculate starting points for grid lines
            left = int(rect.left()) - (int(rect.left()) % self.grid_size)
            top = int(rect.top()) - (int(rect.top()) % self.grid_size)

            # Draw vertical grid lines
            for x in range(left, int(rect.right()), self.grid_size):
                painter.drawLine(x, int(rect.top()), x, int(rect.bottom()))

            # Draw horizontal grid lines
            for y in range(top, int(rect.bottom()), self.grid_size):
                painter.drawLine(int(rect.left()), y, int(rect.right()), y)

            # Draw origin lines
            origin_pen = QtGui.QPen(QtGui.QColor(255, 0, 0))
            origin_pen.setWidth(2)
            painter.setPen(origin_pen)
            painter.drawLine(int(rect.left()), 0, int(rect.right()), 0)  # Horizontal line at y=0
            painter.drawLine(0, int(rect.top()), 0, int(rect.bottom()))  # Vertical line at x=0

            painter.setPen(pen)  # Reset pen

    #################################################################
    ## MOUSE RELATED ##

    def wheelEvent(self, event):
        """
        Handle zoom in/out functionality using the mouse wheel.

        Parameters:
        - event (QWheelEvent): The wheel event.
        """
        if event.modifiers() & QtCore.Qt.ControlModifier:
            delta = event.angleDelta().y()
            zoom_limit = 0.5
            max_zoom_limit = 10.0
            current_scale = self.transform().m11()

            # Zoom in or out based on wheel movement
            if delta > 0 and current_scale < max_zoom_limit:
                self.scale(1.1, 1.1)
            elif delta < 0 and current_scale > zoom_limit:
                self.scale(0.9, 0.9)

            self.update_snap()  # Snap items to grid
            self.viewport().update()
            event.accept()
        else:
            event.ignore()

    def mousePressEvent(self, event):
        """
        Handle mouse press events for panning or starting arrow drawing.

        Parameters:
        - event (QMouseEvent): The mouse event.
        """
        # Determine the item under the mouse cursor
        item = self.itemAt(event.pos())
        if isinstance(item, UMLClassBox):
            self.selected_class = item
            self.selected_arrow = None  # Deselect any arrow
        elif isinstance(item, Arrow):
            self.selected_arrow = item  # Select the arrow
            self.selected_class = None  # Deselect any class
        else:
            self.selected_class = None
            self.selected_arrow = None

        if event.button() == QtCore.Qt.MiddleButton:
            # Start panning
            self.is_panning = True
            self.last_mouse_pos = event.pos()
            self.setCursor(QtCore.Qt.ClosedHandCursor)
            event.accept()
        elif event.button() == QtCore.Qt.RightButton:
            # Start drawing an arrow
            scene_pos = self.mapToScene(event.pos())
            items = self.scene().items(scene_pos)
            items = [item for item in items if isinstance(item, UMLClassBox)]
            if items:
                clicked_item = items[0]
                # Find the closest connection point
                connectionPoints = clicked_item.getConnectionPoints()
                if connectionPoints:
                    min_distance = None
                    closest_point = None
                    closest_key = None
                    for key, point in connectionPoints.items():
                        distance = QtCore.QLineF(scene_pos, point).length()
                        if min_distance is None or distance < min_distance:
                            min_distance = distance
                            closest_point = point
                            closest_key = key

                    if closest_point and closest_key:
                        self.startItem = clicked_item
                        self.startPoint = closest_point
                        self.startKey = closest_key

                        # Create a temporary line for the arrow
                        self.line = QtWidgets.QGraphicsLineItem(
                            QtCore.QLineF(self.startPoint, self.startPoint)
                        )
                        pen = QtGui.QPen(QtCore.Qt.white) if self.is_dark_mode else QtGui.QPen(QtCore.Qt.black)
                        pen.setWidth(2)
                        self.line.setPen(pen)
                        self.line.setZValue(2)
                        self.scene().addItem(self.line)
                        event.accept()
            else:
                super().mousePressEvent(event)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """
        Handle mouse move events for panning or updating the temporary arrow.

        Parameters:
        - event (QMouseEvent): The mouse event.
        """
        if self.is_panning and self.last_mouse_pos is not None:
            # Panning the view
            delta = event.pos() - self.last_mouse_pos
            self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
            self.translate(delta.x(), delta.y())
            self.last_mouse_pos = event.pos()
            self.viewport().update()
            event.accept()
        elif self.line:
            # Update the temporary arrow line during drawing
            new_end = self.mapToScene(event.pos())
            if self.startPoint:
                newLine = QtCore.QLineF(self.startPoint, new_end)
                self.line.setLine(newLine)
                event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Handle mouse release events to end panning or finish drawing arrows.

        Parameters:
        - event (QMouseEvent): The mouse event.
        """
        if event.button() == QtCore.Qt.MiddleButton and self.is_panning:
            # End panning
            self.is_panning = False
            self.last_mouse_pos = None
            self.setCursor(QtCore.Qt.ArrowCursor)
            event.accept()
        elif event.button() == QtCore.Qt.RightButton and self.line:
            # Finish drawing the arrow
            scene_pos = self.mapToScene(event.pos())
            items = self.scene().items(scene_pos)
            items = [item for item in items if isinstance(item, UMLClassBox)]
            if items:
                released_item = items[0]
                if released_item and self.startItem and released_item != self.startItem:
                    try:
                        # Find the closest connection point on the released item
                        connectionPoints = released_item.getConnectionPoints()
                        if connectionPoints:
                            min_distance = None
                            closest_point = None
                            closest_key = None
                            for key, point in connectionPoints.items():
                                distance = QtCore.QLineF(scene_pos, point).length()
                                if min_distance is None or distance < min_distance:
                                    min_distance = distance
                                    closest_point = point
                                    closest_key = key

                            # Validate the closest point and key
                            if closest_point and closest_key:
                                self.endItem = released_item
                                self.endPoint = closest_point
                                self.endKey = closest_key

                                # Check if an arrow between these classes already exists
                                arrow_exists = any(
                                    arrow.startItem == self.startItem and arrow.endItem == self.endItem
                                    for arrow in self.startItem.arrows
                                )

                                if arrow_exists:
                                    # Don't create a duplicate arrow
                                    if self.line:
                                        self.scene().removeItem(self.line)
                                        self.line = None
                                    QtWidgets.QMessageBox.warning(
                                        self, "Duplicate Relationship",
                                        "An arrow between these classes already exists."
                                    )
                                else:
                                    # Remove the temporary line and create the arrow
                                    if self.line:
                                        self.scene().removeItem(self.line)
                                        self.line = None
                                    arrow = Arrow(
                                        self.startItem, self.endItem,
                                        self.startKey, self.endKey, self.is_dark_mode
                                    )
                                    self.scene().addItem(arrow)
                    except Exception as e:
                        print(f"Error during arrow creation: {e}")
                        if self.line:
                            self.scene().removeItem(self.line)
                            self.line = None
                else:
                    # Same item clicked or invalid start/released item; remove temporary line
                    if self.line:
                        self.scene().removeItem(self.line)
                        self.line = None
            else:
                # No valid item under cursor; remove temporary line
                if self.line:
                    self.scene().removeItem(self.line)
                    self.line = None

            # Reset variables to avoid inconsistent state
            self.startItem = None
            self.endItem = None
            self.startPoint = None
            self.endPoint = None
            self.startKey = None
            self.endKey = None
            self.line = None
            event.accept()
        else:
            super().mouseReleaseEvent(event)
            self.viewport().update()

    def keyPressEvent(self, event):
        """
        Handle key press events (e.g., Delete key to remove items).

        Parameters:
        - event (QKeyEvent): The key event.
        """
        if event.key() == QtCore.Qt.Key_Delete:
            self.delete_selected_item()
        else:
            super().keyPressEvent(event)

    #################################################################
    ## UTILITY FUNCTIONS ##

    def delete_selected_item(self):
        """
        Delete the selected class or arrow from the scene.
        """  
        if self.selected_class:
            # Remove all methods and its parameter buttons
            self.selected_class.remove_all_method()
            # Remove connected arrows first
            for arrow in self.selected_class.arrows[:]:
                arrow.startItem.removeArrow(arrow)
                arrow.endItem.removeArrow(arrow)
                self.scene().removeItem(arrow)
            # Remove the class box
            self.scene().removeItem(self.selected_class)
            self.selected_class = None
        elif self.selected_arrow:
            # Remove the arrow
            self.selected_arrow.startItem.removeArrow(self.selected_arrow)
            self.selected_arrow.endItem.removeArrow(self.selected_arrow)
            self.scene().removeItem(self.selected_arrow)
            self.selected_arrow = None

    def update_snap(self):
        """
        Snap all items to the grid after scaling.
        """
        for item in self.scene().items():
            if isinstance(item, UMLClassBox):
                item.snap_to_grid()

    def setGridVisible(self, visible):
        """
        Control the visibility of the grid lines.

        Parameters:
        - visible (bool): If True, the grid is shown; if False, it is hidden.
        """
        self.grid_visible = visible
        self.viewport().update()

    def setGridColor(self, color):
        """
        Update the color of the grid lines.

        Parameters:
        - color (QColor): The new color for the grid lines.
        """
        self.grid_color = color
        self.viewport().update()

    def resetView(self):
        """
        Reset the zoom and position to the initial state.
        """
        # for item in self.scene().items():
        #     if isinstance(item, UMLClassBox):
        #         item.centering_class_name()
        #         item.setRect(0, 0, item.max_width, item.min_height )
        #         item.update_positions()
        self.grid_size = 20
        self.resetTransform()
        self.centerOn(0, 0)

    def add_class(self):
        """
        Add a sample UML class box to the scene.
        """
        field: list[str] = []
        methods: list[dict[str, list[str]]] = []
        class_box = UMLClassBox(self.interface, class_name="Class_Name", field=field, methods=methods)
        class_box.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        class_box.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        class_box.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
        self.scene().addItem(class_box)

    def setLightMode(self):
        """
        Set the view to light mode.
        """
        self.grid_color = QtGui.QColor(200, 200, 200)
        self.is_dark_mode = False
        self.viewport().update()
        self.scene().update()

    def setDarkMode(self):
        """
        Set the view to dark mode.
        """
        self.grid_color = QtGui.QColor(255, 255, 0)
        self.is_dark_mode = True
        self.viewport().update()
        self.scene().update()

    def toggleMode(self):
        """
        Toggle between dark mode and light mode.
        """
        if self.is_dark_mode:
            self.setLightMode()
        else:
            self.setDarkMode()