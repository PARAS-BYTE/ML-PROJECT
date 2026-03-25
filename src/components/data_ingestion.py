import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd


from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from data_transformation import DataTransformation,DataTransformationConfig
from model_trainer import ModelTrainConfig,ModelTrainer

@dataclass
class DataIngestionCofig:
    train_data_path:str=os.path.join('artifacts','train.csv')
    test_data_path:str=os.path.join('artifacts','test.csv')
    raw_data_path:str=os.path.join('artifacts','raw.csv')


class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionCofig()
    def intiate_data_ingestion(self):
        logging.info('Entered the Data Ingestion Method / Component')
        try:
            df=pd.read_csv("data/stud.csv")
            logging.info("Read the Dataset as DataFrame")
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info('Train Test Split Intiated')
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Ingestion of the Data is Completly")
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )

        except Exception as e:
            raise CustomException(e,sys)
        

if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.intiate_data_ingestion()

    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.intiate_data_transformation(train_data,test_data)

    modeltrainer=ModelTrainer()
    sms=modeltrainer.intiate_model_trainer(train_arr,test_arr)
    print("Accuracy : ",sms)