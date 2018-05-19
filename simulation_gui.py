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
        print("New Item! ID: "+str(id(self))+" Address: " + address)

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton and self.isSelected():
            print("Right mouse pressed")
            self.setFlag(QGraphicsItem.ItemIsMovable, True)
            print("selected")
            for item in ex.vScene.items():
                if self.collidesWithItem(item) and self != item:
                    self.setFlag(QGraphicsItem.ItemIsMovable, False)
                    print("COLLISION!")
                    return
            ex.vScene.removeItem(self)
            addresses.remove_name(str(id(self)))

    def mouseDoubleClickEvent(self, *args, **kwargs):
        self.printNeighboursList()

    def printNeighboursList(self):
        addresses.print_node_neighbours(str(id(self)))


class MapEdge(QGraphicsPixmapItem):
    def __init__(self):
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
        #elif e.button() == Qt.LeftButton and self.isSelected():
        #    self.checkConnections()

    def mouseDoubleClickEvent(self, *args, **kwargs):
        self.rotate += 30
        self.setRotation(self.rotate)

    def mouseReleaseEvent(self, *args, **kwargs):
        self.checkConnections()

    def checkConnections(self):
        self.setPixmap(QPixmap('img\\edge.png'))
        #self.setFlag(QGraphicsItem.ItemIsMovable, True)

        # remove current neighbour nodes
        if len(self.neighbours) > 1:
            addresses.remove_edge(self.neighbours[0], self.neighbours[1])

        self.neighbours = []
        for item in ex.vScene.items():
            if self.collidesWithItem(item) and self != item:
                # add neighbour to list
                #address = addresses.value_by_name(str(id(item)))
                self.neighbours.append(str(id(item)))

        print(len(self.neighbours))
        if len(self.neighbours) > 1:
            # add neighbours to dictionary
            addresses.add_node_neighbour(self.neighbours[0], self.neighbours[1])
            #self.setFlag(QGraphicsItem.ItemIsMovable, False)
            self.setPixmap(QPixmap('img\\edgeConnected.png'))
            print("Edge Connected !")
        else:
            print("Edge Disconnected !")


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
                new_item = MapEdge()
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

        deleteButton = QPushButton()
        deleteButton.setIcon(QIcon("img\\delete.png"))
        deleteButton.setFixedSize(35, 35)

        self.menuLayout.addWidget(deleteButton)

       # self.menuLayout.addWidget(QPushButton(QIcon(QPixmap("img\\play.png")), "Play"))
       # self.menuLayout.addWidget(QPushButton(QIcon(QPixmap("img\\stop.png")), "Stop"))
       # self.menuLayout.addWidget(QPushButton(QIcon(QPixmap("img\\pause.png")), "Pause"))
       # self.menuLayout.addWidget(QPushButton(QIcon(QPixmap('img\\next.png')), "Next"))

        # set menu buttons
        router_button = Button('Router', "img\\router.png")
        tablet_button = Button('Tablet', "img\\Tablet.png")
        phone_button = Button('Phone', "img\\")
        computer_button = Button('Computer', "img\\Computer.png")
        edge_button = Button('Edge', "img\\edge.png")

        self.menuLayout.addWidget(QLabel("Network Devices"))
        self.menuLayout.addWidget(router_button)
        self.menuLayout.addWidget(tablet_button)
        self.menuLayout.addWidget(computer_button)
        self.menuLayout.addWidget(edge_button)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Drag and Drop')
        self.setGeometry(0, 0, 50, 150)
        self.setLayout(self.menuLayout)

    def dragEnterEvent(self, e):
        e.setAccepted(True)
        self.dragOver = True
        print('Drag Enter Event')

    #def mouseReleaseEvent(self, e):
    #    print(e.x())
    #    print(e.y())
    #    mouse_pos = [e.x(), e.y()]

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
