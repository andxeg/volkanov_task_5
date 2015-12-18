from Common.Algorithm import Algorithm
from Common.Module import Module
from Common.System import System
from Common.Core import genEvent
from Common.Module import Module
from Common.Statistics import Execution
import random, copy, time
from math import *


class Ant:
    def __init__(self):
        self.subsystemNumbers = len(Module.conf.modules)
        #EDGES_WHERE_WERE_ANT
        #[ [ver1 ... verk ] ->  1st subsystem; sublist.length - amount of the parallel elements
        #                       in this subsystem. veri - their versions
        # ...
        #  [] -> Nst subsystem
        # ]
        self.path = []

    def computeCost(self):
        systemCost = 0
        for subsystem in range(len(self.path)):
            for element in self.path[subsystem]:
                systemCost += Module.conf.modules[subsystem].sw[element].cost

        return systemCost

    def computeRel(self):
        systemRel = 1.0
        for subsystem in range(len(self.path)):
            subsystemFail = 1.0
            for element in self.path[subsystem]:
                subsystemFail *= (1.0 - Module.conf.modules[subsystem].sw[element].rel)
            systemRel *= (1.0 - subsystemFail)

        return systemRel

    def computeWeight(self):
        systemWeight = 0
        for subsystem in range(len(self.path)):
            for element in self.path[subsystem]:
                systemWeight += Module.conf.modules[subsystem].sw[element].weight

        return systemWeight

    def checkConstraints(self, cost, weight):
        return self.computeCost() <= cost and self.computeWeight() <= weight

    def printDecision(self):
        print "Reliability: %f | Cost: %d | Weight: %d\n" % \
              (self.computeRel(), self.computeCost(), self.computeWeight())
        for subsystem in range(len(self.path)):
            print "Subsystem number-> %d consists of " % subsystem
            for element in self.path[subsystem]:
                #in real life elements counted from 1
                print element + 1

class SubSystem:
    def __init__(self, moduleConfig):
        self.pmax = Algorithm.algconf.pmax
        self.versionsCount = len(moduleConfig.sw)
        self.versions = copy.deepcopy(moduleConfig.sw)

        #PHEROMONE_ON_THE_EDGES_INITIALIZATION
        self.edges = []
        #Edges between subsystem-nodes and count-components-in-subsystem-nodes
        edgesFirstType = []
        #Edges between count-components-in-subsystem-node and version-nodes
        edgesSecondType = []

        for i in range(self.pmax):
            edgesFirstType.append(Algorithm.algconf.pheromone0)

        self.edges.append(edgesFirstType)

        for i in range(self.pmax):
            for j in range(self.versionsCount):
                edgesSecondType.append(Algorithm.algconf.pheromone0)
            self.edges.append(edgesSecondType)
            edgesSecondType = []


    def probabilitiesFirstTypeEdges(self):
        probs = copy.deepcopy(self.edges[0])
        probs = map(lambda x: pow(x, Algorithm.algconf.alpha1), probs)
        sumProbsElem = reduce(lambda x,y: x+y, probs)
        probs = map(lambda x: x/sumProbsElem, probs)
        return probs

    def probabilitiesSecondTypeEdges(self, elements):
        #elements in [1..pmax]
        probs = copy.deepcopy(self.edges[elements])
        probs = map(lambda x: pow(x, Algorithm.algconf.alpha2), probs)
        heuristicInfo = []
        for version in self.versions:
            heuristicInfo.append(version.rel/pow(version.weight,3))
        heuristicInfo = map(lambda x: pow(x, Algorithm.algconf.beta), heuristicInfo)
        probs = map(lambda x,y: x*y, probs, heuristicInfo)
        sumProbsElem = reduce(lambda x,y: x+y, probs)
        probs = map(lambda x: x/sumProbsElem, probs)
        return probs

    def printSubSystem(self):
        for version in self.versions:
            print "[SW] (num %f) (cost %f) (rel %f) (weight %f)\n" % \
                  (version.num, version.cost, version.rel, version.weight)


