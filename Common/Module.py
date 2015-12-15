import random
from Common.Schedule import Task, Link

class Module:
    '''Base class for system module.
    :param num: Number of module.
    :param hw: List of used HW versions. DO NOT USE -1 FOR ABSENT VERSIONS!
    :param sw: List of used SW versions. DO NOT USE -1 FOR ABSENT VERSIONS!
    '''
    conf = None
    def __init__(self, num, hw, sw):
        self.num = num
        self.hw = hw
        self.sw = sw
        self.time = -1
        self.cost = -1
        self.rel = -1
        self._computeRel()
        self._computeCost()
        self._computeExecTime()

    def __eq__(self, other):
        '''Operator ==
        '''
        return self.num ==  other.num and self.hw == other.hw and self.sw == other.sw

class NONE(Module):
    '''Class for module with NONE mechanism.
    :param num: number of module
    :param hw: List of used HW versions. DO NOT USE -1 FOR ABSENT VERSIONS! MUST CONTAIN 0 OR 1 ELEMENT.
    :param sw: List of used SW versions. DO NOT USE -1 FOR ABSENT VERSIONS! MUST CONTAIN 0 OR 1 ELEMENT.

    If len(hw) == 0  and len(sw) == 0 module is generated randomly.
    '''
    def __init__(self, num, hw = [], sw = []):
        if hw == [] and sw == []:
            hw = [random.randint(0, len(self.conf.modules[num].hw)-1)]
            sw = [random.randint(0, len(self.conf.modules[num].sw)-1)]
        Module.__init__(self, num, hw, sw)

    def toSchedule(self, schedule):
        '''Adds elements, corresponding to module to schedule.
        :param schedule: object of class 'Schedule'.
        '''
        schedule.tasks.append(Task("t"+str(self.num), self.execTime, "p"+str(self.num), 0))

    def _computeRel(self):
        self.rel = self.conf.modules[self.num].hw[self.hw[0]].rel * self.conf.modules[self.num].sw[self.sw[0]].rel

    def _computeCost(self):
        self.cost = self.conf.modules[self.num].hw[self.hw[0]].cost + self.conf.modules[self.num].sw[self.sw[0]].cost

    def _computeExecTime(self):
        self.execTime = self.conf.modules[self.num].times[self.sw[0]][self.hw[0]]

    def __str__(self):
        '''Converts module to string. So we can 'print module'
        '''
        return "\t"+str(self.num)+ ". None:" + str(self.hw) + str(self.sw) + "\n"


