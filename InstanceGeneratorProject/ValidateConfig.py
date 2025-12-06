from AMMMGlobals import AMMMException


class ValidateConfig(object):
    # Validate config attributes read from a DAT file.

    @staticmethod
    def validate(data):
        # Validate that mandatory input parameters were found
        paramList = ['instancesDirectory', 'fileNamePrefix', 'fileNameExtension', 'numInstances',
                     'numCameras', 'minPrice', 'maxPrice', 'minRange', 'maxRange', 'minAutonomy', 'maxAutonomy', 'minPowerConsumption', 'maxPowerConsumption',
                     'numCrossings', 'minRangeRequirement', 'maxRangeRequirement']
        for paramName in paramList:
            if paramName not in data.__dict__:
                raise AMMMException('Parameter(%s) has not been not specified in Configuration' % str(paramName))

        instancesDirectory = data.instancesDirectory
        if len(instancesDirectory) == 0: raise AMMMException('Value for instancesDirectory is empty')

        fileNamePrefix = data.fileNamePrefix
        if len(fileNamePrefix) == 0: raise AMMMException('Value for fileNamePrefix is empty')

        fileNameExtension = data.fileNameExtension
        if len(fileNameExtension) == 0: raise AMMMException('Value for fileNameExtension is empty')

        numInstances = data.numInstances
        if not isinstance(numInstances, int) or (numInstances <= 0):
            raise AMMMException('numInstances(%s) has to be a positive integer value.' % str(numInstances))

        numCameras = data.numCameras
        if not isinstance(numCameras, int) or (numCameras <= 0):
            raise AMMMException('numCameras(%s) has to be a positive integer value.' % str(numCameras))

        minPrice = data.minPrice
        if not isinstance(minPrice, int) or (minPrice <= 0):
            raise AMMMException('minPrice(%s) has to be a positive integer value.' % str(minPrice))
        maxPrice = data.maxPrice
        if not isinstance(maxPrice, int) or (maxPrice <= 0):
            raise AMMMException('maxPrice(%s) has to be a positive integer value.' % str(maxPrice))
        if maxPrice < minPrice:
            raise AMMMException('maxPrice(%s) has to be >= minPrice(%s).' % (str(maxPrice), str(minPrice)))

        minRange = data.minRange
        if not isinstance(minRange, int) or (minRange <= 0):
            raise AMMMException('minRange(%s) has to be a positive integer value.' % str(minRange))
        maxRange = data.maxRange
        if not isinstance(maxRange, int) or (maxRange <= 0):
            raise AMMMException('maxRange(%s) has to be a positive integer value.' % str(maxRange))
        if maxRange < minRange:
            raise AMMMException('maxRange(%s) has to be >= minRange(%s).' % (str(maxRange), str(minRange)))

        minAutonomy = data.minAutonomy
        if not isinstance(minAutonomy, int) or (minAutonomy <= 0):
            raise AMMMException('minAutonomy(%s) has to be a positive integer value.' % str(minAutonomy))
        maxAutonomy = data.maxAutonomy
        if not isinstance(maxAutonomy, int) or (maxAutonomy <= 0):
            raise AMMMException('maxAutonomy(%s) has to be a positive integer value.' % str(maxAutonomy))
        if maxAutonomy < minAutonomy:
            raise AMMMException('maxAutonomy(%s) has to be >= minAutonomy(%s).' % (str(maxAutonomy), str(minAutonomy)))

        minPowerConsumption = data.minPowerConsumption
        if not isinstance(minAutonomy, int) or (minAutonomy <= 0):
            raise AMMMException('minPowerConsumption(%s) has to be a positive integer value.' % str(minPowerConsumption))
        maxPowerConsumption = data.maxPowerConsumption
        if not isinstance(maxPowerConsumption, int) or (maxPowerConsumption <= 0):
            raise AMMMException('maxPowerConsumption(%s) has to be a positive integer value.' % str(maxPowerConsumption))
        if maxPowerConsumption < minPowerConsumption:
            raise AMMMException('maxPowerConsumption(%s) has to be >= minPowerConsumption(%s).' % (str(maxPowerConsumption), str(minPowerConsumption)))

        numCrossings = data.numCrossings
        if not isinstance(numCrossings, int) or (numCrossings <= 0):
            raise AMMMException('numCrossings(%s) has to be a positive integer value.' % str(numCrossings))

        minRangeRequirement = data.minRangeRequirement
        if not isinstance(minRangeRequirement, int) or (minRangeRequirement <= 0):
            raise AMMMException('minRangeRequirement(%s) has to be a positive integer value.' % str(minRangeRequirement))
        maxRangeRequirement = data.maxRangeRequirement
        if not isinstance(maxRangeRequirement, int) or (maxRangeRequirement <= 0):
            raise AMMMException('maxRangeRequirement(%s) has to be a positive integer value.' % str(maxRangeRequirement))
        if maxRangeRequirement < minRangeRequirement:
            raise AMMMException('maxRangeRequirement(%s) has to be >= minRangeRequirement(%s).' % (str(maxRangeRequirement), str(minRangeRequirement)))
