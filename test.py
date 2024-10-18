import math
import sys

from PyQt5 import QtCore, QtGui, QtWidgets


class Arrow(QtWidgets.QGraphicsLineItem):
    def __init__(self, startItem, endItem, startKey, endKey):
        super().__init__()
        self.startItem = startItem
        self.endItem = endItem
        self.startKey = startKey
        self.endKey = endKey

        # Set pen properties
        pen = QtGui.QPen(QtCore.Qt.black)
        pen.setWidth(2)
        self.setPen(pen)

        # Set arrowhead size
        self.arrowSize = 10

        # Add arrow to items
        self.startItem.addArrow(self)
        self.endItem.addArrow(self)

        # Connect the movement signals of the boxes to update the arrow position
        self.startItem.positionChanged.connect(self.updatePosition)
        self.endItem.positionChanged.connect(self.updatePosition)

        # Update initial position
        self.updatePosition()

    def updatePosition(self):
        startPoints = self.startItem.getConnectionPoints()
        endPoints = self.endItem.getConnectionPoints()

        if self.startKey in startPoints and self.endKey in endPoints:
            startPoint = startPoints[self.startKey]
            endPoint = endPoints[self.endKey]

            line = QtCore.QLineF(startPoint, endPoint)
            self.setLine(line)

    def paint(self, painter, option, widget=None):
        painter.setPen(self.pen())
        line = self.line()
        painter.drawLine(line)

        angle = math.atan2(-line.dy(), line.dx())

        arrowP1 = line.p2() - QtCore.QPointF(
            math.sin(angle + math.pi / 3) * self.arrowSize,
            math.cos(angle + math.pi / 3) * self.arrowSize,
        )
        arrowP2 = line.p2() - QtCore.QPointF(
            math.sin(angle + math.pi - math.pi / 3) * self.arrowSize,
            math.cos(angle + math.pi - math.pi / 3) * self.arrowSize,
        )

        arrowHead = QtGui.QPolygonF([line.p2(), arrowP1, arrowP2])
        painter.drawPolygon(arrowHead)


class MovableBox(QtWidgets.QGraphicsRectItem):
    # Signal to notify when the position of the box changes
    positionChanged = QtCore.pyqtSignal()

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setBrush(QtGui.QBrush(QtGui.QColor(100, 100, 250)))
        self.arrows = []

        # Create connection points as visible circles
        self.connectionPointsItems = {
            "top": self.createConnectionPoint(),
            "bottom": self.createConnectionPoint(),
            "left": self.createConnectionPoint(),
            "right": self.createConnectionPoint(),
        }
        self.updateConnectionPointsPositions()

    def createConnectionPoint(self):
        """
        Create a visible connection point on the box.
        """
        point = QtWidgets.QGraphicsEllipseItem(-5, -5, 10, 10, self)
        point.setBrush(QtGui.QBrush(QtCore.Qt.red))
        return point

    def updateConnectionPointsPositions(self):
        """
        Update the positions of the connection points relative to the box.
        """
        rect = self.rect()
        self.connectionPointsItems["top"].setPos(rect.center().x(), rect.top())
        self.connectionPointsItems["bottom"].setPos(rect.center().x(), rect.bottom())
        self.connectionPointsItems["left"].setPos(rect.left(), rect.center().y())
        self.connectionPointsItems["right"].setPos(rect.right(), rect.center().y())

    def addArrow(self, arrow):
        self.arrows.append(arrow)

    def getConnectionPoints(self):
        rect = self.rect()
        return {
            "top": QtCore.QPointF(rect.center().x(), rect.top()) + self.pos(),
            "bottom": QtCore.QPointF(rect.center().x(), rect.bottom()) + self.pos(),
            "left": QtCore.QPointF(rect.left(), rect.center().y()) + self.pos(),
            "right": QtCore.QPointF(rect.right(), rect.center().y()) + self.pos(),
        }

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemPositionChange:
            # Emit positionChanged signal whenever the box position changes
            self.positionChanged.emit()
            self.updateConnectionPointsPositions()
        return super().itemChange(change, value)


class ArrowScene(QtWidgets.QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.startItem = None
        self.startKey = None
        self.line = None

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            item = self.itemAt(event.scenePos(), QtGui.QTransform())
            if isinstance(item, MovableBox):
                # Find the closest connection point
                connectionPoints = item.getConnectionPoints()
                min_distance = None
                closest_key = None
                for key, point in connectionPoints.items():
                    distance = QtCore.QLineF(event.scenePos(), point).length()
                    if min_distance is None or distance < min_distance:
                        min_distance = distance
                        closest_key = key

                if closest_key is not None:
                    self.startItem = item
                    self.startKey = closest_key

                    # Create a temporary line from the closest connection point
                    startPos = connectionPoints[closest_key]
                    self.line = QtWidgets.QGraphicsLineItem(
                        QtCore.QLineF(startPos, startPos)
                    )
                    pen = QtGui.QPen(QtCore.Qt.black)
                    pen.setWidth(2)
                    self.line.setPen(pen)
                    self.addItem(self.line)
                    event.accept()

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.line:
            # Update the temporary line to the current mouse position
            newLine = QtCore.QLineF(self.line.line().p1(), event.scenePos())
            self.line.setLine(newLine)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Handle mouse release events to finish drawing arrows.
        """
        if event.button() == QtCore.Qt.RightButton and self.line:
            # Finish drawing the arrow
            scene_pos = event.scenePos()  # scenePos is already in scene coordinates
            items = self.items(scene_pos)
            items = [item for item in items if isinstance(item, MovableBox)]
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

                                # Check if an arrow between these boxes already exists
                                arrow_exists = any(
                                    arrow.startItem == self.startItem
                                    and arrow.endItem == self.endItem
                                    for arrow in self.startItem.arrows
                                )

                                if arrow_exists:
                                    # Don't create a duplicate arrow
                                    if self.line:
                                        self.removeItem(self.line)
                                        self.line = None
                                    QtWidgets.QMessageBox.warning(
                                        None,
                                        "Duplicate Relationship",
                                        "An arrow between these boxes already exists.",
                                    )
                                else:
                                    # Remove the temporary line and create the arrow
                                    if self.line:
                                        self.removeItem(self.line)
                                        self.line = None
                                    arrow = Arrow(
                                        self.startItem,
                                        self.endItem,
                                        self.startKey,
                                        self.endKey,
                                    )
                                    self.addItem(arrow)
                    except Exception as e:
                        print(f"Error during arrow creation: {e}")
                        if self.line:
                            self.removeItem(self.line)
                            self.line = None
                else:
                    # Same item clicked or invalid start/released item; remove temporary line
                    if self.line:
                        self.removeItem(self.line)
                        self.line = None
            else:
                # No valid item under cursor; remove temporary line
                if self.line:
                    self.removeItem(self.line)
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


class MainWindow(QtWidgets.QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = ArrowScene()
        self.setScene(self.scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)

        # Add three movable boxes to the scene
        box1 = MovableBox(50, 50, 100, 100)
        box2 = MovableBox(250, 150, 100, 100)
        box3 = MovableBox(450, 50, 100, 100)

        self.scene.addItem(box1)
        self.scene.addItem(box2)
        self.scene.addItem(box3)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle(
        "Arrow Drawing Example with Updated Arrow Tracking (Signals & Slots)"
    )
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
