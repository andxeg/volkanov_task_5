from PyQt4.QtGui import QDialog
from GUI.Windows.ui_ConfigDialog import Ui_ConfigDialog

class ConfigDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_ConfigDialog()
        self.ui.setupUi(self)

    def GetResult(self):
        return {"modnum":self.ui.modnum.value(),
                "hwnum":self.ui.hwnum.value(), 
                "swnum":self.ui.swnum.value(),
                "minrel":self.ui.minrel.value(), 
                "maxrel":self.ui.maxrel.value(), 
                "mincost":self.ui.mincost.value(),
                "maxcost":self.ui.maxcost.value(),
                "mintime":self.ui.mintime.value(),
                "maxtime":self.ui.maxtime.value(),
                "minvol":self.ui.minvol.value(),
                "maxvol":self.ui.maxvol.value(),
                "qrv":self.ui.qrv.value(),
                "qd":self.ui.qd.value(),
                "qall":self.ui.qall.value(),
                "tvote":self.ui.tvote.value(),
                "ttest":self.ui.ttest.value(),
                "trecov":self.ui.trecov.value(),
                "none":self.ui.none.isChecked(),
                "nvp01":self.ui.nvp01.isChecked(),
                "nvp11":self.ui.nvp11.isChecked(),
                "rb11":self.ui.rb11.isChecked(),
                "linkprob":self.ui.linkprob.value()
                }
