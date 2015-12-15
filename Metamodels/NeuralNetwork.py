from Metamodels.Metamodel import  Metamodel
try:
    from pybrain.tools.shortcuts import buildNetwork
    from pybrain.datasets import SupervisedDataSet
    from pybrain.supervised.trainers import BackpropTrainer, RPropMinusTrainer
    from pybrain.structure import LinearLayer
except:
    print "Warning: couldn't import pybrain"


class NeuralNetwork(Metamodel):
    def __init__(self, conf):
        Metamodel.__init__(self)
        self.conf = conf
        self.ds = []
        self.nets = []
        self.trainers = []
        for m in conf.modules:
            input = conf.modNum
            output = 1
            self.ds.append(SupervisedDataSet(input, output))
            self.nets.append(buildNetwork(input, 1, output, hiddenclass=LinearLayer, outclass=LinearLayer))
            self.trainers.append(RPropMinusTrainer(self.nets[len(self.nets)-1]))

    def Clear(self):
        self.__init__(self.conf)

    def add(self, system):
        if not Metamodel.add(self, system):
            return
        for m in system.modules:
            self.ds[m.num].addSample(self.sys2array(system), m.time)

    def Update(self):
        for m in self.conf.modules:
            if len(self.ds[m.num]) >= 4:
                self.trainers[m.num].setData(self.ds[m.num])
                self.trainers[m.num].trainUntilConvergence(maxEpochs=30)

    def getTime(self, system):
        s = self.search(system)
        if s != None:
            for m in system.modules:
                m.time = s.modules[m.num].time
            return True
        for m in system.modules:
            if len(self.ds[m.num]) >= 4:
                m.time = int(self.nets[m.num].activate(self.sys2array(system))[0])
            else:
                return False
        return True


