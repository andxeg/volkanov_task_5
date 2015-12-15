
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MetamodelsRes(object):
    def setupUi(self, MetamodelsRes):
        MetamodelsRes.setObjectName(_fromUtf8("MetamodelsRes"))
        MetamodelsRes.resize(426, 320)
        self.gridLayout = QtGui.QGridLayout(MetamodelsRes)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.graphs = QtGui.QTabWidget(MetamodelsRes)
        self.graphs.setObjectName(_fromUtf8("graphs"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.layoutWidget = QtGui.QWidget(self.tab)
        self.layoutWidget.setGeometry(QtCore.QRect(11, 11, 391, 261))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.moduleNum = QtGui.QComboBox(self.layoutWidget)
        self.moduleNum.setObjectName(_fromUtf8("moduleNum"))
        self.horizontalLayout.addWidget(self.moduleNum)
        self.pushButton = QtGui.QPushButton(self.layoutWidget)
        self.pushButton.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/pics/pics/save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.graph = QtGui.QGraphicsView(self.layoutWidget)
        self.graph.setObjectName(_fromUtf8("graph"))
        self.verticalLayout.addWidget(self.graph)
        self.graphs.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.tab_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.table = QtGui.QTableWidget(self.tab_2)
        self.table.setObjectName(_fromUtf8("table"))
        self.table.setColumnCount(3)
        self.table.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(2, item)
        self.horizontalLayout_2.addWidget(self.table)
        self.graphs.addTab(self.tab_2, _fromUtf8(""))
        self.gridLayout.addWidget(self.graphs, 0, 0, 1, 1)

        self.retranslateUi(MetamodelsRes)
        self.graphs.setCurrentIndex(0)
        QtCore.QObject.connect(self.moduleNum, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), MetamodelsRes.Paint)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MetamodelsRes.Save)
        QtCore.QMetaObject.connectSlotsByName(MetamodelsRes)

    def retranslateUi(self, MetamodelsRes):
        MetamodelsRes.setWindowTitle(_translate("MetamodelsRes", "Dialog", None))
        self.label.setText(_translate("MetamodelsRes", "Module:", None))
        self.graphs.setTabText(self.graphs.indexOf(self.tab), _translate("MetamodelsRes", "Graphs", None))
        item = self.table.horizontalHeaderItem(0)
        item.setText(_translate("MetamodelsRes", "Simulation", None))
        item = self.table.horizontalHeaderItem(1)
        item.setText(_translate("MetamodelsRes", "Metamodel", None))
        item = self.table.horizontalHeaderItem(2)
        item.setText(_translate("MetamodelsRes", "Without penalty", None))
        self.graphs.setTabText(self.graphs.indexOf(self.tab_2), _translate("MetamodelsRes", "Sorting", None))

import resources_rc
