# test_yaml_read.py
from utils.common_functions import read_yaml

config = read_yaml("config/config.yaml")
print(config)
