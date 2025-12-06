from Heuristics.problem.Camera import Camera
from Heuristics.problem.Crossing import Crossing
from Heuristics.problem.solution import Solution


class Instance(object):
    def __init__(self, config, inputData):
        self.config = config
        self.inputData = inputData
        nCameras = inputData.nCameras
        nCrossings = inputData.nCrossings
        prices = inputData.prices
        ranges = inputData.ranges
        autonomies = inputData.autonomies
        consumptions = inputData.consumptions
        minRanges = inputData.minRanges

        self.cameras = [None] * nCameras
        for i in range(0, nCameras):
            self.cameras[i] = Camera(i + 1, prices[i], ranges[i], autonomies[i], consumptions[i])

        self.crossings = [None] * nCrossings
        for i in range(0, nCrossings):
            self.crossings[i] = Crossing(i + 1, minRanges[i])


    def getNumCameras(self):
        return len(self.cameras)

    def getNumCrossings(self):
        return len(self.crossings)

    def getCameras(self):
        return self.cameras

    def getCrossings(self):
        return self.crossings

    def createSolution(self):
        solution = Solution(self.cameras, self.crossings)
        solution.setVerbose(self.config.verbose)
        return solution

    def checkInstance(self):
        # in the current specification, there's not condition that would make the problem unfeasible
        return True
