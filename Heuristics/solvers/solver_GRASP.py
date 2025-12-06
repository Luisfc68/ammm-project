import random
import time
from Heuristics.solver import _Solver
from Heuristics.solvers.localSearch import LocalSearch


# Inherits from the parent abstract solver.
class Solver_GRASP(_Solver):

    def _selectCandidate(self, candidateList, alpha):

        # sort candidate assignments by highestLoad in ascending order
        sortedCandidateList = sorted(candidateList, key=lambda x: x.highestLoad)
        
        # compute boundary highest load as a function of the minimum and maximum highest loads and the alpha parameter
        minHLoad = sortedCandidateList[0].highestLoad
        maxHLoad = sortedCandidateList[-1].highestLoad
        boundaryHLoad = minHLoad + (maxHLoad - minHLoad) * alpha
        
        # find elements that fall into the RCL
        maxIndex = 0
        for candidate in sortedCandidateList:
            if candidate.highestLoad <= boundaryHLoad:
                maxIndex += 1

        # create RCL and pick an element randomly
        rcl = sortedCandidateList[0:maxIndex]          # pick first maxIndex elements starting from element 0
        if not rcl: return None
        return random.choice(rcl)          # pick a candidate from rcl at random
    
    def _greedyRandomizedConstruction(self, alpha):
        # get an empty solution for the problem
        solution = self.instance.createSolution()
        
        # get tasks and sort them by their total required resources in descending order
        tasks = self.instance.getTasks()
        sortedTasks = sorted(tasks, key=lambda t: t.getTotalResources(), reverse=True)


        # for each task taken in sorted order
        for task in sortedTasks:
            taskId = task.getId()
            
            # compute feasible assignments
            candidateList = solution.findFeasibleAssignments(taskId)

            # no candidate assignments => no feasible assignment found
            if not candidateList:
                solution.makeInfeasible()
                break
            
            # select an assignment
            candidate = self._selectCandidate(candidateList, alpha)

            # assign the current task to the CPU that resulted in a minimum highest load
            solution.assign(taskId, candidate.cpuId)
            
        return solution
    
    def stopCriteria(self):
        self.elapsedEvalTime = time.time() - self.startTime
        return time.time() - self.startTime > self.config.maxExecTime

    def solve(self, **kwargs):
        self.startTimeMeasure()
        incumbent = self.instance.createSolution()
        incumbent.makeInfeasible()
        bestHighestLoad = incumbent.getFitness()
        self.writeLogLine(bestHighestLoad, 0)

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
                solutionHighestLoad = solution.getFitness()
                if solutionHighestLoad < bestHighestLoad :
                    incumbent = solution
                    bestHighestLoad = solutionHighestLoad
                    self.writeLogLine(bestHighestLoad, iteration)

        self.writeLogLine(bestHighestLoad, iteration)
        self.numSolutionsConstructed = iteration
        self.printPerformance()
        return incumbent

