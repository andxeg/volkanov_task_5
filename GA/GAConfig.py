from Common.AlgConfig import AlgConfig

class GAParameter:
    def __init__(self, min, norm, max):
        self.min = min
        self.norm = norm
        self.max = max
        self.cur = norm

class GAConfig(AlgConfig):
    def __init__(self):
        AlgConfig.__init__(self)
        self.popNum = 30
        self.maxIter = 30
        self.crossPercent = GAParameter(0.7, 0.8, 0.9)
        self.Pcross = GAParameter(0.5, 0.75, 1.0)
        self.mutPercent = GAParameter(0.7, 0.8, 0.9)
        self.Pmut = GAParameter(0.5, 0.75, 0.9)

    def LoadFromXmlNode(self, node):
        AlgConfig.LoadFromXmlNode(self,node)
        self.popNum = int(node.getAttribute("popsize"))
        self.maxIter = int(node.getAttribute("maxiter"))
        type = node.getAttribute("type")
        for p in node.getElementsByTagName("par"):
            name = p.getAttribute("name")
            norm = float(p.getAttribute("norm"))
            if type=="hga":
                min = float(p.getAttribute("min"))
                max = float(p.getAttribute("max"))
                par = GAParameter(min, norm, max)
            else:
                par = GAParameter(None,norm,None)
            if name=="crosspercent":
                self.crossPercent = par
            elif name=="crossprob":
                self.Pcross = par
            elif name=="mutpercent":
                self.mutPercent = par
            elif name=="mutprob":
                self.Pmut = par