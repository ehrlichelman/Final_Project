import sys
import address_db
import node_process, log_analyzer
import shlex, subprocess
import os
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

ICON_SIZE = 40


# send message between nodes
def start_send():
    # that source and destination are selected differently
    if ex.src != -1 and ex.dst != -1 and ex.src != ex.dst:
        src = ex.src
        dst = ex.dst
        data = ex.dataText.text()

        if ex.add_delay:
            data += 'ADD_DELAY'

        print(ex.selected_item)
        print('start send button works!')
        node_list = addresses.print_all_nodes()
        # create process for every node and set neighbours
        for node in node_list:
            send_rcv_msg.new_node_process(node, addresses.node_neighbours_list(node))

        time.sleep(3)
        # start sending message through nodes
        send_rcv_msg.send_msg(src, dst, data)

        ex.statusBar().showMessage("Sending message to destination...", 6000)
        if ex.add_delay:
            time.sleep(9)
        time.sleep(3)
        # destroy all node processes
        send_rcv_msg.kill_all_nodes()

# add network congestion
def addDelay():
    if ex.delayCheckBox.isChecked():
        ex.add_delay = True
    else:
        ex.add_delay = False

# display performance logger
def showPerformanceLog():
    network_log = log_analyzer.LogAnalyzer()

# remove node from network
def selectItemToDelete():
    for item in ex.vScene.items():
        if ex.selected_item == str(id(item)):
            addresses.remove_name(str(id(item)))
            ex.vScene.removeItem(item)
            ex.statusBar().showMessage("ID: " + str(id(item)) + " was removed", 2000)

# select source node
def selectSourceNode():
    print("selecting source node")
    for item in ex.vScene.items():
        if ex.selected_item == str(id(item)):
            ex.src = str(id(item))
            #ex.statusBar().showMessage("Source ID: " + str(id(item)))
            ex.statusBar().clearMessage()
            ex.statusBar().removeWidget(ex.sourceLabel)
            ex.sourceLabel = QLabel("Source ID: " + str(id(item)))
            ex.statusBar().addWidget(ex.sourceLabel)
            return

# select destination node
def selectDestinationNode():
    print("selecting destination node")
    for item in ex.vScene.items():
        if ex.selected_item == str(id(item)):
            ex.dst = str(id(item))

            ex.statusBar().clearMessage()
            ex.statusBar().removeWidget(ex.sourceLabel)
            ex.sourceLabel = QLabel("Source ID: " + str(ex.src))
            ex.statusBar().addWidget(ex.sourceLabel)

            ex.statusBar().removeWidget(ex.destinationLabel)
            ex.destinationLabel = QLabel("Destination ID: " + str(id(item)))
            ex.statusBar().addWidget(ex.destinationLabel)

            ex.statusBar().removeWidget(ex.dataLabel)
            ex.statusBar().removeWidget(ex.dataText)
            ex.statusBar().removeWidget(ex.delayCheckBox)

            ex.dataLabel = QLabel("Data: ")
            ex.dataText = QLineEdit()
            ex.dataText.resize(150, 40)

            ex.delayCheckBox = QCheckBox('Network Congestion')
            ex.delayCheckBox.stateChanged.connect(addDelay)

            ex.statusBar().addWidget(ex.dataLabel)
            ex.statusBar().addWidget(ex.dataText)
            ex.statusBar().addWidget(ex.delayCheckBox)

            return

"""Network map graphical node, represents devices and access points"""
class MapIcon(QGraphicsPixmapItem):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.img = pixmap
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.isConnected = False
        addresses.add_name_addr(str(id(self)))
        address = addresses.value_by_name(str(id(self)))
        ex.statusBar().showMessage("Click and drag the item on the screen",2000)

    def mousePressEvent(self, e):
        ex.statusBar().clearMessage()
        if e.button() == Qt.LeftButton:
            ex.selected_item = str(id(self))
            self.printNeighboursList()

    def mouseDoubleClickEvent(self, *args, **kwargs):
        self.printNeighboursList()

    def printNeighboursList(self):
        ex.statusBar().showMessage(addresses.print_node_neighbours(str(id(self))))

class MapEdge(QGraphicsPixmapItem):
    def __init__(self):
        super().__init__(QPixmap('img//edge.png'))
        self.rotate = 0
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.neighbours = []
        print("added new edge to map")
        ex.statusBar().showMessage("Place the edge between two network devices",2000)

    def mousePressEvent(self, e):
        ex.statusBar().clearMessage()
        ex.statusBar().showMessage("Double click to rotate the edge")
        self.checkConnections()
        if e.button() == Qt.RightButton and self.isSelected():
            print("Right mouse pressed")
            if len(self.neighbours) > 1:
                addresses.remove_edge(self.neighbours[0], self.neighbours[1])
            ex.vScene.removeItem(self)

    def mouseDoubleClickEvent(self, *args, **kwargs):
        self.rotate += 30
        self.setRotation(self.rotate)

    def checkConnections(self):
        # remove current neighbour nodes
        if len(self.neighbours) > 1:
            addresses.remove_edge(self.neighbours[0], self.neighbours[1])

        self.neighbours = []
        for item in ex.vScene.items():
            if self.collidesWithItem(item) and self != item:
                # add neighbour to list
                self.neighbours.append(str(id(item)))

        print(len(self.neighbours))
        if len(self.neighbours) > 1:
            # add neighbours to dictionary
            addresses.add_node_neighbour(self.neighbours[0], self.neighbours[1])
            self.setPixmap(QPixmap('img//edgeConnected.png'))
            print("Edge Connected !")
            ex.statusBar().showMessage("Connected "+self.neighbours[0]+" and "+self.neighbours[1],2000)
        else:
            self.setPixmap(QPixmap('img//edge.png'))
            print("Edge Disconnected !")


