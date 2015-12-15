from Common.Algorithm import Algorithm
from Common.Module import Module

from Common.System import System
from Common.Core import genEvent
from Common.Module import NONE, NVP01, NVP11, RB11, Module
from Common.Statistics import Execution
import random, copy, time, math
from math import *


class SubSystem:
    def __init__(self, moduleConfig):
        self.pmax = Algorithm.algconf.pmax
        self.elements = copy.deepcopy(moduleConfig.sw)

    def printSubSystem(self):
        for element in self.elements:
            print "[SW] (num %f) (cost %f) (rel %f) (weight %f)\n", \
                         element.num, element.cost, element.rel, element.weight


class ACODC(Algorithm):
    def __init__(self):
        Algorithm.__init__(self)
        self.system = []
        for module in Module.conf.modules:
            self.system.append(SubSystem(module))





    def Step(self):
        pass

    def Run(self):
        Algorithm.timecounts = 0
        Algorithm.simcounts = 0
        Algorithm.time = time.time()

        #Check all system scheme read correctly
        #system = Module.conf
        # print "Amount of the modules %d\n", system.modNum
        # print "Limitcost %d\n", system.limitcost
        # print "Limitweight %d\n", system.limitweight
        # for module in system.modules:
        #         print "Module number-> %d\n", module.num
        #         for version in module.sw:
        #             print "[SW] (num %f) (cost %f) (rel %f) (weight %f)\n", \
        #                 version.num, version.cost, version.rel, version.weight
        #         print "\n"



    def Clear(self):
        Algorithm.Clear(self)
        #reset local variable


