import os
from AMMMGlobals import AMMMException


# Validate config attributes read from a DAT file.
class ValidateConfig(object):
    @staticmethod
    def validate(data):
        # Validate that mandatory input parameters were found
        for paramName in ['inputDataFile', 'solutionFile', 'solver']:
            if paramName not in data.__dict__:
                raise AMMMException('Parameter/Set(%s) not contained in Configuration' % str(paramName))

        # Validate input data file
        inputDataFile = data.inputDataFile
        if len(inputDataFile) == 0:
            raise AMMMException('Value for inputDataFile is empty')
        if not os.path.exists(inputDataFile) and not data.isMultiple:
            raise AMMMException('inputDataFile(%s) does not exist' % inputDataFile)

        # Validate solution file
        solutionFile = data.solutionFile
        if len(solutionFile) == 0:
            raise AMMMException('Value for solutionFile is empty')

        # Validate verbose
        verbose = False
        if 'verbose' in data.__dict__:
            verbose = data.verbose
            if not isinstance(verbose, bool) or (verbose not in [True, False]):
                raise AMMMException('verbose(%s) has to be a boolean value.' % str(verbose))
        else:
            data.verbose = verbose

        # Validate solver and per-solver parameters
        solver = data.solver
        if solver == 'Greedy' or solver == 'Random':
            # Validate that mandatory input parameters for Greedy solver were found
            pass
        elif solver == 'GRASP':
            # Validate that mandatory input parameters for GRASP solver were found
            for paramName in ['maxExecTime', 'alpha']:
                if not paramName in data.__dict__:
                    raise AMMMException('Parameter/Set(%s) not contained in Configuration. Required by GRASP solver.' % str(paramName))

            # Validate maxExecTime
            maxExecTime = data.maxExecTime
            if not isinstance(maxExecTime, (int, float)) or (maxExecTime <= 0):
                raise AMMMException('maxExecTime(%s) has to be a positive real value.' % str(maxExecTime))

            # Validate alpha
            alpha = data.alpha
            if not isinstance(alpha, (int, float)) or (alpha < 0) or (alpha > 1):
                raise AMMMException('alpha(%s) has to be a real value in range [0, 1].' % str(alpha))
        else:
            raise AMMMException('Unsupported solver specified(%s) in Configuration.' % str(solver))

        if data.localSearch:
            # Validate that mandatory input parameters for local search were found
            for paramName in ['neighborhoodStrategy', 'policy']:
                if paramName not in data.__dict__:
                    raise AMMMException('Parameter/Set(%s) not contained in Configuration. Required by Local Search.' % str(paramName))

            # Validate neighborhoodStrategy
            neighborhoodStrategy = data.neighborhoodStrategy
            if neighborhoodStrategy not in ['ModelExchange']:
                raise AMMMException('neighborhoodStrategy(%s) has to be one of [Reassignment, Exchange].' % str(neighborhoodStrategy))

            # Validate policy
            policy = data.policy
            if policy not in ['FirstImprovement', 'BestImprovement']:
                raise AMMMException('policy(%s) has to be one of [BestImprovement, FirstImprovement].' % str(policy))
