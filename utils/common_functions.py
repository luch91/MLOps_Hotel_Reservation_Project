import os
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml

# Function to read the configuration fil
logger = get_logger(__name__)

def read_yaml(file_path: str):
    """
    Reads a YAML file and returns its content as a dictionary.
    
    :param file_path: Path to the YAML file.
    :return: Dictionary containing the YAML file content.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"file is not in the given path")
        with open(file_path, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info(f"YAML file read successfully read")
            return config
        
    except Exception as e:
        logger.error(f"Error reading YAML file")
        raise CustomException(f"Failed to read YAML file",e)



def load_data(path):
    try:
        logger.info("Loading data")
        return pd.read_csv(path)
    except Exception as e:
        logger.error(f"Error loading the data")
        raise CustomException("Failed to load data",e)
