'''
AMMM Lab Heuristics
Greedy solver
Copyright 2020 Luis Velasco.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

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
        sortedCameras = sorted(cameras, key=lambda c: c.getPrice())

        while solution.getUncoveredPairs() > 0:
            for crossing in crossings:
                for camera in sortedCameras:
                    # compute feasible assignments
                    print(solution.getUncoveredPairsSet())
                    candidateList = solution.findFeasibleAssignments(camera, crossing)
                    if not candidateList: continue
                    # select assignment
                    candidate = self._selectCandidate(candidateList)
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


