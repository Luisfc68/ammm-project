import os, random
from AMMMGlobals import AMMMException


class InstanceGenerator(object):
    # Generate instances based on read configuration.

    def __init__(self, config):
        self.config = config

    def generate(self):
        instancesDirectory = self.config.instancesDirectory
        fileNamePrefix = self.config.fileNamePrefix
        fileNameExtension = self.config.fileNameExtension
        numInstances = self.config.numInstances

        numCameras = self.config.numCameras
        minPrice = self.config.minPrice
        maxPrice = self.config.maxPrice
        minRange = self.config.minRange
        maxRange = self.config.maxRange
        minAutonomy = self.config.minAutonomy
        maxAutonomy = self.config.maxAutonomy
        minPowerConsumption = self.config.minPowerConsumption
        maxPowerConsumption = self.config.maxPowerConsumption

        numCrossings = self.config.numCrossings
        minRangeRequirement = self.config.minRangeRequirement
        maxRangeRequirement = self.config.maxRangeRequirement

        if not os.path.isdir(instancesDirectory):
            raise AMMMException('Directory(%s) does not exist' % instancesDirectory)

        for i in range(numInstances):
            instancePath = os.path.join(instancesDirectory, '%s_%d.%s' % (fileNamePrefix, i, fileNameExtension))
            fInstance = open(instancePath, 'w')

            prices = [0] * numCameras
            ranges = [0] * numCameras
            autonomies = [0] * numCameras
            powerConsumptions = [0] * numCameras
            for c in range(numCameras):
                prices[c] = random.randint(minPrice, maxPrice)
                ranges[c] = random.randint(minRange, maxRange)
                autonomies[c] = random.randint(minAutonomy, maxAutonomy)
                powerConsumptions[c] = random.randint(minPowerConsumption, maxPowerConsumption)


            rangeRequirements = [[0] * numCrossings for _ in range(numCrossings)]
            for i in range(numCrossings):
                for j in range(i, numCrossings):
                    if i == j:
                        rangeRequirements[i][j] = 0
                    else:
                        value = random.randint(minRangeRequirement, maxRangeRequirement)
                        rangeRequirements[i][j] = value
                        rangeRequirements[j][i] = value

            fInstance.write('K=%d;\n' % numCameras)
            fInstance.write('N=%d;\n' % numCrossings)

            # translate vector of ints into vector of strings and concatenate that strings separating them by a single space character
            fInstance.write('P=[%s];\n' % (' '.join(map(str, prices))))
            fInstance.write('R=[%s];\n' % (' '.join(map(str, ranges))))
            fInstance.write('A=[%s];\n' % (' '.join(map(str, autonomies))))
            fInstance.write('C=[%s];\n' % (' '.join(map(str, powerConsumptions))))

            fInstance.write('M=[\n')
            for i in range(numCrossings):
                fInstance.write('\t[%s]\n' % (' '.join(map(str, rangeRequirements[i]))))
            fInstance.write('];')

            fInstance.close()
