class TimeConstraints:
    '''Class for time constraints.
    :param constraints: list of deadlines.
    '''
    def __init__(self, constraints):
        self.limitTimes = constraints

    def CheckConstraints(self, system):
        '''Checks if time constaraints are satisfied
        :param system: object of 'System' class.
        '''
        for m,l in zip(system.modules, self.limitTimes):
            if (m.time > l):
                return False
        return True

    def GetPenalty(self,system):
        '''Gets penalty.
        :param system: object of 'System' class.
        :returns: Float penalty.
        '''
        res = 1.0
        for m,l in zip(system.modules,self.limitTimes):
            if (m.time > l):
                res *= float(l)/m.time
        return res

class CostConstraints:
    '''Class for cost constraint.
    :param limitCost: maximum system cost.
    '''
    def __init__(self,limitCost):
        self.limitCost = limitCost

    def CheckConstraints(self,system):
        '''Checks if cost constaraint is satisfied
        :param system: object of 'System' class.
        '''
        return system.cost < self.limitCost

    def GetPenalty(self,system):
        '''Gets penalty.
        :param system: object of 'System' class.
        :returns: Float penalty.
        '''
        return float(self.limitCost)/system.cost if system.cost > self.limitCost else 1.0

class RelConstraints:
    '''Class for reliability constraint.
    :param limitRel: maximum system reliability.
    '''
    def __init__(self,limitRel):
        self.limitRel = limitRel

    def CheckConsraints(self,system):
        '''Checks if reliability constaraint is satisfied
        :param system: object of 'System' class.
        '''
        return system.rel > self.limitRel

    def GetPenalty(self,system):
        '''Gets penalty.
        :param system: object of 'System' class.
        :returns: Float penalty.
        '''
        return float(system.rel)/self.limitRel if system.rel < self.limitRel else 1.0