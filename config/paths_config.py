import os

################################ DATA INGESTION #########################

RAW_DIR ="artifacts/raw_data"
RAW_FILE_PATH = os.path.join(RAW_DIR, "raw.csv")
TRAIN_FILE_PATH = os.path.join(RAW_DIR, "train.csv")
TEST_FILE_PATH = os.path.join(RAW_DIR, "test.csv")

################################ CONFIGURATION #########################
# Path to the configuration file
CONFIG_FILE_PATH = "config/config.yaml"

###################### DATA PROCESSING #########################
PROCESSED_DIR = "artifacts/processed_data"
PROCESSED_TRAIN_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_train.csv")
PROCESSED_TEST_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_test.csv")

################################ MODEL TRAINING #########################
MODEL_OUTPUT_PATH = "artifacts/models/lgbm_model.pkl"