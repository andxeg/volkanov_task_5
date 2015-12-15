from Metamodels.Metamodel import Metamodel
from Common.Module import Module

class Averaging(Metamodel):
    def __init__(self):
        Metamodel.__init__(self)

    def add(self, system):
        Metamodel.add(self, system)

    def Clear(self):
        self.__init__()

    def getTime(self, system):
        s = self.search(system)
        if s != None:
            for m in system.modules:
                m.time = s.modules[m.num].time
            return True
        dist = 1
        res = []
        while dist <= Module.conf.modNum:
            for s in self.systems:
                if s.distance(system)==dist:
                    res.append(s)
            if res != []:
                break
            else:
                dist += 1
        if res == []:
            return False
        time = [0 for i in range(Module.conf.modNum)]
        for s in res:
            for m in system.modules:
                time[m.num] += s.modules[m.num].time
        k = len(res)
        for m in system.modules:
            m.time = time[m.num]/k
        return True

