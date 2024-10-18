import sys
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QPainterPath, QPainter
from PyQt5.QtWidgets import (
    QApplication, QGraphicsScene, QGraphicsView, QGraphicsPathItem, 
    QGraphicsTextItem, QGraphicsItem
)
from math import atan2, cos, sin

class Arrow(QGraphicsPathItem):
    def __init__(self, start_point, end_point, parent=None):
        super().__init__(parent)
        self.start_point = start_point
        self.end_point = end_point

        # Create a QGraphicsTextItem for the arrow label
        self.text_item = QGraphicsTextItem("Double click to edit", self)
        self.text_item.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.text_item.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.text_item.setTextInteractionFlags(Qt.NoTextInteraction)  # Start with no text interaction

        self.setPen(QPen(Qt.black, 2))
        self.update_arrow()

    def update_arrow(self):
        path = QPainterPath(self.start_point)
        path.lineTo(self.end_point)

        # Calculate the angle of the arrow line
        angle = atan2(self.end_point.y() - self.start_point.y(), self.end_point.x() - self.start_point.x())
        
        # Arrowhead dimensions
        arrow_size = 10
        arrow_p1 = QPointF(self.end_point.x() - arrow_size * cos(angle - 0.5), self.end_point.y() - arrow_size * sin(angle - 0.5))
        arrow_p2 = QPointF(self.end_point.x() - arrow_size * cos(angle + 0.5), self.end_point.y() - arrow_size * sin(angle + 0.5))

        # Add the arrowhead
        path.moveTo(self.end_point)
        path.lineTo(arrow_p1)
        path.moveTo(self.end_point)
        path.lineTo(arrow_p2)

        self.setPath(path)

        # Position the QGraphicsTextItem above the middle of the arrow
        mid_point = (self.start_point + self.end_point) / 2
        self.text_item.setPos(mid_point.x() - 50, mid_point.y() - 30)

class ArrowScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(0, 0, 800, 600)
        self.current_arrow = None
        self.start_point = None

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.start_point = event.scenePos()
            self.current_arrow = Arrow(self.start_point, self.start_point)
            self.addItem(self.current_arrow)

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.current_arrow:
            self.current_arrow.end_point = event.scenePos()
            self.current_arrow.update_arrow()

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton and self.current_arrow:
            # Finalize the arrow placement
            self.current_arrow.end_point = event.scenePos()
            self.current_arrow.update_arrow()
            self.current_arrow = None

        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        # Handle text editing on double-click
        item = self.itemAt(event.scenePos(), self.views()[0].transform())
        if isinstance(item, QGraphicsTextItem):
            item.setTextInteractionFlags(Qt.TextEditorInteraction)
            item.setFocus(Qt.MouseFocusReason)

        super().mouseDoubleClickEvent(event)

    def focusOutEvent(self, event):
        # Disable text editing once focus is lost
        for item in self.items():
            if isinstance(item, QGraphicsTextItem):
                item.setTextInteractionFlags(Qt.NoTextInteraction)
        super().focusOutEvent(event)

class ArrowView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(ArrowScene())
        self.setRenderHint(QPainter.Antialiasing)

def main():
    app = QApplication(sys.argv)
    view = ArrowView()
    view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
