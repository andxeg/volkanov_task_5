from Common.Module import Module, NONE, NVP01, NVP11, RB11
import copy


class Metamodel:
    def __init__(self):
        self.systems = [] #known systems
        self.models = [] #metamodel for every model

    def add(self, system):
        if not system in self.systems:
            s = copy.deepcopy(system)
            self.systems.append(s)
            return True
        else:
            return False

    def search(self, system):
        for s in self.systems:
            if s == system:
                return s
        return None

    def Update(self):
        pass

    def mod2array(self, m):
        #res = [m.execTime]
        res = []
        if isinstance(m, NONE):
            res.append(m.execTime + Module.conf.modules[m.num].output)
        elif isinstance(m, NVP01):
            res.append(m.execTime + Module.conf.modules[m.num].output)
        elif isinstance(m, NVP11):
            res.append(2 * Module.conf.modules[m.num].input + m.execTime + 3 * Module.conf.modules[m.num].output)
        elif isinstance(m, RB11):
            res.append(Module.conf.modules[m.num].input + m.execTime + 2 * Module.conf.modules[m.num].output)
        else:
            print "Error"
            return None
        return res

    def sys2array(self, system):
        inp = []
        for m in system.modules:
            inp.extend(self.mod2array(m))
        return inp

    def Clear(self):
        pass