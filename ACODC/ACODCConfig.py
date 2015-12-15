from Common.AlgConfig import AlgConfig

class ACODCConfig(AlgConfig):
    def __init__(self):
        AlgConfig.__init__(self)

        #Maximum number of elements in parallel
        self.pmax = 4
        #Parameter that controls the relative weight of the pheromone
        #Use in the transition between subsystem-node and count-components-in-subsystem-node
        self.alpha1 = 0.1
        #Parameter thaht control the relative weight ot the pheromone
        #Use in the transition between count-components-in-subsystem-node and version-node
        self.alpha2 = 0.5
        #Parameter that control the local heuristic - version heuristic
        self.beta = 1
        #Use in pheromone update. Coefficient in front of old pheromone-value
        self.ro = 0.9
        #Use in pheromone update. Coefficient in delta-pheromone-value
        self.Q = 0.01
        #Use in pheromone update. Use in delta-pheromone-value calculation. Coefficient in penalty
        self.a = 1
        #Use in pheromone update. Use in delta-pheromone-value calculation. Coefficient in penalty
        self.b = 10
        #Initial pheromone-value on the edges
        self.pheromone0 = 1
        #Step in degraded ceiling algorithm
        self.localSearchStep = 0.0001
        #Good solution affinity
        self.affinity = 0.01
        #Amount of the ants
        self.antCounts = 50
        #ACO/DC algorithm maximum iteration
        self.maxIter = 300
        #Maximum iterations without changes in degraded ceiling algorithm
        self.dcMaxIterWithoutChange = 100


    def LoadFromXmlNode(self, node):
        AlgConfig.LoadFromXmlNode(self,node)
        try:
            self.pmax = int(node.getAttribute("pmax"))
            self.alpha1 = float(node.getAttribute("alpha1"))
            self.alpha2 = float(node.getAttribute("alpha2"))
            self.beta = float(node.getAttribute("beta"))
            self.ro = float(node.getAttribute("beta"))
            self.Q = float(node.getAttribute("Q"))
            self.a = int(node.getAttribute("a"))
            self.b = int(node.getAttribute("b"))
            self.pheromone0 = float(node.getAttribute("pheromone0"))
            self.localSearchStep = float(node.getAttribute("localSearchStep"))
            self.affinity = float(node.getAttribute("affinity"))
            self.antCounts = int(node.getAttribute("antCounts"))
            self.maxIter = int(node.getAttribute("maxIter"))
            self.dcMaxIterWithoutChange = int(node.getAttribute("dcMaxIterWithoutChange"))
        except Exception as e:
            print "Error in algorithm parameter"



