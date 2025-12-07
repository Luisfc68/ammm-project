import sys
import os
import json
from Heuristics.datParser import DATParser
from AMMMGlobals import AMMMException
from InstanceGeneratorProject.ValidateConfig import ValidateConfig
from InstanceGeneratorProject.InstanceGenerator import InstanceGenerator

def load_config(config_file="config.json"):
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file not found: {config_file}")
    with open(config_file, 'r') as f:
        return json.load(f)

def run():
    try:
        configFile = "config/config.dat"
        confNew = load_config("config/config.json")
        print("AMMM Instance Generator")
        print("-----------------------")
        print("Reading Config file %s..." % configFile)
        config = DATParser.parse(configFile)
        ValidateConfig.validate(config)
        print("Creating Instances...")
        instGen = InstanceGenerator(config, confNew)
        instGen.generate()
        print("Done")
        return 0
    except AMMMException as e:
        print("Exception: %s", e)
        return 1

if __name__ == '__main__':
    sys.exit(run())
