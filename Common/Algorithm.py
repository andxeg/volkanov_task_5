from Common.Statistics import Statistics
class Algorithm:
    '''Base Algoritm Class.
    '''
    algconf = None
    timecounts = 0
    simcounts = 0
    time = None
    result_filename = "result.csv"

    def __init__(self):
        self.currentSolution = None
        self.currentIter = 0
        self.stat = Statistics()

    def Run(self):
        '''Runs algorithm. Should be reimplemented.'''
        print "Should be reimplemented"

    def Step(self):
        '''Makes one algorithm step. Should be reimplemented.
        '''
        print "Should be reimplemented"

    def Clear(self):
        '''
        Clears some class fields.
        Necessary for multiple experiments
        It's likely to be reimplemented'''
        self.currentSolution = None
        self.currentIter = 0
        self.timecounts = 0
        self.simcounts = 0
        self.time = None

    def PrintStats(self):
        '''Prints statistics to csv-file.
        Can be reimplemented'''
        self.stat.ExportToCsv(Algorithm.result_filename)