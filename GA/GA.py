from Common.Algorithm import Algorithm
from Common.System import System
from Common.Core import genEvent
from Common.Module import NONE, NVP01, NVP11, RB11, Module
from Common.Statistics import Execution
import random, copy, time

class GA(Algorithm):
    def __init__(self):
        Algorithm.__init__(self)
        self.population = []
        self.iterWithoutChange = 0

    def Step(self):
        self._select()
        self._recombine()
        self._mutate()
        self._evalPopulation()

    def Run(self):
        self.Clear()
        Algorithm.timecounts = 0
        Algorithm.simcounts = 0
        Algorithm.time = time.time()
        for i in range(self.algconf.popNum):
            s = System()
            s.GenerateRandom(True)
            self.population.append(s)
        if Algorithm.algconf.metamodel:
            Algorithm.algconf.metamodel.Update()
        self.population.sort(key=lambda x: x.rel * x.penalty, reverse = True)
        while not self._checkStopCondition():
            self.Step()
            print self.currentIter, self.currentSolution
        print "Best solution: ", self.currentSolution
        print "--------------------------------------\n"
        Algorithm.time = time.time() - Algorithm.time
        self.stat.AddExecution(Execution(self.currentSolution, self.currentIter, Algorithm.time, Algorithm.timecounts, Algorithm.simcounts))

    def Clear(self):
        Algorithm.Clear(self)
        self.population = []
        self.iterWithoutChange = 0
        self.candidate = None

    def _mutate(self):
        for s in self.population[int((1.0-self.algconf.mutPercent.cur) * self.algconf.popNum):]:
            if random.random() <= self.algconf.Pmut.cur:
                k = random.randint(0, Module.conf.modNum-1)
                if self.currentIter > 500 and self.currentSolution == None:
                    type = "none"
                else:
                    type = random.choice(Module.conf.modules[k].tools)
                if type == "none":
                    new = NONE(k)
                elif type == "nvp01":
                    new = NVP01(k)
                elif type == "nvp11":
                    new = NVP11(k)
                else:
                    new = RB11(k)
                s.modules[k] = new
                s.Update()
            
    def _select(self):
        probabilities = []
        sum = 0.0 
        for s in self.population:
            val = s.rel*s.penalty
            sum += val
            probabilities.append(val)
        for p in range(self.algconf.popNum):
            probabilities[p] = probabilities[p]/sum
        nums = range(self.algconf.popNum)
        events = dict(zip(nums, probabilities))
        new_pop = []
        for i in nums:
            new_pop.append(self.population[genEvent(events)])
        self.population = new_pop
        self.population.sort(key=lambda x: x.rel * x.penalty, reverse = True)

    def _recombine(self):
        if Module.conf.modNum == 1:
            return
        new_pop = []
        notCrossNum =  int((1.0 - self.algconf.crossPercent.cur) * self.algconf.popNum)
        for i in range(notCrossNum):
            new_pop.append(copy.deepcopy(self.population[i]))
        for i in range(self.algconf.popNum/2):
            if random.random() <= self.algconf.Pcross.cur:
                parents = random.sample(self.population,  2)
                k = random.randint(1,Module.conf.modNum-1)
                child1 = parents[0].modules[0:k] + parents[1].modules[k:Module.conf.modNum]
                child2 = parents[1].modules[0:k] + parents[0].modules[k:Module.conf.modNum]
                parents[0].modules = child1
                parents[1].modules = child2
                parents[0].Update()
                parents[1].Update()
        self.population.sort(key=lambda x: x.rel * x.penalty, reverse = True)
        new_pop += self.population[:self.algconf.popNum - notCrossNum]
        self.population = new_pop
        self.population.sort(key=lambda x: x.rel * x.penalty, reverse = True)

    def _evalPopulation(self):
        self.currentIter += 1
        self.iterWithoutChange += 1
        self.population.sort(key=lambda x: x.rel * x.penalty, reverse = True)
        not_use_metamodel = Algorithm.algconf.metamodel==None or random.random() <= self.algconf.pop_control_percent
        for s in self.population:
            if not_use_metamodel:
                if self.candidate:
                    self.candidate.Update(use_metamodel=False)
                    if self.candidate.CheckConstraints() and (self.currentSolution == None or self.candidate.rel > self.currentSolution.rel):
                            self.currentSolution = copy.deepcopy(self.candidate)
                            self.iterWithoutChange = 0
                s.Update(use_metamodel=False)
                if s.CheckConstraints() and (self.currentSolution == None or s.rel > self.currentSolution.rel):
                    self.currentSolution = copy.deepcopy(s)
                    self.iterWithoutChange = 0
                    self.candidate = None
                    break
            else:
                if s.CheckConstraints() and (self.currentSolution == None or self.candidate == None or s.rel > self.candidate.rel):
                    self.candidate = copy.deepcopy(s)
                    break
        if not_use_metamodel and Algorithm.algconf.metamodel:
            Algorithm.algconf.metamodel.Update()

    def _checkStopCondition(self):
        if self.currentSolution != None and self.iterWithoutChange > self.algconf.maxIter:
            self.currentSolution.Update(use_metamodel=False)
            if self.currentSolution.CheckConstraints():
                return True

        if self.currentSolution == None and self.iterWithoutChange >= 1000:
            self.currentSolution = System()
            self.currentSolution.rel = 0
            for m in Module.conf.modules:
                self.currentSolution.modules.append(NONE(m.num))
            return True
        return False