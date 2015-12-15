import random, os, xml.dom.minidom, sys
from Common.Module import NONE, NVP01, NVP11, RB11, Module
from Common.Algorithm import Algorithm
from Common.Schedule import Schedule, Link
from Common.Constraints import TimeConstraints

class System:
    '''
    Represents a system.
    '''
    constraints = []
    def __init__(self):
        self.modules = []
        self.rel = -1.0
        self.cost = -1
        self.penalty = 1.0
        self.num = 0

    def __eq__(self, other):
        if other == None:
            return False
        for m1, m2 in zip(self.modules, other.modules):
            if not (m1 == m2):
                return False
        return True

    def distance(self, other):
        '''
        :param other: other system.
        :returns: number of different modules for self and other.
        '''
        res = 0
        for m in self.modules:
            if not (m == other.modules[m.num]):
                res += 1
        return res

    def __computeRel(self):
        self.rel = 1.0
        for m in self.modules:
            self.rel *= m.rel

    def __computeCost(self):
        self.cost = 0
        for m in self.modules:
            self.cost += m.cost

    def __computeTime(self, use_metamodel=True, add=True):
        #for m in self.modules:
        #   s = Module.conf.metamodel.search(self, m.num)
        Algorithm.timecounts += 1
        l = []
        if not any(isinstance(c, TimeConstraints) for c in self.constraints):
            return
        if not use_metamodel or not Algorithm.algconf.use_metamodel:
            self.getTimesSim()
            if Algorithm.algconf.use_metamodel and add:
                Algorithm.algconf.metamodel.add(self)
            return
        if not Algorithm.algconf.metamodel.getTime(self):
            self.getTimesSim()
            if add:
                Algorithm.algconf.metamodel.add(self)

    def __computeModTime(self, l, num):
        if l[num]:
            return
        start = 0
        for m in Module.conf.modules[num].src:
            n = Module.conf.modules.index(m)
            self.__computeModTime(l, n)
            end = self.modules[n].time
            if end > start:
                start = end
        transfer = 0
        for d in Module.conf.modules[num].dst:
            transfer += d[1]
        self.modules[num].time = start + self.modules[num].execTime + transfer
        l[num] = True

    def Update(self, use_metamodel=True, add=True):
        '''
        Updates reliability, cost and times.
        Call it after every changing in modules!!!
        :param use_metamodel: if metamodel is used.
        :param add: if we should add new solution to metamodel base.
        '''
        self.__computeCost()
        self.__computeRel()
        self.__computeTime(use_metamodel, add)
        self.ComputePenalty()

    def ComputePenalty(self):
        self.penalty = 1.0
        for c in self.constraints:
            self.penalty *= c.GetPenalty(self)

    def CheckConstraints(self):
        '''
        Checks all constraints.
        '''
        ok = True
        for c in self.constraints:
            ok = c.CheckConstraints(self)
            if not ok:
                break
        return ok

    def GenerateRandom(self, checkConstraints):
        '''
        Generates random solution.
        :param checkConstraints: if generated solution must satisfy constraints.
        '''
        for j in range(Algorithm.algconf.maxGenIter):
            self.modules = []
            for i in range(Module.conf.modNum):
                type = random.choice(Module.conf.modules[i].tools)
                if type == "none":
                    self.modules.append(NONE(i))
                elif type == "nvp01":
                    self.modules.append(NVP01(i))
                elif type == "nvp11":
                    self.modules.append(NVP11(i))
                else:
                    self.modules.append(RB11(i))
            self.Update(False)
            if not checkConstraints or self.CheckConstraints():
                break

    def __str__(self):
        s = "Rel = %0.6f Cost = %d [" %(self.rel,self.cost)
        for i in self.modules:
            s+= str(i.time) + ","
        s = s[:-1]+"]"  
        #print "\n"
        #for i in self.modules:
        #    s += str(i)
        return s

    def toSchedule(self):
        '''
        Generates xml-file with schedule for self
        '''
        sch = Schedule()
        for m in self.modules:
            m.toSchedule(sch)
        for l in Module.conf.links:
            src = self.modules[l.src.num]
            dst = self.modules[l.dst.num]
            src_str = ""
            dst_str = ""
            if isinstance(src, NONE) or isinstance(src, NVP01):
                src_str = "t" + str(src.num)
            if isinstance(src, NVP11) or isinstance(src, RB11):
                src_str = "t" + str(src.num) + "_snd"
            if isinstance(dst, NONE) or isinstance(dst, NVP01):
                dst_str = "t" + str(dst.num)
            if isinstance(dst, NVP11) or isinstance(dst, RB11):
                dst_str = "t" + str(dst.num) + "_rcv"
            sch.links.append(Link(src_str, dst_str, l.vol))
        filename = "sch" + str(os.getpid()) + ".xml"
        sch.exportXML(filename)

    def getTimesSim(self):
        '''
        Runs simulation experiment for self and finds module times.
        '''
        Algorithm.simcounts += 1
        self.toSchedule()
        sch = "sch" + str(os.getpid()) + ".xml"
        res = "res" + str(os.getpid()) + ".xml"
        #os.system("python Common/Timecounter.py %s %s" % (sch, res))
        if sys.platform.startswith("win"):
            os.system(u"python.exe Common/Timecounter.py %s %s" % (unicode(sch), unicode(res)))
        else:
            os.system("python Common/Timecounter.py %s %s" % (sch, res))
        f = open(res, "r")
        dom = xml.dom.minidom.parse(f)
        for task in dom.getElementsByTagName("task"):
            id = task.getAttribute("id")
            id = id.replace("t","")
            time = int(task.getAttribute("time"))
            if id.find("_snd") > 0:
                num = int(id.replace("_snd",""))
                self.modules[num].time = time
                continue
            if id.find("_") == -1:
                num = int(id)
                self.modules[num].time = time
                continue
        f.close()