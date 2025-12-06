class _Decoder(object):
    def __init__(self, config, instance):
        self.config = config
        self.instance = instance

    def decode(self, generation):
        numDecoded = 0
        bestInGeneration = {'chr':None, 'solution':None, 'fitness':float('inf')}
        for individual in generation:
            numDecoded += 1
            if individual['fitness'] is None:
                solution, fitness = self.decodeIndividual(individual['chr'])
                individual['solution'] = solution
                individual['fitness'] = fitness
            if individual['fitness'] < bestInGeneration['fitness']:
                bestInGeneration = individual
        return bestInGeneration, numDecoded

    def getConfiguration(self):
        return self.config

    def decodeIndividual(self, chromosome):
        raise NotImplementedError