from Metamodels.Metamodel import Metamodel
try:
    from sklearn.linear_model import LinearRegression
except:
    print "Warning: Couldn't import scipy module."

class Polynomial(Metamodel):
    def __init__(self, conf):
        Metamodel.__init__(self)
        self.conf = conf
        self.interpolators = []
        for m in self.conf.modules:
            self.interpolators.append(LinearRegression())
        self.inputs = []
        self.outputs =[]

    def Clear(self):
        self.__init__(self.conf)

    def add(self, system):
        if not Metamodel.add(self, system):
            return

    def Update(self):
        self.inputs = [[] for m in self.conf.modules]
        self.outputs = [[] for m in self.conf.modules]
        for s in self.systems:
            for m in self.conf.modules:
                self.inputs[m.num].append(self.sys2array(s))
                self.outputs[m.num].append(s.modules[m.num].time)
        for m in self.conf.modules:
            self.interpolators[m.num].fit(self.inputs[m.num], self.outputs[m.num])

    def getTime(self, system):
        s = self.search(system)
        if s != None:
            for m in system.modules:
                m.time = s.modules[m.num].time
            return True
        input = self.sys2array(system)
        for m in system.modules:
            m.time = self.interpolators[m.num].predict(input)
        return True