class Button(QPushButton):
    def __init__(self, title, icon):
        super().__init__()
        self.name = title
        self.setIcon(QIcon(QPixmap(icon)))
        self.iconFile = icon
        self.setFixedSize(ICON_SIZE, ICON_SIZE)

    def mouseMoveEvent(self, e):
        mimeData = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        if e.button() == Qt.LeftButton:
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
        deleteButton.setIcon(QIcon("img//delete.png"))
        deleteButton.setFixedSize(ICON_SIZE, ICON_SIZE)
        deleteButton.clicked.connect(selectItemToDelete)
        self.menuLayout.addWidget(deleteButton)

        sendButton = QPushButton()
        sendButton.setIcon(QIcon("img//play.png"))
        sendButton.setFixedSize(ICON_SIZE, ICON_SIZE)
        sendButton.clicked.connect(start_send)
        self.menuLayout.addWidget(sendButton)

        selectSrcButton = QPushButton()
        selectSrcButton.setIcon(QIcon("img//start.png"))
        selectSrcButton.setFixedSize(ICON_SIZE, ICON_SIZE)
        selectSrcButton.clicked.connect(selectSourceNode)
        self.menuLayout.addWidget(selectSrcButton)

        selectDestButton = QPushButton()
        selectDestButton.setIcon(QIcon("img//end.png"))
        selectDestButton.setFixedSize(ICON_SIZE, ICON_SIZE)
        selectDestButton.clicked.connect(selectDestinationNode)
        self.menuLayout.addWidget(selectDestButton)

        showLogButton = QPushButton()
        showLogButton.setIcon(QIcon("img//log.png"))
        showLogButton.setFixedSize(ICON_SIZE, ICON_SIZE)
        showLogButton.clicked.connect(showPerformanceLog)
        self.menuLayout.addWidget(showLogButton)

        # set menu buttons
        router_button = Button('Router', "img//router.png")
        tablet_button = Button('Tablet', "img//tablet.png")
        phone_button = Button('Phone', "img//phone.png")
        computer_button = Button('Computer', "img//computer.png")
        edge_button = Button('Edge', "img//edge.png")

        self.menuLayout.addWidget(QLabel("Network Devices"))
        self.menuLayout.addWidget(edge_button)
        self.menuLayout.addWidget(router_button)
        self.menuLayout.addWidget(tablet_button)
        self.menuLayout.addWidget(phone_button)
        self.menuLayout.addWidget(computer_button)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Drag and Drop')
        self.setGeometry(0, 0, 50, 150)
        self.setLayout(self.menuLayout)

    def dragEnterEvent(self, e):
        e.setAccepted(True)
        self.dragOver = True
        print('Drag Enter Event')


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        self.setWindowTitle("Network Simulation Alpha")
        self.setLayout(QGridLayout())
        self.setMenuWidget(Example())

        self.selected_item = -1
        self.src = -1
        self.dst = -1
        self.data = 'FFF'
        self.add_delay = False

        self.sourceLabel = QLabel("Source: ")
        self.destinationLabel = QLabel("Destination: ")
        self.dataLabel = QLabel("Data: ")

        self.dataText = QLineEdit()
        self.dataText.resize(150, 40)

        self.delayCheckBox = QCheckBox('Network Congestion')
        self.delayCheckBox.stateChanged.connect(addDelay)

        self.vScene = QGraphicsScene()
        self.vGraphicsView = NetworkGraph()

        self.vGraphicsView.setScene(self.vScene)
        self.vGraphicsView.show()

        self.mdi.addSubWindow(self.vGraphicsView)
        self.mdi.tileSubWindows()

        status_bar = QStatusBar()
        status_bar.clearMessage()

        self.setStatusBar(status_bar)

        self.statusBar().showMessage("Add a network device by clicking on one of the buttons right to Network Devices", 2000)
        self.statusBar().addWidget(self.dataLabel)
        self.statusBar().addWidget(self.dataText)
        self.statusBar().addWidget(self.delayCheckBox)


        self.setAnimated(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    addresses = address_db.AddressDictionary()
    send_rcv_msg = node_process.NodeProcess()
    ex = MainWindow()
    ex.show()
    app.exec_()
    send_rcv_msg.kill_all_nodes()
