import os
import sys
import pandas as pd
from google.cloud import storage
from src.logger import get_logger
from src.custom_exception import CustomException
from sklearn.model_selection import train_test_split
from utils.common_functions import read_yaml
from config.paths_config import RAW_DIR, RAW_FILE_PATH, TRAIN_FILE_PATH, TEST_FILE_PATH, CONFIG_FILE_PATH

# Function to download the dataset from Google Cloud Storage
logger = get_logger(__name__)


class DataIngestion:
    def __init__(self, config):
        self.config = config['data_ingestion']
        self.bucket_name = self.config['bucket_name']
        self.file_name = self.config['bucket_file_name']
        self.train_test_ratio = self.config['train_ratio']

        os.makedirs(RAW_DIR, exist_ok=True)
        logger.info(f"Data Ingestion initialized with bucket: {self.bucket_name}, file is: {self.file_name}")

    def download_csv_from_gcp(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)
            
            logger.info(f"Downloading file {self.file_name} from GCP bucket {self.bucket_name}")
            blob.download_to_filename(RAW_FILE_PATH)
            logger.info(f"File downloaded from GCP bucket to {RAW_FILE_PATH}")
        
        except Exception as e:
            logger.error(f"Error downloading file from GCP: {e}")
            raise CustomException(f"Failed to download file from GCP: {e}",sys)

        if not os.path.exists(RAW_FILE_PATH):
            logger.error(f"Download failed. {RAW_FILE_PATH} does not exist.")
        else:
            logger.info(f"Confirmed: {RAW_FILE_PATH} exists.") 

    def split_data(self):
        try:
            df = pd.read_csv(RAW_FILE_PATH)
            logger.info(f"Data loaded from {RAW_FILE_PATH}")

            train_df, test_df = train_test_split(df, test_size=1 - self.train_test_ratio, random_state=42)
            logger.info(f"Data split into train and test sets with ratio {self.train_test_ratio}")

            train_df.to_csv(TRAIN_FILE_PATH, index=False)
            test_df.to_csv(TEST_FILE_PATH, index=False)
            logger.info(f"Train and test data saved to {TRAIN_FILE_PATH} and {TEST_FILE_PATH}")

        except Exception as e:
            logger.error(f"Error splitting data: {e}")
            raise CustomException(f"Failed to split data: {e}")

    def run(self):  # ✅ Now it's properly placed
        try:
            logger.info("Starting data ingestion process")

            self.download_csv_from_gcp()
            self.split_data()

            logger.info("Data Ingestion completed successfully")

        except CustomException as ce:
            logger.error(f"CustomException: {str(ce)}")

        finally:
            logger.info("Data Ingestion completed")


from utils.common_functions import read_yaml

if __name__ == "__main__":
    config = read_yaml("config/config.yaml")  # read YAML file
    data_ingestion = DataIngestion(config)    # pass the parsed dictionary
    data_ingestion.run()
    logger.info("Data Ingestion script executed successfully")