class NVP01(Module):
    def __init__(self, num, hw=[], sw=[]):
        if hw == [] and sw == []:
            hw = [random.randint(0, len(self.conf.modules[num].hw)-1)]
            sw1 = random.randint(0, len(self.conf.modules[num].sw)-3)
            sw2 = random.randint(sw1+1, len(self.conf.modules[num].sw)-2)
            sw = [sw1, sw2, random.randint(sw2+1, len(self.conf.modules[num].sw)-1)]
        Module.__init__(self, num, hw, sw)

    def _computeRel(self):
        Qhw = self.conf.modules[self.num].hw[self.hw[0]].rel;     Phw = 1 - Qhw
        Qsw0 = self.conf.modules[self.num].sw[self.sw[0]].rel;    Psw0 = 1 - Qsw0
        Qsw1 = self.conf.modules[self.num].sw[self.sw[1]].rel;    Psw1 = 1 - Qsw1
        Qsw2 = self.conf.modules[self.num].sw[self.sw[2]].rel;    Psw2 = 1 - Qsw2
        Qrv = self.conf.modules[self.num].qrv;                    Prv = 1 - Qrv
        Qd = self.conf.modules[self.num].qd;                      Pd = 1 - Qd
        Qall = self.conf.modules[self.num].qall;                  Pall = 1 - Qall
        P = (Prv +
             Qrv * Prv +
             Qrv * Qrv * Prv +
             Qrv * Qrv * Qrv * Pd +
             Qrv * Qrv * Qrv * Qd * Pall +
             Qrv * Qrv * Qrv * Qd * Qall * Phw +
             Qrv * Qrv * Qrv * Qd * Qall * Qhw * Psw0 * Psw1 +
             Qrv * Qrv * Qrv * Qd * Qall * Qhw * Qsw0 * Psw1 * Psw2 +
             Qrv * Qrv * Qrv * Qd * Qall * Qhw * Qsw1 * Psw0 * Psw2)
        self.rel = 1 - P

    def _computeCost(self):
        self.cost = (self.conf.modules[self.num].hw[self.hw[0]].cost +
                     self.conf.modules[self.num].sw[self.sw[0]].cost +
                     self.conf.modules[self.num].sw[self.sw[1]].cost +
                     self.conf.modules[self.num].sw[self.sw[2]].cost)
        
    def _computeExecTime(self):
        self.execTime = (self.conf.modules[self.num].times[self.sw[0]][self.hw[0]] +
                         self.conf.modules[self.num].times[self.sw[1]][self.hw[0]] +
                         self.conf.modules[self.num].times[self.sw[2]][self.hw[0]] +
                         self.conf.modules[self.num].tvote)

    def toSchedule(self, schedule):
        schedule.tasks.append(Task("t"+str(self.num), self.execTime, "p"+str(self.num), 0))

    def __str__(self):
        return "\t"+str(self.num)+ ". NVP01:" + str(self.hw) + str(self.sw) + "\n"


