import os, random, math
from AMMMGlobals import AMMMException


class InstanceGenerator(object):
    # Generate instances based on read configuration.

    def __init__(self, config, conf):
        self.config = config
        self.conf   = conf

    def generate(self):
        instancesDirectory = self.config.instancesDirectory
        fileNamePrefix = self.config.fileNamePrefix
        fileNameExtension = self.config.fileNameExtension
        numInstances = self.config.numInstances

        numCameras = self.config.numCameras
        numCrossings = self.config.numCrossings

        map_cfg = self.conf["map_settings"]
        mkt_cfg = self.conf["market_settings"]
        profiles = self.conf["profiles"]
        profile_names = list(profiles.keys())

        grid_side = int(math.sqrt(numCrossings * map_cfg["density_factor"]))

        if not os.path.isdir(instancesDirectory):
            raise AMMMException('Directory(%s) does not exist' % instancesDirectory)

        for i in range(numInstances):
            coords = [(random.uniform(0, grid_side), random.uniform(0, grid_side)) for _ in range(numCrossings)]
            instancePath = os.path.join(instancesDirectory, '%s_%d.%s' % (fileNamePrefix, i, fileNameExtension))
            fInstance = open(instancePath, 'w')

            prices = [0] * numCameras
            ranges = [0] * numCameras
            autonomies = [0] * numCameras
            powerConsumptions = [0] * numCameras

            for c in range(numCameras):
                manufacturer = random.choices(
                    profile_names,
                    weights=mkt_cfg["share_weights"]
                )[0]

                specs = profiles[manufacturer]
                ranges[c] = random.randint(*specs["range"])
                autonomies[c] = random.randint(*specs["autonomy"])
                powerConsumptions[c] = int(ranges[c] * random.uniform(*specs["consumption_factor"]))

                prices[c] = specs["base_price"] + \
                        (ranges[c] * specs["mult_range"]) + \
                        (autonomies[c] * specs["mult_autonomy"])

                noise = random.uniform(*mkt_cfg["price_noise"])
                prices[c] = int(prices[c] * noise)
                prices[c] = max(mkt_cfg["price_floor"], prices[c])

            rangeRequirements = [[0] * numCrossings for _ in range(numCrossings)]
            cutoff = map_cfg["visibility_cutoff"]

            for i in range(numCrossings):
                for j in range(numCrossings):
                    if i == j: continue

                    xi, yi = coords[i]
                    xj, yj = coords[j]
                    dist = math.sqrt((xi - xj)**2 + (yi - yj)**2)
                    val = int(round(dist))

                    rangeRequirements[i][j] = cutoff if val > cutoff else val

            fInstance.write('K=%d;\n' % numCameras)
            fInstance.write('N=%d;\n' % numCrossings)

            # translate vector of ints into vector of strings and concatenate that strings separating them by a single space character
            fInstance.write('P=[%s];\n' % (' '.join(map(str, prices))))
            fInstance.write('R=[%s];\n' % (' '.join(map(str, ranges))))
            fInstance.write('A=[%s];\n' % (' '.join(map(str, autonomies))))
            fInstance.write('C=[%s];\n' % (' '.join(map(str, powerConsumptions))))

            fInstance.write('M=[\n')
            for i in rangeRequirements:
                fInstance.write("  " + str(i).replace(',', '') + "\n")
            fInstance.write('];')

            fInstance.close()
