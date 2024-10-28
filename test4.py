import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QDialog, QComboBox, QLabel, QDialogButtonBox
from PyQt5.QtCore import Qt, QPointF, QPoint
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPolygonF, QMouseEvent

class BoxWidget(QWidget):
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name
        self.setFixedSize(100, 100)
        self.connection_points = {
            "top": QPoint(self.width() // 2, 0),
            "bottom": QPoint(self.width() // 2, self.height()),
            "left": QPoint(0, self.height() // 2),
            "right": QPoint(self.width(), self.height() // 2)
        }
        self.setStyleSheet("background-color: lightblue;")
        self.is_moving = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(QColor("lightblue")))
        painter.drawRect(self.rect())
        painter.setBrush(QBrush(QColor("red")))
        for point in self.connection_points.values():
            painter.drawEllipse(point, 5, 5)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.is_moving = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.is_moving:
            self.move(self.mapToParent(event.pos() - self.offset))
            self.parent().update()  # Redraw connections in parent

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.is_moving = False

    def get_global_connection_points(self):
        """Returns the connection points in global coordinates."""
        return {name: self.mapToParent(point) for name, point in self.connection_points.items()}

class RelationshipDialog(QDialog):
    def __init__(self, box_names, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create Relationship")
        self.setFixedSize(250, 150)
        layout = QVBoxLayout(self)
        
        self.label = QLabel("Do you want to create a relationship?")
        layout.addWidget(self.label)
        
        self.combo_box_1 = QComboBox()
        self.combo_box_1.addItems(box_names)
        layout.addWidget(self.combo_box_1)
        
        self.combo_box_2 = QComboBox()
        self.combo_box_2.addItems(box_names)
        layout.addWidget(self.combo_box_2)
        
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
    
    def get_selections(self):
        return self.combo_box_1.currentText(), self.combo_box_2.currentText()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Box Relationship Creator")
        self.setGeometry(100, 100, 600, 400)

        # Layout setup
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        
        # Initialize boxes
        self.box1 = BoxWidget("Box 1")
        self.box1.move(150, 150)
        self.box2 = BoxWidget("Box 2")
        self.box2.move(400, 150)
        
        # Add boxes to layout
        self.layout.addWidget(self.box1)
        self.layout.addWidget(self.box2)

        # Create relationship button
        self.button = QPushButton("Create Relationship")
        self.button.clicked.connect(self.create_relationship)
        self.layout.addWidget(self.button)
        
        # Set layout
        self.setCentralWidget(self.central_widget)
        self.relationships = []  # Store relationships as pairs of boxes
    
    def create_relationship(self):
        # Open dialog to select boxes
        dialog = RelationshipDialog(["Box 1", "Box 2"], self)
        if dialog.exec_() == QDialog.Accepted:
            box1_name, box2_name = dialog.get_selections()
            if box1_name == box2_name:
                return  # Cannot create relationship with the same box
            
            # Get box references
            box1 = self.box1 if box1_name == "Box 1" else self.box2
            box2 = self.box1 if box2_name == "Box 1" else self.box2
            
            # Store relationship
            self.relationships.append((box1, box2))
            self.update()

    def paintEvent(self, event):
        # Draw relationships (arrows) between boxes
        painter = QPainter(self)
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        for box1, box2 in self.relationships:
            # Find the optimal connection points between the two boxes
            start, end = self.closest_connection_points(box1, box2)
            painter.drawLine(start, end)
            self.draw_arrow(painter, start, end)

    def closest_connection_points(self, box1, box2):
        """Finds the pair of closest connection points between two boxes."""
        box1_points = box1.get_global_connection_points()
        box2_points = box2.get_global_connection_points()

        # Find the closest pair of points
        closest_pair = None
        min_distance = float('inf')
        for p1 in box1_points.values():
            for p2 in box2_points.values():
                distance = (p1 - p2).manhattanLength()  # Manhattan length for simplicity
                if distance < min_distance:
                    min_distance = distance
                    closest_pair = (p1, p2)
        return closest_pair

    def draw_arrow(self, painter, start, end):
        # Draw arrowhead
        angle = math.radians(30)  # Arrowhead angle
        line_angle = math.atan2(end.y() - start.y(), end.x() - start.x())
        arrow_size = 10
        p1 = end - QPointF(arrow_size * math.cos(line_angle + angle), arrow_size * math.sin(line_angle + angle))
        p2 = end - QPointF(arrow_size * math.cos(line_angle - angle), arrow_size * math.sin(line_angle - angle))
        painter.setBrush(Qt.black)
        painter.drawPolygon(QPolygonF([end, p1, p2]))

        # Draw line connecting the boxes, precisely from start to end points
        painter.drawLine(start, end)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
