import sys, xml.dom.minidom
from GUI.MainWindow import MainWindow
from PyQt4 import QtGui

from Common.SysConfig import SysConfig
from GA.GAConfig import GAConfig
from Common.Constraints import CostConstraints, TimeConstraints
from Common.System import System
from Common.Module import Module
from Common.Algorithm import Algorithm
from Common.AlgConfig import AlgConfig
from GA.HGA import HGA

try:
    from Metamodels.NeuralNetwork import NeuralNetwork
    from Metamodels.Averaging import Averaging
    from Metamodels.Polynomial import Polynomial
    from Metamodels.KNearestNeighbours import KNearestNeighbours
    from Metamodels.Svr import Svr
    from Metamodels.Random import Random
except:
    print "Warning: Couldn't import metamodels"

def Console(argv):
    print "Warning: Do not use command-line interface!"
    _algconf = argv[1]
    _sysconf = argv[2]
    _num = argv[3]
    _metamodel = argv[4]
    _percent = argv[5]

    f = open(_algconf, "r")
    dom = xml.dom.minidom.parse(f)
    root = dom.childNodes[0]
    Algorithm.algconf = GAConfig()
    Algorithm.algconf.LoadFromXmlNode(root)
    f.close()

    Module.conf = SysConfig()
    Module.conf.loadXML(_sysconf)
    System.constraints = []
    if Module.conf.limitcost != None:
        System.constraints.append(CostConstraints(Module.conf.limitcost))
    c = Module.conf.getLimitTimes()
    if c != None:
        System.constraints.append(TimeConstraints(c))

    result = _sysconf.replace(".xml", "")

    result += "_"+_metamodel
    Algorithm.algconf.use_metamodel = True
    if _metamodel=="none":
        Algorithm.algconf.use_metamodel = False
    elif _metamodel=="kn":
        Algorithm.algconf.metamodel = KNearestNeighbours(10)
    elif _metamodel=="lr":
        Algorithm.algconf.metamodel = Polynomial(Module.conf)
    elif _metamodel=="rnd":
        Algorithm.algconf.metamodel = Random()
    elif _metamodel=="avg":
        Algorithm.algconf.metamodel = Averaging()

    Algorithm.algconf.pop_control_percent = float(_percent)/100.0

    algorithm = HGA()
    Algorithm.result_filename  = result + "_" +_percent + ".csv"

    for i in range(int(_num)):
        if algorithm.algconf.metamodel:
            algorithm.algconf.metamodel.Clear()
        algorithm.Run()
        algorithm.PrintStats()
    try:
        os.remove("sch" + str(os.getpid()) + ".xml")
        os.remove("res" + str(os.getpid()) + ".xml")
    except:
        pass



if __name__ == "__main__":
    if len(sys.argv) > 1:
        Console(sys.argv)
    else:
        app = QtGui.QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
