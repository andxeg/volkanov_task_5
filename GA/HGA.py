from GA import GA
import copy

class HGA(GA):
    def __init__(self):
        GA.__init__(self)
        self.prevSolution = None
        self.prevAvg = -1
        self.currentAvg = -1
        
    def Step(self):
        self._select()
        self._recombine()
        self._mutate()
        self._evalPopulation()
        self._fuzzyLogic()

    def Clear(self):
        GA.Clear(self)
        self.prevSolution = None
        self.prevAvg = -1
        self.currentAvg = -1
        self.algconf.crossPercent.cur = self.algconf.crossPercent.norm
        self.algconf.Pcross.cur = self.algconf.Pcross.norm

    def _fuzzyLogic(self):
        if self.currentSolution == None or self.prevSolution == None:
            self.algconf.crossPercent.cur = self.algconf.crossPercent.max
            self.algconf.Pcross.cur = self.algconf.Pcross.max
            self.algconf.mutPercent.cur = self.algconf.mutPercent.max
            self.algconf.Pmut.cur = self.algconf.Pmut.max
            return
        self.currentAvg = reduce(lambda a, b: a + b.rel, self.population, 0)/len(self.population)
        if self.currentIter > 1:
            bestDiff = (self.currentSolution.rel - self.prevSolution.rel)/self.currentSolution.rel
            avgDiff = (self.currentAvg - self.prevAvg)/self.currentAvg
            if bestDiff >= 0.01:
                self.algconf.crossPercent.cur = self.algconf.crossPercent.max
                self.algconf.Pcross.cur = self.algconf.Pcross.max
            else:
                self.algconf.crossPercent.cur = self.algconf.crossPercent.min
                self.algconf.Pcross.cur = self.algconf.Pcross.min
            if avgDiff >= 0.03:
                self.algconf.mutPercent.cur = self.algconf.mutPercent.min
                self.algconf.Pmut.cur = self.algconf.Pmut.min
            elif avgDiff > -0.03 and avgDiff < 0.03:
                self.algconf.mutPercent.cur = self.algconf.mutPercent.norm
                self.algconf.Pmut.cur = self.algconf.Pmut.norm
            elif avgDiff <= -0.03:
                self.algconf.mutPercent.cur = self.algconf.mutPercent.max
                self.algconf.Pmut.cur = self.algconf.Pmut.max
        self.prevSolution = copy.deepcopy(self.currentSolution)
        self.prevAvg = self.currentAvg
   
