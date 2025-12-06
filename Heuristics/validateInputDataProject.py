from AMMMGlobals import AMMMException


# Validate instance attributes read from a DAT file.
# It validates the structure of the parameters read from the DAT file.
# It does not validate that the instance is feasible or not.
# Use Problem.checkInstance() function to validate the feasibility of the instance.
class ValidateInputData(object):
    @staticmethod
    def validate(data):
        # Validate that all input parameters were found
        for paramName in ['nCameras', 'nCrossings', 'prices', 'ranges', 'autonomies', 'consumptions', 'minRanges']:
            if paramName not in data.__dict__:
                raise AMMMException('Parameter/Set(%s) not contained in Input Data' % str(paramName))


        nCameras = data.nCameras
        if not isinstance(nCameras, int) or (nCameras <= 0):
            raise AMMMException('nCameras(%s) has to be a positive integer value.' % str(nCameras))


        nCrossings = data.nCrossings
        if not isinstance(nCrossings, int) or (nCrossings <= 0):
            raise AMMMException('nCrossings(%s) has to be a positive integer value.' % str(nCrossings))

        data.prices = list(data.prices)
        prices = data.prices
        if len(prices) != nCameras:
            raise AMMMException('Size of prices(%d) does not match with value of nCameras(%d).' % (len(prices), nCameras))

        for value in prices:
            if not isinstance(value, int) or (value < 0):
                raise AMMMException('Invalid parameter value(%s) in prices. Should be a int greater or equal than zero.' % str(value))

        data.ranges = list(data.ranges)
        ranges = data.ranges
        if len(ranges) != nCameras:
            raise AMMMException(
                'Size of ranges(%d) does not match with value of nCameras(%d).' % (len(ranges), nCameras))

        for value in ranges:
            if not isinstance(value, int) or (value < 1) or (value > 49):
                raise AMMMException(
                    'Invalid parameter value(%s) in ranges. Should be a int in [1,49].' % str(value))

        data.autonomies = list(data.autonomies)
        autonomies = data.autonomies
        if len(autonomies) != nCameras:
            raise AMMMException(
                'Size of autonomies(%d) does not match with value of nCameras(%d).' % (len(autonomies), nCameras))

        for value in autonomies:
            if not isinstance(value, int) or (value < 2) or (value > 6):
                raise AMMMException(
                    'Invalid parameter value(%s) in autonomies. Should be a int in [2, 6].' % str(value))

        data.consumptions = list(data.consumptions)
        consumptions = data.consumptions
        if len(consumptions) != nCameras:
            raise AMMMException(
                'Size of consumptions(%d) does not match with value of nCameras(%d).' % (len(consumptions), nCameras))

        for value in consumptions:
            if not isinstance(value, int) or (value < 0):
                raise AMMMException(
                    'Invalid parameter value(%s) in consumptions. Should be a int greater or equal than zero.' % str(value))

        data.minRanges = list(data.minRanges)
        minRanges = data.minRanges
        for i in range(len(minRanges)):
            minRanges[i] = list(minRanges[i])

        if len(minRanges) != nCrossings:
            raise AMMMException('Size of minRanges(%d) does not match with value of nCrossings(%d).' % (len(minRanges), nCrossings))

        for value in minRanges:
            if not(isinstance(value, list) and all(isinstance(x, int) for x in value)):
                raise AMMMException('Invalid parameter value(%s) in minRanges. Should be a list of integers.' % str(value))

