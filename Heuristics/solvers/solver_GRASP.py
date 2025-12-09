import random
import time
from Heuristics.solver import _Solver
from Heuristics.solvers.localSearch import LocalSearch


# Inherits from the parent abstract solver.
class Solver_GRASP(_Solver):

    def _selectCandidate(self, candidateList, alpha):

        # sort candidate assignments by covered pairs and use cost if is a tie
        sortedCandidateList = sorted(candidateList, key=lambda x: (-len(x.coveredPairs), x.cost()))
        
        # our quality metric is number of covered pairs
        minPairs = len(sortedCandidateList[0].coveredPairs)
        maxPairs = len(sortedCandidateList[-1].coveredPairs)
        boundaryCoveredPairs = minPairs + (maxPairs - minPairs) * alpha
        
        # find elements that fall into the RCL
        maxIndex = 0
        for candidate in sortedCandidateList:
            if len(candidate.coveredPairs) <= boundaryCoveredPairs:
                maxIndex += 1

        # create RCL and pick an element randomly
        rcl = sortedCandidateList[0:maxIndex]          # pick first maxIndex elements starting from element 0
        if not rcl: return None
        return random.choice(rcl)          # pick a candidate from rcl at random

    def _greedyRandomizedConstruction(self, alpha):
        # get an empty solution for the problem
        solution = self.instance.createSolution()

        crossings = self.instance.getCrossings()
        cameras = self.instance.getCameras()
        sortedCrossings = sorted(crossings, key=lambda cr: sum(cr.getRequiredRanges()))

        while solution.getUncoveredPairs() > 0:
            for crossing in sortedCrossings:
                candidateList = []
                for camera in cameras:
                    newCandidates = solution.findFeasibleAssignments(camera, crossing)
                    if not newCandidates: continue
                    candidateList.extend(newCandidates)
                if not candidateList: continue
                candidate = self._selectCandidate(candidateList, alpha)
                solution.assign(candidate.camera, candidate.crossing, candidate.schedule)
                if solution.getUncoveredPairs() == 0: return solution
            if solution.getUncoveredPairs() > 0:
                solution.makeInfeasible()
                return solution
        return solution

    def stopCriteria(self):
        self.elapsedEvalTime = time.time() - self.startTime
        return time.time() - self.startTime > self.config.maxExecTime

    def solve(self, **kwargs):
        self.startTimeMeasure()
        incumbent = self.instance.createSolution()
        incumbent.makeInfeasible()
        bestTotalCost = incumbent.getFitness()
        self.writeLogLine(bestTotalCost, 0)

        iteration = 0
        while not self.stopCriteria():
            iteration += 1
            
            # force first iteration as a Greedy execution (alpha == 0)
            alpha = 0 if iteration == 1 else self.config.alpha

            solution = self._greedyRandomizedConstruction(alpha)
            if self.config.localSearch:
                localSearch = LocalSearch(self.config, None)
                endTime = self.startTime + self.config.maxExecTime
                solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)

            if solution.isFeasible():
                solutionTotalCost = solution.getFitness()
                if solutionTotalCost < bestTotalCost:
                    incumbent = solution
                    bestTotalCost = solutionTotalCost
                    self.writeLogLine(bestTotalCost, iteration)

        self.writeLogLine(bestTotalCost, iteration)
        self.numSolutionsConstructed = iteration
        self.printPerformance()
        return incumbent

