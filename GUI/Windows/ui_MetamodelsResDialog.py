
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

class Ui_MetamodelsResDialog(object):
    def setupUi(self, MetamodelsResDialog):
        MetamodelsResDialog.setObjectName(_fromUtf8("MetamodelsResDialog"))
        MetamodelsResDialog.resize(360, 85)
        self.gridLayout = QtGui.QGridLayout(MetamodelsResDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.random = QtGui.QRadioButton(MetamodelsResDialog)
        self.random.setObjectName(_fromUtf8("random"))
        self.verticalLayout.addWidget(self.random)
        self.radioButton_2 = QtGui.QRadioButton(MetamodelsResDialog)
        self.radioButton_2.setChecked(True)
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.verticalLayout.addWidget(self.radioButton_2)
        self.buttonBox = QtGui.QDialogButtonBox(MetamodelsResDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(MetamodelsResDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MetamodelsResDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MetamodelsResDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(MetamodelsResDialog)

    def retranslateUi(self, MetamodelsResDialog):
        MetamodelsResDialog.setWindowTitle(_translate("MetamodelsResDialog", "Dialog", None))
        self.random.setText(_translate("MetamodelsResDialog", "Random Solutions", None))
        self.radioButton_2.setText(_translate("MetamodelsResDialog", "Solutions in the neighbourhood of the best solution", None))

