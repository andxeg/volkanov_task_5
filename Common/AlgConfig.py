class AlgConfig:
    '''Algorithm settings.
    '''
    def __init__(self):
        self.use_metamodel = False
        #Max number of attempts to generate random solution
        self.maxGenIter = 10
        self.metamodel = None

    def LoadFromXmlNode(self, node):
        '''Loading from xml-node with tag 'alg'.
        Should be reimplemented in subclass
        :param node: <alg> node in xml-file'''
        pass
