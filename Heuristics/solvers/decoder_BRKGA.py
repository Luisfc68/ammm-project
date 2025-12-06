from AMMMGlobals import AMMMException
from Heuristics.BRKGA_fwk.decoder import _Decoder

class Decoder(_Decoder):
    def __init__(self, config, instance):
        config.__dict__['numGenes'] = int(instance.getNumTasks())
        config.__dict__['numIndividuals'] = int(config.IndividualsMultiplier * config.numGenes)
        config.__dict__['numElite'] = int(config.eliteProp * config.numIndividuals)
        config.__dict__['numMutants'] = int(config.mutantProp * config.numIndividuals)
        config.__dict__['numCrossover'] = int(config.numIndividuals - config.numElite - config.numMutants)
        super().__init__(config, instance)

    def selectCandidate(self, candidateList):
        if not candidateList: return None

        # sort candidate assignments by highestLoad in ascending order
        sortedCandidateList = sorted(candidateList, key=lambda x: x.highestLoad)

        # choose assignment with minimum highest load
        return sortedCandidateList[0]

    def decodeIndividual(self, chromosome):

        if len(chromosome) != self.instance.getNumTasks():
            raise AMMMException("Error: the length of the chromosome does not fits the number of tasks")

        # get an empty solution for the problem
        solution = self.instance.createSolution()

        # get tasks and sort them by their total required resources in descending order
        tasks = self.instance.getTasks()
        for tId in range(len(tasks)):
            tasks[tId].gene = chromosome[tId]
        sortedTasks = sorted(tasks, key=lambda t: t.getWeightedResources(), reverse=True)

        # for each task taken in sorted order
        for task in sortedTasks:
            taskId = task.getId()

            # compute feasible assignments
            candidateList = solution.findFeasibleAssignments(taskId)

            # no candidate assignments => no feasible assignment found
            if not candidateList:
                solution.makeInfeasible()
                break

            # select the best assignment
            bestCandidate = self.selectCandidate(candidateList)

            # assign the current task to the CPU that resulted in a minimum highest load
            solution.assign(task.getId(), bestCandidate.cpuId)

        return solution, solution.getFitness()