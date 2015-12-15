from Metamodels.Metamodel import Metamodel
from Common.Module import Module

class KNearestNeighbours(Metamodel):
    def __init__(self,k):
        Metamodel.__init__(self)
        self.k = k

    def add(self, system):
        Metamodel.add(self, system)

    def Clear(self):
        self.__init__(self.k)

    def getTime(self, system):
        s = self.search(system)
        if s != None:
            for m in system.modules:
                m.time = s.modules[m.num].time
            return True
        dist = 1
        res = []
        while dist <= 1.0 * len(system.modules):
            for s in self.systems:
                if s.distance(system)==dist:
                    res.append(s)
            if len(res) >= self.k:
                break
            else:
                dist += 1
        if len(res) < self.k:
            return False
        s1 = [0.0 for i in range(Module.conf.modNum)]
        s2 = [0.0 for i in range(Module.conf.modNum)]
        for i in range(self.k):
            for m in system.modules:
                d = res[i].distance(system)
                w = 1.0/(d**2)
                s1[m.num] += (w*res[i].modules[m.num].time)
                s2[m.num] += w
        for m in system.modules:
            m.time = s1[m.num]/s2[m.num]
        return True
