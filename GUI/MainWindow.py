from PyQt4.QtGui import QMainWindow, QFileDialog, QDialog, QMessageBox, qApp
from PyQt4.QtCore import QTranslator
from GUI.Windows.ui_MainWindow import Ui_MainWindow
from GUI.ConfigDialog import ConfigDialog
from GUI.MetamodelsRes import MetamodelsRes
from GUI.Windows.ui_MetamodelsResDialog import Ui_MetamodelsResDialog
from Common.SysConfig import SysConfig
from GA.GAConfig import GAConfig
from Common.Constraints import CostConstraints, TimeConstraints
from Common.System import System
from Common.Module import Module
from Common.Algorithm import Algorithm
from Common.AlgConfig import AlgConfig
from GA.GA import GA
from GA.HGA import HGA
from Greedy.Greedy import Greedy

from ACODC.ACODC import ACODC
from ACODC.ACODCConfig import ACODCConfig

import xml.dom.minidom, time, os
try:
    from Metamodels.NeuralNetwork import NeuralNetwork
    from Metamodels.Averaging import Averaging
    from Metamodels.Polynomial import Polynomial
    from Metamodels.KNearestNeighbours import KNearestNeighbours
    from Metamodels.Svr import Svr
    from Metamodels.Random import Random
except:
    print "Warning: Couldn't import metamodels"


class MetamodelsResDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_MetamodelsResDialog()
        self.ui.setupUi(self)

    def Load(self, v):
        self.ui.id.setText(v.id)
        self.ui.speed.setText(str(v.speed))
        self.ui.ram.setText(str(v.ram))

    def SetResult(self, v):
        v.id = self.ui.id.text()
        v.speed = int(self.ui.speed.text())
        v.ram = int(self.ui.ram.text())

