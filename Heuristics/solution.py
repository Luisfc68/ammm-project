from AMMMGlobals import AMMMException


# Solution includes functions to manage the solution, to perform feasibility
# checks and to dump the solution into a string or file.
class _Solution(object):
    def __init__(self):
        self.fitness = 0.0
        self.feasible = True
        self.verbose = False

    def setVerbose(self, verbose):
        if not isinstance(verbose, bool) or (verbose not in [True, False]):
            raise AMMMException('verbose(%s) has to be a boolean value.' % str(verbose))
        self.verbose = verbose

    def getFitness(self):
        return self.fitness

    def makeInfeasible(self):
        self.feasible = False
        self.fitness = float('inf')

    def isFeasible(self):
        return self.feasible

    def saveToFile(self, filePath):
        f = open(filePath, 'w')
        f.write(self.__str__())
        f.close()
