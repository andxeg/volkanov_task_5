from Metamodels.Metamodel import  Metamodel
try:
    from sklearn.svm import SVR
except:
    print "Warning: couldn't import SVR"


class Svr(Metamodel):
    def __init__(self, conf):
        Metamodel.__init__(self)
        self.conf = conf
        self.svrs = []
        self.inputs = []
        self.outputs = []
        for m in conf.modules:
            #self.svrs.append(SVR(kernel='rbf', C=1e3, gamma=0.1))
            self.svrs.append(SVR(kernel='linear', C=1.0))
            self.inputs.append([])
            self.outputs.append([])

    def Clear(self):
        self.__init__(self.conf)

    def add(self, system):
        if not Metamodel.add(self, system):
            return
        for m in system.modules:
            self.inputs[m.num].append(self.sys2array(system))
            self.outputs[m.num].append(m.time)

    def Update(self):
        for m in self.conf.modules:
            if len(self.outputs[m.num])>=4:
                self.svrs[m.num].fit(self.inputs[m.num], self.outputs[m.num])

    def getTime(self, system):
        s = self.search(system)
        if s != None:
            for m in system.modules:
                m.time = s.modules[m.num].time
            return True
        for m in system.modules:
            if len(self.outputs[m.num]) >= 4:
                m.time = int(self.svrs[m.num].predict(self.sys2array(system)))
            else:
                return False
        return True