class ACODC(Algorithm):
    def __init__(self):
        Algorithm.__init__(self)
        self.system = []
        self.ants = []

    def Step(self):
        self._createAnts()
        self._buildSeriesParallelStructure()
        self._updatePheromones()
        self.currentIter += 1


    def Run(self):
        Algorithm.timecounts = 0
        Algorithm.simcounts = 0
        Algorithm.time = time.time()
        #SYSTEM INITIALIZATION.
        for module in Module.conf.modules:
            self.system.append(SubSystem(module))

        #SET_FIRST_BEST_SOLUTION
        #SOLUTION == [ANT, RELIABILITY]
        #ALL INFORMATION ABOUT SYSTEM STRUCTURE KEEP IN ANT.path
        self.currentSolution = self._initialDecision()

        while not self._algorithmFinished():
            self.Step()
            print "Iteration# %d | Current reliability %f\n" % \
                (self.currentIter, self.currentSolution[1])

        Algorithm.time = time.time() - Algorithm.time
        print "Best solution:\n"
        self.currentSolution[0].printDecision()
        print "Reliability: %f | Algorithm time calculation %f\n" % \
            (self.currentSolution[1], Algorithm.time)

        #TODO: MAKE PRINT RESULT WITH self.stat


    def Clear(self):
        Algorithm.Clear(self)
        #reset local variable

    def _initialDecision(self):
        #The first solution had to be selected manually
        #for 14 subsystem in system, limitcost == 130, limitweight == 159
        #all versions of elements in each subsystem take from article
        #in the input file elements sorted from high-rel to low-rel
        decision = [Ant(), 0.0]
        for i in range(len(Module.conf.modules)):
            decision[0].path.append([len(Module.conf.modules[i].sw)-1])

        decision[1] = decision[0].computeRel()
        return decision

    def _algorithmFinished(self):
        return self.currentIter >= Algorithm.algconf.maxIter

    def _createAnts(self):
        self.ants = []
        for i in range(Algorithm.algconf.antCounts):
            self.ants.append(Ant())

    def _buildSeriesParallelStructure(self):
        for ant in self.ants:
            self._globalSearch(ant)
            if not ant.checkConstraints(Module.conf.limitcost, Module.conf.limitweight):
                continue

            currentRel = ant.computeRel()

            #print "After global search ", currentRel
            #ant.printDecision()

            if (currentRel >= self.currentSolution[1] or
                0 <= ((self.currentSolution[1] - currentRel) / self.currentSolution[1]) <= Algorithm.algconf.affinity):
                #ant -> CANNOT_BE_MODIFIED_AS_IT_IS_USED_IN_THE_CALCULATION_OF_PHEROMONE_UPDATE
                solution = self._localSearch(ant)
            else:
                continue

            newDecision = Ant()
            newDecision.path = copy.deepcopy(solution.path)
            #Update_the_best_solution
            self.currentSolution[0] = newDecision
            self.currentSolution[1] = newDecision.computeRel()


    def _globalSearch(self, ant):
        #print "_globalSearch system SIZE -> ", len(self.system)
        for subsystem in self.system:
            #CHOOSE_FIRST_EDGE
            parallelCount = subsystem.pmax
            probs = subsystem.probabilitiesFirstTypeEdges()
            probs.append(0.0)
            probs.sort()
            print "First edges probabilities", probs
            p = random.random()
            #print "random ->", p
            for i in range(len(probs) - 1):
                #print "choose parallel"
                if probs[i] <= p <= probs[i+1]:
                    parallelCount = i + 1
                    break

            #print "Parallel count -> ", parallelCount
            #NOW_WE_KNOW_HOW_MUCH_PARALLEL_ELEMENTS_IN_CURRENT_SUBSYSTEM
            #THEN_WE_MUST_CHOOSE_THIS_ELEMENTS
            probs = subsystem.probabilitiesSecondTypeEdges(parallelCount)
            probs.append(0.0)
            probs.sort()
            #print "Second edges probabilities", probs
            elements = []
            for element in range(parallelCount):
                p = random.random()
                #print "random -> ", p
                el = subsystem.versionsCount - 1
                for i in range(0, len(probs) - 1):
                    #print "choose element"
                    if probs[i] <= p <= probs[i+1]:
                        #elements counted from (0) to (subsystem.versionsCount - 1)
                        el = i
                        #print "Added element ->", i
                        break
                elements.append(el)

            ant.path.append(elements)
        #print "End in _globalSearch"
        #ant.printDecision()

    def _localSearch(self, ant):
        maxIterWithoutChanges = Algorithm.algconf.dcMaxIterWithoutChange
        curriter = 0
        #INITIAL_SOLUTION
        solution = Ant()
        solution.path = copy.deepcopy(ant.path)
        #INITIAL_RELIABILITY
        L = solution.computeRel()
        #STEP_OF_DEGRADED_CEILING_ALGORITHM
        deltaL = Algorithm.algconf.localSearchStep

        while curriter < maxIterWithoutChanges:
        #FIND_NEIGHBORHOOD
            neighborhood = Ant()
            neighborhood.path = copy.deepcopy(solution.path)
            #CHOOSE_THE_NUMBER_OF_SUBSYSTEMS_WHICH_WE_WILL_CHANGE
            changeCount = random.randint(1, len(Module.conf.modules))
            for i in range(changeCount):
                #CHOOSE_RANDOM_SUBSYSTEM
                changeSubsystem = random.randint(0, len(Module.conf.modules) - 1)
                subsystem = neighborhood.path[changeSubsystem]
                #CHOOSE_RANDOM_ELEMENT_IN_CURRENT_SUBSYSTEM
                availableVersions = len(Module.conf.modules[changeSubsystem].sw)
                oldElement = random.randint(0, len(subsystem) - 1)
                newElement = self._getNewElement(availableVersions, subsystem[oldElement])
                #MODIFY_SUBSYSTEM
                subsystem[oldElement] = newElement

            #NOW_WE_OBTAIN_NEIGHBORHOOD
            if not neighborhood.checkConstraints(Module.conf.limitcost, Module.conf.limitweight):
                #not increment iter in this case, because we didn't obtain feasible neighborhood
                #set counter in 0 in the following case -> when neighborhood is better than solution
                #else increment
                continue

            newRel = neighborhood.computeRel()
            if (newRel >= solution.computeRel() or newRel >= L):
                solution.path = copy.deepcopy(neighborhood.path)
                L += deltaL
                curriter = 0
            else:
                curriter += 1
                continue

        return solution

    def _getNewElement(self, availableVersions, oldElement):
        maxIterations = 1000
        newElement = 0
        for i in range(maxIterations):
            p = random.randint(0, availableVersions - 1)
            if p != oldElement:
                newElement = p
                break
        return newElement

    def _updatePheromones(self):
        #RUN_THROUGH_ALL_ANTS
        for ant in self.ants:
            #RUN_THROUGH_ALL_SUBSYSTEM
            for i in range(len(ant.path)):
                subsystem = ant.path[i]
                parallelElements = len(subsystem)
                #MODIFY_PHEROMONE_ON_THE_FIRST_TYPE_EDGE
                delta = Algorithm.algconf.Q * self._penalty(ant) * float(ant.computeRel())
                #print "Update pheromones OLD -> ", self.system[i].edges[0][parallelElements - 1]

                self.system[i].edges[0][parallelElements - 1] = \
                    self.system[i].edges[0][parallelElements - 1] * \
                    Algorithm.algconf.ro + delta

                #print "Update pheromones NEW -> ", self.system[i].edges[0][parallelElements - 1]

                #MODIFY_PHEROMONE_ON_THE_SECOND_TYPE_EDGES
                #SUBSYSTEM_KEEP_ALL_SECOND_TYPE_EDGES_WHERE_ANT_WAS
                for j in subsystem:
                    self.system[i].edges[parallelElements][j] = \
                        self.system[i].edges[parallelElements][j] * \
                        Algorithm.algconf.ro + delta


    def _penalty(self, ant):
        cost = ant.computeCost()
        weight = ant.computeWeight()
        if cost > Module.conf.limitcost and weight > Module.conf.limitweight:
            return pow(float(Module.conf.limitcost)/cost, Algorithm.algconf.a) * \
                   pow(Module.conf.limitweight/weight, Algorithm.algconf.b)

        if cost > Module.conf.limitcost:
            return pow(float(Module.conf.limitcost)/cost, Algorithm.algconf.a)

        if weight > Module.conf.limitweight:
            return pow(float(Module.conf.limitweight)/weight, Algorithm.algconf.b)
        else:
            return 0