class NVP11(Module):
    def __init__(self, num, hw = [], sw = []):
        if hw == [] and sw == []:
            hw = [random.randint(0, len(self.conf.modules[num].hw)-1),
                  random.randint(0, len(self.conf.modules[num].hw)-1),
                  random.randint(0, len(self.conf.modules[num].hw)-1)]
            sw1 = random.randint(0, len(self.conf.modules[num].sw)-3)
            sw2 = random.randint(sw1+1, len(self.conf.modules[num].sw)-2)
            sw = [sw1, sw2, random.randint(sw2+1, len(self.conf.modules[num].sw)-1)]
        Module.__init__(self, num, hw, sw)

    def _computeRel(self):
        Qhw0 = self.conf.modules[self.num].hw[self.hw[0]].rel;      Phw0 = 1 - Qhw0
        Qhw1 = self.conf.modules[self.num].hw[self.hw[1]].rel;      Phw1 = 1 - Qhw1
        Qhw2 = self.conf.modules[self.num].hw[self.hw[2]].rel;      Phw2 = 1 - Qhw2
        Qsw0 = self.conf.modules[self.num].sw[self.sw[0]].rel;      Psw0 = 1 - Qsw0
        Qsw1 = self.conf.modules[self.num].sw[self.sw[1]].rel;      Psw1 = 1 - Qsw1
        Qsw2 = self.conf.modules[self.num].sw[self.sw[2]].rel;      Psw2 = 1 - Qsw2
        Qrv = self.conf.modules[self.num].qrv;                      Prv = 1 - Qrv
        Qd = self.conf.modules[self.num].qd;                        Pd = 1 - Qd
        Qall = self.conf.modules[self.num].qall;                    Pall = 1 - Qall
        Qrv3 = Qrv**3
        P = (Prv +
             Qrv * Prv +
             Qrv * Qrv * Prv +
             Qrv3 * Pd +
             Qrv3 * Qd * Pall +
             Psw0 * Psw1 * Qrv3 * Qd * Qall +
             Psw0 * Psw2 * Qsw1 * Qrv3 * Qd * Qall +
             Psw2 * Psw1 * Qsw0 * Qrv3 * Qd * Qall +
             Psw0 * Phw0 * Phw1 * Qsw1 * Qsw2 * Qrv3 * Qd * Qall * Qhw2+
             Qrv3 * Qd * Qall * Phw0 * Phw2 * Qhw1 * Qsw2 * (1 - Psw0 * Psw1) +
             Psw2 * Phw0 * Phw2 * Qsw0 * Qsw1 * Qrv3 * Qd * Qall * Qhw1 +
             Qrv3 * Qd * Qall * Phw1 * Phw2 * Qhw0 * Qsw1 * (1 - Psw0 * Psw2) +
             Psw1 * Phw1 * Phw2 * Qsw0 * Qsw2 * Qrv3 * Qd * Qall * Qhw0 +
             Qrv3 * Qd * Qall * Phw0 * Phw1 * Qhw2 * Qsw0 * (1 - Psw2 * Psw1) +
             Psw0 * Phw2 * Qsw2 * Qsw2 * Qrv3 * Qd * Qall * Qhw0 * Qhw1 +
             Psw0 * Phw1 * Qsw1 * Qsw2 * Qrv3 * Qd * Qall * Qhw0 * Qhw2 +
             Psw1 * Phw1 * Qsw0 * Qsw2 * Qrv3 * Qd * Qall * Qhw0 * Qhw1 +
             Psw1 * Phw0 * Qsw0 * Qsw2 * Qrv3 * Qd * Qall * Qhw1 * Qhw2 +
             Psw2 * Phw0 * Qsw0 * Qsw1 * Qrv3 * Qd * Qall * Qhw0 * Qhw2 +
             Psw2 * Phw1 * Qsw0 * Qsw1 * Qrv3 * Qd * Qall * Qhw1 * Qhw2)
        self.rel = 1 - P

    def _computeCost(self):
        self.cost = (self.conf.modules[self.num].hw[self.hw[0]].cost +
                     self.conf.modules[self.num].hw[self.hw[1]].cost +
                     self.conf.modules[self.num].hw[self.hw[2]].cost +
                     self.conf.modules[self.num].sw[self.sw[0]].cost +
                     self.conf.modules[self.num].sw[self.sw[1]].cost +
                     self.conf.modules[self.num].sw[self.sw[2]].cost)
        
    def _computeExecTime(self):
        self.execTime = (max([self.conf.modules[self.num].times[self.sw[0]][self.hw[0]],
                         self.conf.modules[self.num].times[self.sw[1]][self.hw[1]],
                         self.conf.modules[self.num].times[self.sw[2]][self.hw[2]]]) +
                         self.conf.modules[self.num].tvote)

    def toSchedule(self, schedule):
        schedule.tasks.append(Task("t"+str(self.num)+"_rcv", 0, "p"+str(self.num)+"_1", 0))
        schedule.tasks.append(Task("t"+str(self.num)+"_1",
            self.conf.modules[self.num].times[self.sw[0]][self.hw[0]],
            "p"+str(self.num)+"_1", 1))
        schedule.tasks.append(Task("t"+str(self.num)+"_2",
            self.conf.modules[self.num].times[self.sw[1]][self.hw[1]],
            "p"+str(self.num)+"_2", 0))
        schedule.tasks.append(Task("t"+str(self.num)+"_3",
            self.conf.modules[self.num].times[self.sw[2]][self.hw[2]],
            "p"+str(self.num)+"_3", 0))
        schedule.tasks.append(Task("t"+str(self.num)+"_snd",
            self.conf.modules[self.num].tvote,
            "p"+str(self.num)+"_1", 2))
        schedule.links.append(Link("t"+str(self.num)+"_rcv", "t"+str(self.num)+"_2", self.conf.modules[self.num].input))
        schedule.links.append(Link("t"+str(self.num)+"_rcv", "t"+str(self.num)+"_3", self.conf.modules[self.num].input))
        schedule.links.append(Link("t"+str(self.num)+"_2", "t"+str(self.num)+"_snd", self.conf.modules[self.num].output))
        schedule.links.append(Link("t"+str(self.num)+"_3", "t"+str(self.num)+"_snd", self.conf.modules[self.num].output))


    def __str__(self):
        return "\t"+str(self.num)+ ". NVP11:" + str(self.hw) + str(self.sw) + "\n"


