from argparse import ArgumentParser
from pathlib import Path

import sys
import os

from Heuristics.datParser import DATParser
from AMMMGlobals import AMMMException
from Heuristics.validateInputDataProject import ValidateInputData
from Heuristics.ValidateConfig import ValidateConfig
from Heuristics.solvers.solver_Greedy import Solver_Greedy
from Heuristics.solvers.solver_GRASP import Solver_GRASP
from Heuristics.problem.instance import Instance


class Main:
    def __init__(self, config):
        self.config = config

    def run(self, data):
        try:
            if self.config.verbose: print('Creating Problem Instance...')
            instance = Instance(self.config, data)
            if self.config.verbose: print('Solving the Problem...')
            if instance.checkInstance():
                initialSolution = None
                if self.config.solver == 'Greedy' or self.config.solver == 'Random':
                    solver = Solver_Greedy(self.config, instance)
                elif self.config.solver == 'GRASP':
                    solver = Solver_GRASP(self.config, instance)
                else:
                    raise AMMMException('Solver %s not supported.' % str(self.config.solver))
                solution = solver.solve(solution=initialSolution)
                #print('Solution (CPUid: [TasksId]): %s' % str(solution.cpuIdToListTaskId))
                solution.saveToFile(self.config.solutionFile)
            else:
                print('Instance is infeasible.')
                solution = instance.createSolution()
                solution.makeInfeasible()
                solution.saveToFile(self.config.solutionFile)
            return 0
        except AMMMException as e:
            print('Exception:', e)
            return 1

def runSingleMode(args):
    config = DATParser.parse(args.configFile)
    config.isMultiple = args.multiple
    ValidateConfig.validate(config)
    inputData = DATParser.parse(config.inputDataFile)
    ValidateInputData.validate(inputData)

    if config.verbose:
        print('AMMM Lab Heuristics')
        print('-------------------')
        print('Config file %s' % args.configFile)
        print('Input Data file %s' % config.inputDataFile)

    main = Main(config)
    sys.exit(main.run(inputData))

def runMultipleMode(args):
    config = DATParser.parse(args.configFile)
    config.isMultiple = args.multiple
    ValidateConfig.validate(config)
    files = os.listdir(config.inputDataDir)
    solutionFile = config.solutionFile

    for i in range(len(files)):
        instanceInput = os.path.join(config.inputDataDir, files[i])
        solutionFileParsed = Path(solutionFile)
        instanceSolution = str(solutionFileParsed.with_stem(solutionFileParsed.stem+'_'+str(i)))
        inputData = DATParser.parse(instanceInput)
        ValidateInputData.validate(inputData)

        if config.verbose:
            print('AMMM Lab Heuristics')
            print('-------------------')
            print('Config file %s' % args.configFile)
            print('Input Data file %s' % instanceInput)
            print('Solution File %s' % instanceSolution)

        config.solutionFile = instanceSolution
        main = Main(config)
        errorCode = main.run(inputData)
        if errorCode != 0: sys.exit(errorCode)

if __name__ == '__main__':
    parser = ArgumentParser(description='AMMM Lab Heuristics')
    parser.add_argument('-c', '--configFile', nargs='?', type=Path,
                        default=Path(__file__).parent / 'config/config.dat', help='specifies the config file')
    parser.add_argument('-m', '--multiple', action="store_true")
    args = parser.parse_args()

    if args.multiple:
        print("Running in multiple mode...")
        runMultipleMode(args)
    else:
        print("Running in single mode...")
        runSingleMode(args)
