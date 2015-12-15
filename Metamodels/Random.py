from Metamodels.Metamodel import Metamodel
from Common.Module import Module
import random

class Random(Metamodel):
    def __init__(self):
        Metamodel.__init__(self)

    def add(self, system):
        pass

    def getTime(self, system):
        for m in system.modules:
            m.time = random.randint(1,1000)
        return True