class RB11(Module):
    def __init__(self, num, hw = [], sw = []):
        if hw == [] and sw == []:
            hw = [random.randint(0, len(self.conf.modules[num].hw)-1),
                  random.randint(0, len(self.conf.modules[num].hw)-1)]
            sw1 = random.randint(0, len(self.conf.modules[num].sw)-2)
            sw = [sw1, random.randint(sw1+1, len(self.conf.modules[num].sw)-1)]
        Module.__init__(self, num, hw, sw)

    def _computeRel(self):
        Qhw0 = self.conf.modules[self.num].hw[self.hw[0]].rel;      Phw0 = 1 - Qhw0
        Qhw1 = self.conf.modules[self.num].hw[self.hw[1]].rel;      Phw1 = 1 - Qhw1
        Qsw0 = self.conf.modules[self.num].sw[self.sw[0]].rel;      Psw0 = 1 - Qsw0
        Qsw1 = self.conf.modules[self.num].sw[self.sw[1]].rel;      Psw1 = 1 - Qsw1
        Qrv = self.conf.modules[self.num].qrv;                      Prv = 1 - Qrv
        Qd = self.conf.modules[self.num].qd;                        Pd = 1 - Qd
        Qall = self.conf.modules[self.num].qall;                    Pall = 1 - Qall
        Qrv3 = Qrv**3
        P = (Prv +
             Qrv * Pd +
             Qrv * Qd * Pall +
             Qrv * Qd * Qall * Phw0 * Phw1 +
             Qrv * Qd * Qall * (1 - Phw0 * Phw1) * Psw0 * Psw1)
        self.rel = 1 - P

    def _computeCost(self):
        self.cost = (self.conf.modules[self.num].hw[self.hw[0]].cost +
                     self.conf.modules[self.num].hw[self.hw[1]].cost +
                     2 * self.conf.modules[self.num].sw[self.sw[0]].cost +
                     2 * self.conf.modules[self.num].sw[self.sw[1]].cost)
        
    def _computeExecTime(self):
        self.execTime = (max([self.conf.modules[self.num].times[self.sw[0]][self.hw[0]] +
                             self.conf.modules[self.num].times[self.sw[1]][self.hw[0]],
                             self.conf.modules[self.num].times[self.sw[0]][self.hw[1]] +
                             self.conf.modules[self.num].times[self.sw[1]][self.hw[1]]]) +
                             2 * self.conf.modules[self.num].ttest +
                             self.conf.modules[self.num].trecov)

    def toSchedule(self, schedule):
        schedule.tasks.append(Task("t"+str(self.num)+"_rcv", 0, "p"+str(self.num)+"_1", 0))
        schedule.tasks.append(Task("t"+str(self.num)+"_1",
            self.conf.modules[self.num].times[self.sw[0]][self.hw[0]] +
            self.conf.modules[self.num].times[self.sw[1]][self.hw[0]] +
            2 * self.conf.modules[self.num].ttest +
            self.conf.modules[self.num].trecov,
            "p"+str(self.num)+"_1", 1))
        schedule.tasks.append(Task("t"+str(self.num)+"_2",
            self.conf.modules[self.num].times[self.sw[0]][self.hw[1]] +
            self.conf.modules[self.num].times[self.sw[1]][self.hw[1]] +
            2 * self.conf.modules[self.num].ttest +
            self.conf.modules[self.num].trecov,
            "p"+str(self.num)+"_2", 0))
        schedule.tasks.append(Task("t"+str(self.num)+"_snd", 0, "p"+str(self.num)+"_1", 2))
        schedule.links.append(Link("t"+str(self.num)+"_rcv", "t"+str(self.num)+"_2", self.conf.modules[self.num].input))
        schedule.links.append(Link("t"+str(self.num)+"_2", "t"+str(self.num)+"_snd", self.conf.modules[self.num].output))

    def __str__(self):
        return "\t"+str(self.num)+ ". RB11:" + str(self.hw) + str(self.sw) + "\n"