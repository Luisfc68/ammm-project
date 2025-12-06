from AMMMGlobals import AMMMException


# Validate instance attributes read from a DAT file.
# It validates the structure of the parameters read from the DAT file.
# It does not validate that the instance is feasible or not.
# Use Problem.checkInstance() function to validate the feasibility of the instance.
class ValidateInputData(object):
    @staticmethod
    def validate(data):
        # Validate that all input parameters were found
        for paramName in ['N', 'K', 'P', 'R', 'A', 'C', 'M']:
            if paramName not in data.__dict__:
                raise AMMMException('Parameter/Set(%s) not contained in Input Data' % str(paramName))


        nCameras = data.K
        if not isinstance(nCameras, int) or (nCameras <= 0):
            raise AMMMException('nCameras(%s) has to be a positive integer value.' % str(nCameras))


        nCrossings = data.N
        if not isinstance(nCrossings, int) or (nCrossings <= 0):
            raise AMMMException('nCrossings(%s) has to be a positive integer value.' % str(nCrossings))

        data.P = list(data.P)
        prices = data.P
        if len(prices) != nCameras:
            raise AMMMException('Size of prices(%d) does not match with value of nCameras(%d).' % (len(prices), nCameras))

        for value in prices:
            if not isinstance(value, int) or (value < 0):
                raise AMMMException('Invalid parameter value(%s) in prices. Should be a int greater or equal than zero.' % str(value))

        data.R = list(data.R)
        ranges = data.R
        if len(ranges) != nCameras:
            raise AMMMException(
                'Size of ranges(%d) does not match with value of nCameras(%d).' % (len(ranges), nCameras))

        for value in ranges:
            if not isinstance(value, int) or (value < 1) or (value > 49):
                raise AMMMException(
                    'Invalid parameter value(%s) in ranges. Should be a int in [1,49].' % str(value))

        data.A = list(data.A)
        autonomies = data.A
        if len(autonomies) != nCameras:
            raise AMMMException(
                'Size of autonomies(%d) does not match with value of nCameras(%d).' % (len(autonomies), nCameras))

        for value in autonomies:
            if not isinstance(value, int) or (value < 2) or (value > 6):
                raise AMMMException(
                    'Invalid parameter value(%s) in autonomies. Should be a int in [2, 6].' % str(value))

        data.C = list(data.C)
        consumptions = data.C
        if len(consumptions) != nCameras:
            raise AMMMException(
                'Size of consumptions(%d) does not match with value of nCameras(%d).' % (len(consumptions), nCameras))

        for value in consumptions:
            if not isinstance(value, int) or (value < 0):
                raise AMMMException(
                    'Invalid parameter value(%s) in consumptions. Should be a int greater or equal than zero.' % str(value))

        data.M = list(data.M)
        minRanges = data.M
        for i in range(len(minRanges)):
            minRanges[i] = list(minRanges[i])

        if len(minRanges) != nCrossings:
            raise AMMMException('Size of minRanges(%d) does not match with value of nCrossings(%d).' % (len(minRanges), nCrossings))

        for value in minRanges:
            if not(isinstance(value, list) and all(isinstance(x, int) for x in value)):
                raise AMMMException('Invalid parameter value(%s) in minRanges. Should be a list of integers.' % str(value))

