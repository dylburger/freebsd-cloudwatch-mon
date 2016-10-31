""" Classes and methods to handle config data
"""
from __future__ import print_function
import yaml

CONFIG_FILE = "config.yml"


class YAMLParser(object):
    """ Class to read in and retrieve the data
        found in YAML files
    """
    def __init__(self, FILE):
        with open(FILE, 'r') as f:
            try:
                config = yaml.load(f)
            except yaml.YAMLError as exc:
                print("Your config file appears to contain invalid YAML: ",
                       exc)
            else:
                self.config = config
