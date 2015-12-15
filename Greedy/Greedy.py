__author__ = 'A'
from Common.Algorithm import Algorithm
from Common.System import System
from Common.Core import genEvent
from Common.Module import NONE, NVP01, NVP11, RB11, Module
from Common.Statistics import Execution
import random, copy

class Greedy(Algorithm):
    def __init__(self):
        Algorithm.__init__(self)
        self.bankConf = []
        self.system = System()
        self.curconf = []
        self.numOper = 0
        self.finished = []

    def Prep(self):


        for i in range(len(Module.conf.modules)):
            tmpbank = []


            if "none" in Module.conf.modules[i].tools:
                sw = [-1, -1, -1]
                hw = [-1, -1, -1]

                for q in range(len(Module.conf.modules[i].hw)):

                    hw[2] = Module.conf.modules[i].hw[q].num

                    for j in range(len(Module.conf.modules[i].sw)):

                        sw[2] = Module.conf.modules[i].sw[j].num

                        if hw[0] == -1 and hw[1] == -1 and sw[0] == -1 and sw[1] == -1:

                            hw1 = []
                            sw1 = []
                            hw1.append(hw[2])
                            sw1.append(sw[2])
                            tmp = NONE(i, hw1, sw1)
                            tmpbank.append(tmp)


            if "nvp01" in Module.conf.modules[i].tools:
                j1 = 0
                j2 = 0
                j3 = 0
                sw = [-1, -1, -1]
                hw = [-1, -1, -1]
                for i3 in range(len(Module.conf.modules[i].hw)):

                    hw[2] = Module.conf.modules[i].hw[i3].num
                    for j1 in range(len(Module.conf.modules[i].sw)):

                        sw[0] = Module.conf.modules[i].sw[j1].num
                        for j2 in range(len(Module.conf.modules[i].sw)):



                            if j2!= j1:

                                sw[1] = Module.conf.modules[i].sw[j2].num
                                for j3 in range(len(Module.conf.modules[i].sw)):

                                    if j3 != j2 and j3 != j1:

                                        sw[2] = Module.conf.modules[i].sw[j3].num
                                        hw1 = []
                                        hw1.append(hw[2])
                                        sw1 = []
                                        sw1.append(sw[0])
                                        sw1.append(sw[1])
                                        sw1.append(sw[2])

                                        tmp = NVP01(i, hw1, sw1)


                                        tmpbank.append(tmp)


            if "nvp11" in Module.conf.modules[i].tools:
                j1 =0
                j2 = 0
                j3 = 0
                sw = [-1, -1, -1]
                hw = [-1, -1, -1]

                for i1 in range(len(Module.conf.modules[i].hw)):
                    hw[0] = Module.conf.modules[i].hw[i1].num
                    for i2 in range(len(Module.conf.modules[i].hw)):
                        hw[1] = Module.conf.modules[i].hw[i2].num
                        for i3 in range(len(Module.conf.modules[i].hw)):
                            hw[2] = Module.conf.modules[i].hw[i3].num
                            for j1 in range(len(Module.conf.modules[i].sw)):
                                sw[0] = Module.conf.modules[i].sw[j1].num
                                for j2 in range(len(Module.conf.modules[i].sw)):
                                    if j2!= j1:
                                        sw[1] = Module.conf.modules[i].sw[j2].num
                                        for j3 in range(len(Module.conf.modules[i].sw)):
                                            if j3 != j2 and j3 != j1:
                                                sw[2] = Module.conf.modules[i].sw[j3].num
                                                sw1 = []
                                                hw1 = []
                                                sw1.append(sw[0])
                                                sw1.append(sw[1])
                                                sw1.append(sw[2])
                                                hw1.append(hw[0])
                                                hw1.append(hw[1])
                                                hw1.append(hw[2])

                                                tmp = NVP11(i, hw1, sw1)


                                                tmpbank.append(tmp)



            if "rb11" in Module.conf.modules[i].tools:
                    j1 = 0
                    j2 = 0
                    j3 = 0
                    sw = [-1, -1, -1]
                    hw = [-1, -1, -1]

                    for i2 in range(len(Module.conf.modules[i].hw)):
                        hw[1] = Module.conf.modules[i].hw[i2].num
                        for i3 in range(len(Module.conf.modules[i].hw)):
                            hw[2] = Module.conf.modules[i].hw[i3].num
                            for j2 in range(len(Module.conf.modules[i].sw)):
                                sw[1] = Module.conf.modules[i].sw[j2].num
                                for j3 in range(len(Module.conf.modules[i].sw)):
                                    if j3 != j2:
                                        sw[2] = Module.conf.modules[i].sw[j3].num

                                        hw1 = []
                                        sw1 = []
                                        hw1.append(hw[1])
                                        hw1.append(hw[2])
                                        sw1.append(sw[1])
                                        sw1.append(sw[2])
                                        tmp = RB11(i, hw1, sw1)
                                        tmpbank.append(tmp)




            tmpbank.sort(key = lambda x: x.rel, reverse = True)



            self.bankConf.append(tmpbank)
            self.curconf.append(0)


    def Step(self):
        max = 0

        for i in range(len(self.system.modules)):

            if self.system.modules[i].cost > self.system.modules[max].cost and not i in self.finished:
                max = i

        j = self.curconf[max]

        while self.system.modules[max].cost <= self.bankConf[max][j].cost:
            if  j != (len(self.bankConf[max])) - 1:
                j = j+1
            else:
                j = len(self.bankConf[max]) - 1
                self.finished.append(max)
                break

        if self.bankConf[max][j].cost <= self.system.modules[max].cost:
            self.system.modules[max] = self.bankConf[max][j]
            self.curconf[max] = j
            self.system.Update()


    def Run(self):
        self.Prep()

        for i in range(len(self.bankConf)):

            self.system.modules.append(self.bankConf[i][0])
        self.system.Update()

        while not self._checkStopCondition():
            self.Step()

            self.numOper = self.numOper + 1
            print self.numOper, self.system

        print "Best solution: ", self.system.cost, self.system

        print "--------------------------------------\n"
        self.Clear()

    def Clear(self):
        Algorithm.Clear(self)

    def _checkStopCondition(self):
        return True if (self.system != None and self.system.CheckConstraints()) or self.numOper > 200 else False