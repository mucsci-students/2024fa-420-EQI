import sys
from PyQt5 import QtWidgets, QtCore, QtGui


class Box(QtWidgets.QGraphicsRectItem):
    """
    A simple rectangular box that can be selected, copied, and pasted.
    """
    def __init__(self, x, y, width, height, color=QtGui.QColor("lightblue")):
        super().__init__(x, y, width, height)
        self.setBrush(QtGui.QBrush(color))
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)


class GraphicsView(QtWidgets.QGraphicsView):
    """
    Custom QGraphicsView that supports adding, copying, and pasting boxes,
    as well as selecting items by dragging a rectangular selection area.
    """
    def __init__(self):
        super().__init__()
        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        
        # To store the copied box
        self.copied_box = None
        
        # For the rectangular selection feature
        self.rubber_band = None  # Selection rectangle
        self.origin_point = QtCore.QPointF()  # Starting point of the selection

    def add_box(self, x=0, y=0, width=100, height=100):
        """
        Add a new box to the scene.
        """
        box = Box(x, y, width, height)
        self.scene.addItem(box)

    def copy_selected_box(self):
        """
        Copy the selected box if one is selected.
        """
        selected_items = self.scene.selectedItems()
        if selected_items:
            # Copy the first selected item (for simplicity)
            self.copied_box = selected_items[0]

    def paste_box(self):
        """
        Paste the copied box at a new location if one has been copied.
        """
        if self.copied_box:
            # Create a new box with the same dimensions and color as the copied one
            rect = self.copied_box.rect()
            new_box = Box(0, 0, rect.width(), rect.height(), self.copied_box.brush().color())
            new_box.setPos(self.copied_box.pos() + QtCore.QPointF(20, 20))  # Paste with a small offset
            self.scene.addItem(new_box)

    def mousePressEvent(self, event):
        """
        Handle mouse press events, including starting the rectangular selection.
        """
        if event.button() == QtCore.Qt.LeftButton:
            self.origin_point = self.mapToScene(event.pos())
            self.rubber_band = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self.viewport())
            self.rubber_band.setGeometry(QtCore.QRect(event.pos(), event.pos()))
            self.rubber_band.show()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """
        Handle mouse move events, including updating the rectangular selection area.
        """
        if self.rubber_band:
            rect = QtCore.QRectF(self.origin_point, self.mapToScene(event.pos())).normalized()
            self.rubber_band.setGeometry(self.mapFromScene(rect).boundingRect())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Handle mouse release events, including finalizing the rectangular selection.
        """
        if self.rubber_band:
            rubber_band_rect = self.rubber_band.geometry()
            selection_rect = self.mapToScene(rubber_band_rect).boundingRect()
            self.select_items_in_rect(selection_rect)
            self.rubber_band.hide()
            self.rubber_band = None
        super().mouseReleaseEvent(event)
        
        
    def select_items_in_rect(self, rect):
        """
        Select all items within the provided rectangular area.
        """
        items_in_rect = self.scene.items(rect)
        for item in self.scene.selectedItems():
            item.setSelected(False)  # Deselect previously selected items
        for item in items_in_rect:
            item.setSelected(True)  # Select new items in the rectangle


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.view = GraphicsView()
        self.setCentralWidget(self.view)

        # Create the toolbar with Add, Copy, and Paste actions
        toolbar = self.addToolBar("Tools")
        add_action = toolbar.addAction("Add Box")
        copy_action = toolbar.addAction("Copy")
        paste_action = toolbar.addAction("Paste")
        
        # Connect toolbar actions to their respective functions
        add_action.triggered.connect(self.add_box)
        copy_action.triggered.connect(self.copy_box)
        paste_action.triggered.connect(self.paste_box)

    def add_box(self):
        self.view.add_box(0, 0, 100, 100)

    def copy_box(self):
        self.view.copy_selected_box()

    def paste_box(self):
        self.view.paste_box()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Rectangular Selection and Copy-Paste Example")
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
