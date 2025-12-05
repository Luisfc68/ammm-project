import copy
import time
from Heuristics.problem.constants import SCHEDULES_PER_AUTONOMY
from Heuristics.solver import _Solver
from AMMMGlobals import AMMMException

# Implementation of a local search using two neighborhoods and two different policies.
class LocalSearch(_Solver):
    def __init__(self, config, instance):
        self.enabled = config.localSearch
        self.nhStrategy = config.neighborhoodStrategy
        self.policy = config.policy
        self.maxExecTime = config.maxExecTime
        super().__init__(config, instance)

    def getAssignmentsSortedByCost(self, solution):
        return sorted(solution.getAssignments(), key=lambda x: x[0].getCostForSchedule(x[2]), reverse=True)

    def createModelExchange(self, solution, originalFitness, crossing, newCamera, newSchedule):
        newCost = newCamera.getCostForSchedule(newSchedule)
        if newCost >= originalFitness: return None
        newAssignment = solution.createAssignmentSnapshot(newCamera, crossing, newSchedule)
        if newAssignment is not None and len(newAssignment.coveredPairs) == solution.getUniverseSize() and newAssignment.totalCost < originalFitness:
            return newAssignment
        return None

    def exploreModelExchange(self, solution):
        currentTotalCost = solution.getFitness()
        bestNeighbor = copy.deepcopy(solution)

        sortedAssignments = self.getAssignmentsSortedByCost(solution)
        for i in range(len(sortedAssignments)):
            assignment = sortedAssignments[i]
            assignmentCamera = assignment[0]
            assignmentCrossing = assignment[1]
            assignmentSchedule = assignment[2]
            unusedCameras = [camera for camera in solution.getCameras() if camera.getModel() != assignmentCamera.getModel()]
            solution.unassign(assignmentCamera, assignmentCrossing, assignmentSchedule)
            for newCamera in unusedCameras:
                for newSchedule in SCHEDULES_PER_AUTONOMY[newCamera.getAutonomy()]:
                    betterAssignment = self.createModelExchange(solution, currentTotalCost, assignmentCrossing, newCamera, newSchedule)
                    if betterAssignment is not None and self.policy == 'FirstImprovement':
                        solution.assign(betterAssignment.camera, betterAssignment.crossing, betterAssignment.schedule)
                        return solution
                    elif betterAssignment is not None and bestNeighbor.getFitness() > betterAssignment.totalCost:
                        solution.assign(betterAssignment.camera, betterAssignment.crossing, betterAssignment.schedule)
                        bestNeighbor = copy.deepcopy(solution)
                        solution.unassign(betterAssignment.camera, betterAssignment.crossing, betterAssignment.schedule)
            solution.assign(assignmentCamera, assignmentCrossing, assignmentSchedule)
        return bestNeighbor

    def exploreNeighborhood(self, solution):
        if self.nhStrategy == 'ModelExchange': return self.exploreModelExchange(solution)
        else: raise AMMMException('Unsupported NeighborhoodStrategy(%s)' % self.nhStrategy)

    def solve(self, **kwargs):
        initialSolution = kwargs.get('solution', None)
        if initialSolution is None:
            raise AMMMException('[local search] No solution could be retrieved')

        if not initialSolution.isFeasible(): return initialSolution
        self.startTime = kwargs.get('startTime', None)
        endTime = kwargs.get('endTime', None)

        incumbent = initialSolution
        incumbentFitness = incumbent.getFitness()
        iterations = 0

        # keep iterating while improvements are found
        while time.time() < endTime:
            iterations += 1
            neighbor = self.exploreNeighborhood(incumbent)
            if neighbor is None: break
            neighborFitness = neighbor.getFitness()
            if incumbentFitness <= neighborFitness: break
            incumbent = neighbor
            incumbentFitness = neighborFitness

        return incumbent
