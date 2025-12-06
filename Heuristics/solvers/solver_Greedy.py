import random, time
from Heuristics.solver import _Solver
from Heuristics.solvers.localSearch import LocalSearch


# Inherits from the parent abstract solver.
class Solver_Greedy(_Solver):

    def _selectCandidate(self, candidateList):
        if self.config.solver == 'Greedy':
            sortedCandidateList = sorted(candidateList, key=lambda x: (-len(x.coveredPairs), x.cost()))
            # choose the cheapest candidate that covers more paris
            return sortedCandidateList[0]
        return random.choice(candidateList)

    def construction(self):
        # get an empty solution for the problem
        solution = self.instance.createSolution()

        crossings = self.instance.getCrossings()
        cameras = self.instance.getCameras()
        sortedCrossings = sorted(crossings, key=lambda cr: sum(cr.getRequiredRanges()))

        while solution.getUncoveredPairs() > 0:
            for crossing in sortedCrossings:
                candidateList = []
                for camera in cameras:
                    # compute feasible assignments
                    # print(solution.getUncoveredPairsSet())
                    newCandidates = solution.findFeasibleAssignments(camera, crossing)
                    if not newCandidates: continue
                    candidateList.extend(newCandidates)
                    # select assignment
                if not candidateList:
                    solution.makeInfeasible()
                    return solution
                candidate = self._selectCandidate(candidateList)
                if len(candidate.coveredPairs) > len(solution.getCoveredPairs()):
                    solution.assign(candidate.camera, candidate.crossing, candidate.schedule)
                if solution.getUncoveredPairs() == 0: return solution
        return solution

    def solve(self, **kwargs):
        self.startTimeMeasure()

        solver = kwargs.get('solver', None)
        if solver is not None:
            self.config.solver = solver
        localSearch = kwargs.get('localSearch', None)
        if localSearch is not None:
            self.config.localSearch = localSearch

        self.writeLogLine(float('inf'), 0)

        solution = self.construction()
        if self.config.localSearch:
            localSearch = LocalSearch(self.config, None)
            endTime= self.startTime + self.config.maxExecTime
            solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)

        self.elapsedEvalTime = time.time() - self.startTime
        self.writeLogLine(solution.getFitness(), 1)
        self.numSolutionsConstructed = 1
        self.printPerformance()

        return solution


