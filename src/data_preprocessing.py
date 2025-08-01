import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataPreprocessor:
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir

        self.config = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    def preprocess_data(self, df):
        try:
            logger.info("Starting data preprocessing")

            logger.info("Dropping the unnecessary columns")
            df.drop(columns=[col for col in ['Unnamed: 0', 'Booking_ID'] if col in df.columns], inplace=True) # fixed typo
            df.drop_duplicates(inplace=True)

            cat_cols = self.config['data_processing']['categorical_columns']
            num_cols = self.config['data_processing']['numerical_columns']

            logger.info("Applying label encoding to categorical columns")
            label_encoder = LabelEncoder()
            mappings = {}

            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col] = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))

            logger.info(f"Label Mappings are: ")
            for col, mapping in mappings.items():
                logger.info(f"{col}: {mapping}")

            logger.info("Handling Skewness")
            skewness_threshold = self.config["data_processing"]["skewness_threshold"]
            skewness = df[num_cols].apply(lambda x: x.skew())

            for column in skewness[skewness > skewness_threshold].index:
                df[column] = np.log1p(df[column])

            return df
        except Exception as e:
            logger.error("Error during data preprocessing")
            raise CustomException("Data preprocessing failed", e)

    def balanced_data(self, df):
        try:
            logger.info("Handling Imbalanced Data")
            X = df.drop(columns=["booking_status"])
            y = df["booking_status"]

            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X, y)

            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)  # fixed typo
            balanced_df["booking_status"] = y_resampled

            logger.info("Imbalanced data handled successfully")
            return balanced_df
        except Exception as e:
            logger.error(f"Error handling imbalanced data: {e}")
            raise CustomException("Failed to handle imbalanced data", e)

    def select_features(self, df):
        try:
            logger.info("Starting feature selection")

            X = df.drop(columns=["booking_status"])
            y = df["booking_status"]

            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)

            feature_importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({
                'Feature': X.columns,
                'Importance': feature_importance
            })

            top_features_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
            num_features_to_select = self.config["data_processing"]["no_of_features"]  # fixed key

            top_features = top_features_importance_df["Feature"].head(num_features_to_select).values  # used config

            logger.info(f"Features Selected: {top_features}")

            top_df = df[top_features.tolist() + ['booking_status']]

            logger.info("Feature Selection Completed Successfully")
            return top_df
        except Exception as e:
            logger.error(f"Error during feature selection: {e}")
            raise CustomException("Feature selection failed", e)

    def save_processed_data(self, df, file_path):
        try:
            logger.info(f"Saving processed data to {file_path}")
            df.to_csv(file_path, index=False)
            logger.info(f"Processed data saved successfully to {file_path}")  # fixed f-string
        except Exception as e:
            logger.error(f"Error saving processed data to {file_path}")
            raise CustomException("Failed to save processed data", e)

    def process(self):
        try:
            logger.info("Loading data from RAW directory")

            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.balanced_data(train_df)
            test_df = self.balanced_data(test_df)

            train_df = self.select_features(train_df)
            test_df = self.select_features(test_df)

            self.save_processed_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_processed_data(test_df, PROCESSED_TEST_DATA_PATH)

            logger.info("Data processing pipeline completed successfully")
        except Exception as e:
            logger.error(f"Error in data processing pipeline: {e}")
            raise CustomException("Data processing pipeline failed", e)


if __name__ == "__main__":
    processor = DataPreprocessor(
        TRAIN_FILE_PATH,
        TEST_FILE_PATH,
        PROCESSED_DIR,
        CONFIG_FILE_PATH
    )
    processor.process()
