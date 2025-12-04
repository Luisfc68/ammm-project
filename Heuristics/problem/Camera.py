class Camera(object):
    def __init__(self, model, price, range, autonomy, powerConsumption):
        self._model = model
        self._price = price
        self._range = range
        self._autonomy = autonomy
        self._powerConsumption = powerConsumption

    def getModel(self):
        return self._model

    def getPrice(self):
        return self._price

    def getRange(self):
        return self._range

    def getAutonomy(self):
        return self._autonomy

    def getPowerConsumption(self):
        return self._powerConsumption

    def __str__(self):
        return "camera model: %d (price: %d, range: %d, autonomy: %d, power consumption: %d)" % (self._model, self._price, self._range, self._autonomy, self._powerConsumption)