class MainWindow(QMainWindow):
    sysconfig = None
    algconfig = None
    sysconfigfile = None
    algconfigfile = None
    constraints = []

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.sysConfigFilter = self.tr("System Configuration files (*.xml)")
        self.algConfigFilter = self.tr("Algorithm Configuration files (*.xml)")
        self.ui.result_filename.setText("result"+str(time.time())+".csv")
        self.best = None
        translator = QTranslator(qApp)
        translator.load("GUI/Windows/Translations/relopt_ru.qm")
        qApp.installTranslator(translator)
        self.ui.retranslateUi(self)

    def LoadSysConf(self):
        if self.ui.sysconfname.text() == None or self.ui.sysconfname.text() == '':
            return
        self.sysconfig = SysConfig()
        self.sysconfig.loadXML(self.ui.sysconfname.text())
        self.constraints = []
        if self.sysconfig.limitcost != None:
            self.constraints.append(CostConstraints(self.sysconfig.limitcost))
        if self.ui.checktime_yes.isChecked():
            c = self.sysconfig.getLimitTimes()     
            if c != None:
                self.constraints.append(TimeConstraints(c))

    def LoadAlgConf(self):
        f = open(unicode(self.ui.algconfname.text()), "r")
        dom = xml.dom.minidom.parse(f)
        root = dom.childNodes[0]
        if self.ui.algorithm.currentIndex() == 0 or self.ui.algorithm.currentIndex() == 1:
            self.algconfig = GAConfig()
        #Create object with my algorithm parameter reader
        if self.ui.algorithm.currentIndex() == 4:
            self.algconfig = ACODCConfig()
        self.algconfig.LoadFromXmlNode(root)

    def Run(self):
        if self.sysconfig == None:
            QMessageBox.critical(self, "An error occurred", "System configuration must be defined")
            return
        Module.conf = self.sysconfig
        if self.constraints == None:
            QMessageBox.critical(self, "An error occurred", "Constraints must be defined")
            return
        System.constraints = self.constraints
        if self.algconfig == None and self.ui.algorithm.currentIndex() < 2 :
            QMessageBox.critical(self, "An error occurred", "Algorithm configuration must be defined")
            return
        Algorithm.algconf = self.algconfig
        if Algorithm.algconf == None:
            Algorithm.algconf = AlgConfig()
        if self.ui.use_metamodels.isChecked():
            Algorithm.algconf.use_metamodel = True
            modelidx = self.ui.metamodel.currentIndex()
            if modelidx == 0:
                Algorithm.algconf.metamodel = Averaging()
            elif modelidx == 1:
                Algorithm.algconf.metamodel = KNearestNeighbours(10) #TODO user should define this number
            elif modelidx == 2:
                Algorithm.algconf.metamodel = NeuralNetwork(self.sysconfig) #TODO add settings
            elif modelidx == 3:
                Algorithm.algconf.metamodel = Svr(self.sysconfig)
            elif modelidx == 4:
                Algorithm.algconf.metamodel = Polynomial(self.sysconfig)
            elif modelidx == 5:
                Algorithm.algconf.metamodel = Random()
            Algorithm.algconf.pop_control_percent = float(self.ui.popControl.value())/100.0

        algidx = self.ui.algorithm.currentIndex()
        if algidx==0:
            algorithm = GA()
        elif algidx==1:
            algorithm = HGA()
        elif algidx==2:
            algorithm = Greedy()
        elif algidx==4:
            algorithm = ACODC()
        Algorithm.result_filename = self.ui.result_filename.text()
        for i in range(self.ui.execNum.value()):
            if algorithm.algconf.metamodel:
                algorithm.algconf.metamodel.Clear()
            algorithm.Run()
            algorithm.PrintStats()
            self.best = algorithm.currentSolution
        try:
            os.remove("sch" + str(os.getpid()) + ".xml")
            os.remove("res" + str(os.getpid()) + ".xml")
        except:
            pass

    def OpenSysConf(self):
        name = unicode(QFileDialog.getOpenFileName(filter=self.sysConfigFilter))
        if name == None or name == '':
            return
        self.sysconfigfile = name
        self.ui.sysconfname.setText(name)
        self.LoadSysConf()
        costrange = self.sysconfig.costInterval()
        timerange = self.sysconfig.timeInterval()
        self.ui.maxcost.setText(str(costrange[1]))
        self.ui.mincost.setText(str(costrange[0]))
        self.ui.maxtime.setText(str(timerange[1]).replace("]","").replace("[",""))
        self.ui.mintime.setText(str(timerange[0]).replace("]","").replace("[",""))
        self.ui.limitcost.setText(str(self.sysconfig.limitcost) if self.sysconfig.limitcost != None else "")
        l = []
        for constr in self.constraints:
            if isinstance(constr,TimeConstraints):
                l = constr.limitTimes
        if l == []:
            self.ui.limittimes.setText("")
        else:
            self.ui.limittimes.setText(str(l).replace("]","").replace("[",""))

    def OpenAlgConf(self):
        name = unicode(QFileDialog.getOpenFileName(filter=self.algConfigFilter))
        if name == None or name == '':
            return
        self.algconfigfile = name
        self.ui.algconfname.setText(name)
        self.LoadAlgConf()

    def Random(self):
        d = ConfigDialog()
        d.exec_()
        if d.result() == QDialog.Accepted: 
            dict = d.GetResult()
        else:
            return
        self.sysconfig = SysConfig()
        self.sysconfig.generateRandom(dict)
        costrange = self.sysconfig.costInterval()
        timerange = self.sysconfig.timeInterval()
        self.ui.maxcost.setText(str(costrange[1]))
        self.ui.mincost.setText(str(costrange[0]))
        self.ui.maxtime.setText(str(timerange[1]).replace("]","").replace("[",""))
        self.ui.mintime.setText(str(timerange[0]).replace("]","").replace("[",""))
        self.ui.limitcost.setText("")
        self.ui.limittimes.setText("")
        self.ui.sysconfname.setText("")
        self.constraints = []

    def InputTimeLimits(self):
        if self.ui.limittimes.text() == "":
            return
        for constr in self.constraints:
            if isinstance(constr,TimeConstraints):
                self.constraints.remove(constr)
                break
        l = []
        for c in self.ui.limittimes.text().split(","):
            l.append(int(c))
        self.constraints.append(TimeConstraints(l))
        for m,t in zip(self.sysconfig.modules, l):
            m.limittime = t

    def InputCostLimit(self):
        if self.ui.limitcost.text() == "":
            return
        for constr in self.constraints:
            if isinstance(constr,CostConstraints):
                self.constraints.remove(constr)
                break
        c = int(self.ui.limitcost.text())
        self.constraints.append(CostConstraints(c))
        self.sysconfig.limitcost = c

    def SaveSysConf(self):
        name = unicode(QFileDialog.getSaveFileName(filter=self.sysConfigFilter))
        if name == None or name == '':
            return
        self.sysconfig.saveXML(name)

    def no_checked(self):
        if self.ui.checktime_yes.isChecked():
            return
        for constr in self.constraints:
            if isinstance(constr,TimeConstraints):
                self.constraints.remove(constr)
                break
        self.ui.limittimes.setText("")
        self.ui.limittimes.setEnabled(False)

    def yes_checked(self):
        if not self.ui.checktime_yes.isChecked():
            return
        self.ui.limittimes.setEnabled(True)
        if self.sysconfig == None:
            return
        c = self.sysconfig.getLimitTimes()     
        if c != None:
            self.constraints.append(TimeConstraints(c))
            self.ui.limittimes.setText(str(c).replace("]","").replace("[",""))

    def use_metamodels_checked(self):
        if not self.ui.use_metamodels.isChecked():
            self.ui.metamodel.setEnabled(False)
            self.ui.popControl.setEnabled(False)
        else:
            self.ui.metamodel.setEnabled(True)
            self.ui.popControl.setEnabled(True)

    def ShowMetamodelRes(self):
        d = MetamodelsResDialog()
        d.exec_()
        if not d.result():
            return
        if d.ui.random.isChecked():
            d1 = MetamodelsRes(self.best, True)
        else:
            d1 = MetamodelsRes(self.best, False)
        d1.exec_()
        try:
            os.remove("sch" + str(os.getpid()) + ".xml")
            os.remove("res" + str(os.getpid()) + ".xml")
        except:
            pass



