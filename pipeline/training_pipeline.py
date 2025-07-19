from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataPreprocessor
from src.model_training import ModelTraining
from utils.common_functions import read_yaml
from config.paths_config import *

if __name__=="__main__":
    ### 1. Data Ingestion

    config = read_yaml("config/config.yaml")  # read YAML file
    data_ingestion = DataIngestion(config)    # pass the parsed dictionary
    data_ingestion.run()

    ### 2. Data preprocessing
    processor = DataPreprocessor(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCESSED_DIR,CONFIG_FILE_PATH)
    processor.process()

    ### 3. Model training 
    trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH,PROCESSED_TEST_DATA_PATH,MODEL_OUTPUT_PATH)
    trainer.run()