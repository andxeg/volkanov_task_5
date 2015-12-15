from PyQt4.QtGui import QDialog, QColor, QGraphicsScene, QPen, QTableWidgetItem, QBrush, QImage, QPainter, QFileDialog, QFont
from PyQt4.QtCore import Qt
from GUI.Windows.ui_MetamodelsRes import Ui_MetamodelsRes
from Common.Module import NVP01, NONE, NVP11, RB11, Module
from Common.System import System
import copy, random

class SimpleSystem:
    def __init__(self, id, mmrel, simrel, rel):
        self.id = id
        self.mmrel = mmrel
        self.simrel = simrel
        self.rel = rel

class MetamodelsRes(QDialog):
    settings = {"axis": QColor(0, 0, 0),
                "mm": QColor(255, 0, 0),
                "sim": QColor(0, 255, 0),
                "num_points": 20}

    def __init__(self, best, randomSolutions=False):
        QDialog.__init__(self)
        self.ui = Ui_MetamodelsRes()
        self.ui.setupUi(self)
        self.points_mm = []
        self.points_sim = []
        self.best = best
        self.random = randomSolutions
        self.num = 0
        for m in Module.conf.modules:
            self.num += m.GetConfigsNum()
        self.num -= 3
        self.num = min(self.num, self.settings["num_points"])
        self.GetData()
        for i in range(Module.conf.modNum):
            self.ui.moduleNum.addItem(str(i))
        self.Paint()

    def GetData(self):
        self.points_mm = []
        self.points_sim = []
        self.systems = []
        self.simplesystems = []
        self.systems.append(self.best)
        for i in range(self.num):
            mm = []
            sim = []
            s = None
            if not self.random:
                while not s or any(s1 == s for s1 in self.systems):
                    s = copy.deepcopy(self.best)
                    j = random.randint(0, len(s.modules)-1)
                    type = random.choice(Module.conf.modules[j].tools)
                    if type == "none":
                        s.modules[j] = NONE(j)
                    elif type == "nvp01":
                        s.modules[j] = NVP01(j)
                    elif type == "nvp11":
                        s.modules[j] = NVP11(j)
                    else:
                        s.modules[j] = RB11(j)
            else:
                while not s or any(s1 == s for s1 in self.systems):
                    s = System()
                    s.modules = []
                    for j in range(Module.conf.modNum):
                        type = random.choice(Module.conf.modules[j].tools)
                        if type == "none":
                            s.modules.append(NONE(j))
                        elif type == "nvp01":
                            s.modules.append(NVP01(j))
                        elif type == "nvp11":
                            s.modules.append(NVP11(j))
                        else:
                            s.modules.append(RB11(j))
            self.systems.append(s)
            s.Update(use_metamodel=True, add=False)
            for m in s.modules:
                mm.append(m.time)
            mmrel = s.rel * s.penalty
            s.Update(use_metamodel=False, add=False)
            simrel = s.rel * s.penalty
            for m in s.modules:
                sim.append(m.time)
            self.points_mm.append(mm)
            self.points_sim.append(sim)
            self.simplesystems.append(SimpleSystem("System_"+str(i), mmrel, simrel, s.rel))


    def Paint(self):
        scene = QGraphicsScene()
        scene.setBackgroundBrush(Qt.transparent)
        scene.addLine(5, 5, 5, 213, QPen(self.settings["axis"]))
        scene.addLine(2, 210, 210, 210, QPen(self.settings["axis"]))
        mod_num = int(self.ui.moduleNum.currentText())
        max_sim = max(self.points_sim, key=lambda x: x[mod_num])[mod_num]
        max_mm = max(self.points_mm, key=lambda x: x[mod_num])[mod_num]
        max_time = max(max_mm, max_sim)

        for i in range(10):
            scene.addLine(4, 210 - (i + 1) * 20, 6, 210 - (i + 1) * 20, QPen(self.settings["axis"]))
            font = QFont()
            font.setPointSize(6)
            if int(0.1*max_time*(i + 1)) != 0:
                t2 = scene.addText(str(int(0.1*max_time*(i + 1))), font)
                t2.setPos(-18, 200 - (i + 1) * 20)

        i = 1
        x0 = 5 + 200 / self.num
        y0 = 210 - float(self.points_mm[0][mod_num]) / max_time * 200
        for p in self.points_mm:
            x = 5 + i * 200 / self.num
            y = 210 - float(p[mod_num])/max_time * 200
            scene.addLine(x0, y0, x, y, QPen(self.settings["mm"]))
            scene.addLine(x - 2, y - 2, x + 2, y + 2, QPen(self.settings["mm"]))
            scene.addLine(x + 2, y - 2, x - 2, y + 2, QPen(self.settings["mm"]))
            x0 = x
            y0 = y
            i += 1
        i = 1
        x0 = 5 + 200 / self.num
        y0 = 210 - float(self.points_sim[0][mod_num]) / max_time * 200
        for p in self.points_sim:
            x = 5 + i * 200 / self.num
            y = 210 - float(p[mod_num])/max_time * 200
            scene.addLine(x0, y0, x, y, QPen(self.settings["sim"]))
            scene.addLine(x - 2, y - 2, x + 2, y + 2, QPen(self.settings["sim"]))
            scene.addLine(x + 2, y - 2, x - 2, y + 2, QPen(self.settings["sim"]))
            x0 = x
            y0 = y
            i += 1
        self.ui.graph.setScene(scene)

        self.ui.table.setRowCount(len(self.simplesystems))
        self.simplesystems.sort(key = lambda x: x.simrel)
        for i in range(len(self.simplesystems)):
            self.ui.table.setItem(i, 0, QTableWidgetItem(self.simplesystems[i].id))
        self.simplesystems.sort(key = lambda x: x.mmrel)
        for i in range(len(self.simplesystems)):
            self.ui.table.setItem(i, 1, QTableWidgetItem(self.simplesystems[i].id))
            if self.ui.table.item(i, 0).text() != self.ui.table.item(i, 1).text():
                self.ui.table.item(i, 0).setForeground(QBrush(QColor(255,0,0)))
                self.ui.table.item(i, 1).setForeground(QBrush(QColor(255,0,0)))
            else:
                self.ui.table.item(i, 0).setForeground(QBrush(QColor(0,255,0)))
                self.ui.table.item(i, 1).setForeground(QBrush(QColor(0,255,0)))
        self.simplesystems.sort(key = lambda x: x.rel)
        for i in range(len(self.simplesystems)):
            self.ui.table.setItem(i, 2, QTableWidgetItem(self.simplesystems[i].id))

    def Replot(self, i):
        self.Paint()

    def Save(self):
        fileName = unicode(QFileDialog.getSaveFileName(directory="graph.png", filter="*.png"))
        if fileName == '':
            return
        scene = self.ui.graph.scene()
        scene.clearSelection()
        scene.setSceneRect(scene.itemsBoundingRect())
        scene.setBackgroundBrush(QBrush(QColor(255,255,255)))
        img = QImage(scene.sceneRect().size().toSize(), QImage.Format_ARGB32)
        img.fill(Qt.transparent)
        ptr = QPainter(img)
        self.ui.graph.scene().render(ptr)
        ptr.end()
        img.save(fileName)
        self.Paint()