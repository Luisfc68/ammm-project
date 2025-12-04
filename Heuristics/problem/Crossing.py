class Crossing(object):
    def __init__(self, crossingId, requiredRanges):
        self._crossingId = crossingId
        self._requiredRanges = requiredRanges

    def getCrossingId(self):
        return self._crossingId

    def getRequiredRanges(self):
        return self._requiredRanges

    def __str__(self):
        return "crossingId: %d (requiredRanges: %f)".format(self._crossingId, self._requiredRanges)
