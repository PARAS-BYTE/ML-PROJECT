import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler 
from src.exception import CustomException
from src.logger import logging
import os
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join("artifacts","preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    def get_data_transformer(self):
        try:
            numerical_feature=["writing_score","reading_score"]
            categorical_feature=["gender","race_ethnicity","parental_level_of_education","lunch","test_preparation_course"]
            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )
            cat_pipeline=Pipeline([
                 ("imputer",SimpleImputer(strategy="most_frequent")),
                 ("one_hot_encoder",OneHotEncoder()),
            ])
            prerocessor=ColumnTransformer([
                ("numerical_pipeline",num_pipeline,numerical_feature),
                ("categorical_pipeline",cat_pipeline,categorical_feature)
            ])
            logging.info(f"Numerical Columns : {numerical_feature}")
            logging.info(f"Categorical Columns : {categorical_feature}")

            return prerocessor
        except Exception as e:
            raise CustomException(e,sys)
    
    def intiate_data_transformation(self,train_path,test_path):
        try :
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path) 

            logging.info("Reading Train and Test Data Completed")


            logging.info("Obtaining pre-processing object")

            preprocessing_obj=self.get_data_transformer()

            target_column_name="math_score"
            numerical_feature=["writing_score","reading_score"]
            categorical_feature=["gender","race_ethnicity","parental_level_of_education","lunch","test_preparation_course"]

            input_feature_train_df=train_df.drop(target_column_name,axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(target_column_name,axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info("Applying preprocessing object on training dataframe and testing dataframe")
            x_train=preprocessing_obj.fit_transform(input_feature_train_df)
            x_test=preprocessing_obj.transform(input_feature_test_df)
            
            train_arr=np.c_[x_train,np.array(target_feature_train_df)]
            test_arr=np.c_[x_test,np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object. ")
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj,
            )
            
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e,sys)
