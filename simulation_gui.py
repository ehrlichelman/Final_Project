import sys
import address_db

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

mouse_pos = [0, 0]


class MapIcon(QGraphicsPixmapItem):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.img = pixmap
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.isConnected = False
        addresses.add_name_addr(str(id(self)))
        # print(str(id(self)))
        address = addresses.value_by_name(str(id(self)))
        print("New Item! Address: " + address)

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton and self.isSelected():
            print("Right mouse pressed")
            ex.vScene.removeItem(self)
            addresses.remove_name(str(id(self)))
        else:
            self.setFlag(QGraphicsItem.ItemIsMovable, True)
            print("selected")
            for item in ex.vScene.items():
                if self.collidesWithItem(item) and self != item:
                    self.setFlag(QGraphicsItem.ItemIsMovable, False)
                    print("COLLISION!")
                    return

    def mouseDoubleClickEvent(self, *args, **kwargs):
        self.getNeighboursList()

    def getNeighboursList(self):
        address = addresses.value_by_name(str(id(self)))
        addresses.print_node_neighbours(address)

    def checkConnections(self):
        # reset neighbours list
        self.neighbours = []
        addr_list = []
        for item in ex.vScene.items():
            if self.collidesWithItem(item) and self != item:
                # add neighbour to list
                #address = addresses.value_by_name(str(id(item)))
                #print("Found new neighbour: " + str(address))
                self.neighbours.append(id(item))

        for x in self.neighbours:
            addr_list.append(addresses.value_by_name(x))
        print("List of neighbours: " + str(addr_list))
        #print(self.neighbours)


class MapEdge(QGraphicsPixmapItem):
    def __init__(self, x1, y1, x2, y2, front):
        super().__init__(QPixmap('img\edge.png'))
        self.rotate = 0
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.neighbours = []
        print("added new edge to map")

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton and self.isSelected():
            print("Right mouse pressed")
            ex.vScene.removeItem(self)

    def mouseDoubleClickEvent(self, *args, **kwargs):
        self.rotate += 30
        self.setRotation(self.rotate)

    def mouseReleaseEvent(self, *args, **kwargs):
        self.checkConnections()

    def checkConnections(self):
        self.setPixmap(QPixmap('img\edge.png'))
        #for x in self.neighbours:
        #   addresses.remove_name(str(x))

        self.neighbours = []
        for item in ex.vScene.items():
            if self.collidesWithItem(item) and self != item:
                print("Edge Connected !")
                self.setPixmap(QPixmap('img\edgeConnected.png'))
                # add neighbour to list
                address = addresses.value_by_name(str(id(item)))
                print(address)
                self.neighbours.append(address)

        if len(self.neighbours) > 1:
            # add neighbours to dictionary
            addresses.add_node_neighbour(self.neighbours[0], self.neighbours[1])
            addresses.add_node_neighbour(self.neighbours[1], self.neighbours[0])
            self.setFlag(QGraphicsItem.ItemIsMovable, False)


class Button(QPushButton):
    def __init__(self, title, icon):
        super().__init__()
        #self.setText(title)
        self.name = title
        self.setIcon(QIcon(QPixmap(icon)))
        self.iconFile = icon
        self.setFixedSize(35, 35)

    def mouseMoveEvent(self, e):
        print('click')
        mimeData = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        if e.button() == Qt.LeftButton:
            print('press')
            pic = QPixmap(self.iconFile)
            if self.name == 'Edge':
                new_item = MapEdge(mouse_pos[0], mouse_pos[1], 50, 50, 0)
            else:
                new_item = MapIcon(pic)
            ex.vScene.addItem(new_item)


class NetworkGraph(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        vScene = QGraphicsScene()
        self.setScene(vScene)
        self.setGeometry(0, 0, 512, 768)
        self.show()


class Example(QWidget):
    menu_buttons = []
    network_comp = []

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.setAcceptDrops(True)

        self.menuLayout = QHBoxLayout()

        # set control buttons
        self.menuLayout.addWidget(QLabel("Control Menu"))
        self.menuLayout.addWidget(QPushButton(QIcon(QPixmap("img\play.png")), "Play"))
        self.menuLayout.addWidget(QPushButton(QIcon(QPixmap("img\stop.png")), "Stop"))
        self.menuLayout.addWidget(QPushButton(QIcon(QPixmap("img\pause.png")), "Pause"))
        self.menuLayout.addWidget(QPushButton(QIcon(QPixmap('img\\next.png')), "Next"))

        # set menu buttons
        router_button = Button('Router', "img\\router.png")
        tablet_button = Button('Tablet', "img\Tablet.png")
        computer_button = Button('Computer', "img\Computer.png")
        edge_button = Button('Edge', "img\edge.png")

        self.menuLayout.addWidget(QLabel("Network Devices"))
        self.menuLayout.addWidget(router_button)
        self.menuLayout.addWidget(tablet_button)
        self.menuLayout.addWidget(computer_button)
        self.menuLayout.addWidget(edge_button)

        #self.menuLayout.addLayout(self.gridLayout)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Drag and Drop')
        self.setGeometry(0, 0, 50, 150)
        self.setLayout(self.menuLayout)

    def dragEnterEvent(self, e):
        e.setAccepted(True)
        self.dragOver = True
        print('Drag Enter Event')

    def mouseReleaseEvent(self, e):
        print(e.x())
        print(e.y())
        mouse_pos = [e.x(), e.y()]

    def dragMoveEvent(self, e):
        print('Drag')


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        self.setWindowTitle("Network Simulation Alpha")
        self.setLayout(QGridLayout())
        self.setMenuWidget(Example())

        self.vScene = QGraphicsScene()
        self.vGraphicsView = NetworkGraph()

        self.vGraphicsView.setScene(self.vScene)
        self.vGraphicsView.show()

        self.mdi.addSubWindow(self.vGraphicsView)
        self.mdi.tileSubWindows()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    addresses = address_db.AddressDictionary()
    ex = MainWindow()
    ex.show()
    app.exec_()
    addresses.drop_db()
