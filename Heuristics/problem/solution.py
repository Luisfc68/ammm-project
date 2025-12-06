import copy
from Heuristics.solution import _Solution
from Heuristics.problem.utils import computeCrossingDayPairs
from Heuristics.problem.constants import DAYS, SCHEDULES_PER_AUTONOMY

class Assignment(object):
    def __init__(self, camera, crossing, schedule, totalCost, coveredPairs):
        self.camera = camera
        self.crossing = crossing
        self.schedule = schedule
        self.totalCost = totalCost
        self.coveredPairs = coveredPairs

    def cost(self):
        return self.camera.getPrice() + sum(self.schedule) * self.camera.getPowerConsumption()

    def __str__(self):
        return "(camera {}, crossing {}, schedule {}) =  {} pairs, {} cost".format(self.camera.getModel(), self.crossing.getCrossingId(), self.schedule, self.coveredPairs, self.totalCost)

# Solution includes functions to manage the solution, to perform feasibility
# checks and to dump the solution into a string or file.
class Solution(_Solution):
    def __init__(self, cameraModels, crossings):
        self._assignments = [] # array of tuples (camera, crossing, schedule) that are covered
        self._coveredPairs = set()
        self._totalCost = 0
        self._pairs = computeCrossingDayPairs(len(crossings), DAYS)
        self._schedulesPerAutonomy = SCHEDULES_PER_AUTONOMY
        self._cameraModels = cameraModels
        self._crossings = crossings
        self._crossingToModel = {}
        super().__init__()

    def getCameras(self):
        return self._cameraModels

    def getUncoveredPairs(self):
        return len(self._pairs) - len(self._coveredPairs)

    def getUniverseSize(self):
        return len(self._pairs)

    def getAssignments(self):
        return copy.deepcopy(self._assignments)

    def getUncoveredPairsSet(self):
        return self._pairs.difference(self._coveredPairs)

    def getCoveredPairs(self):
        return self._coveredPairs

    def updateTotalCost(self):
        assignments = self._assignments
        self._totalCost = 0
        self.fitness = 0
        for assignment in assignments:
            camera = assignment[0]
            totalDays = sum(assignment[2])
            cost = camera.getPrice() + totalDays * camera.getPowerConsumption()
            self._totalCost += cost
        self.fitness = self._totalCost

    def updateCoveredPairs(self):
        assignments = self._assignments
        self._coveredPairs = set()
        for assignment in assignments:
            pairs = set()
            cameraRange = assignment[0].getRange()
            ranges = assignment[1].getRequiredRanges()
            daysOn = [i + 1 for i, value in enumerate(assignment[2]) if value == 1]

            visibleCrossings = [
                index + 1 for index, value in enumerate(ranges) if value <= cameraRange
            ]

            for d in daysOn:
                for c in visibleCrossings:
                    pairs.add((c, d))
            self._coveredPairs.update(pairs)

    def assign(self, camera, crossing, schedule):
        if not self.isFeasibleToAssignCameraToCrossing(crossing): return False
        self._assignments.append((camera, crossing, schedule))
        self._crossingToModel[crossing.getCrossingId()] = camera.getModel()
        self.updateTotalCost()
        self.updateCoveredPairs()
        return True

    def unassign(self, camera, crossing, schedule):
        if not self.isFeasibleToUnassignCameraToCrossing(crossing): return False
        self._assignments = [a for a in self._assignments if not(a[0].getModel() == camera.getModel() and a[1].getCrossingId() == crossing.getCrossingId() and a[2] == schedule)]
        del self._crossingToModel[crossing.getCrossingId()]
        self.updateTotalCost()
        self.updateCoveredPairs()
        return True

    def findFeasibleAssignments(self, camera, crossing):
        feasibleAssignments = []
        schedules = self._schedulesPerAutonomy[camera.getAutonomy()]
        for schedule in schedules:
            feasible = self.assign(camera, crossing, schedule)
            if not feasible: continue
            assignment = Assignment(camera, crossing, schedule, self._totalCost, self._coveredPairs)
            feasibleAssignments.append(assignment)

            self.unassign(camera, crossing, schedule)

        return feasibleAssignments

    def createAssignmentSnapshot(self, camera, crossing, schedule):
        feasible = self.assign(camera, crossing, schedule)
        if not feasible: return None
        assignment = Assignment(camera, crossing, schedule, self._totalCost, self._coveredPairs)
        self.unassign(camera, crossing, schedule)
        return assignment

    def isFeasibleToAssignCameraToCrossing(self, crossing):
        if crossing.getCrossingId() in self._crossingToModel: return False
        return True

    def isFeasibleToUnassignCameraToCrossing(self, crossing):
        if crossing.getCrossingId() not in self._crossingToModel: return False
        return True

    def __str__(self):
        strSolution = 'cost = {};\n'.format(self.fitness)
        if self.fitness == float('inf'): return strSolution

        # assignments: [(camera, crossing, schedule)]
        strSolution += 'assignments = [\n'
        for a in self._assignments:
            strSolution += '\t('+ str(a[0].getModel()) + ', ' + str(a[1].getCrossingId()) + ', ' + str(a[2]) + '),\n'
        strSolution += '];\n'

        return strSolution

    def saveToFile(self, filePath):
        f = open(filePath, 'w')
        f.write(self.__str__())
        f.close()
