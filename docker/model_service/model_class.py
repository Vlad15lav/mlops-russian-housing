import os
import mlflow
import pandas as pd

from mlflow import MlflowClient
from data_class import DataLoader, Quary


class Model:
    def __init__(
            self,
            data_class: DataLoader,
            model_name: str,
            version: int = None) -> None:
        """Класс для модели предсказания

        Args:
            data_class (DataLoader): Объект класса для обработки входных данных
            model_name (str): Название модели из MLFlow Models
            version (int): Версия модели (если None,
                то будет выбрана последняя версия)
        """
        self.data_class = data_class
        self.model_name = model_name
        self.version = version

        print(f"MLFlow Tracking URI: {os.getenv('MLFLOW_TRACKING_URI')}")
        self.client = MlflowClient(
            tracking_uri=os.getenv('MLFLOW_TRACKING_URI')
            )

        if self.version is None:
            model_metadata = self.client.get_latest_versions(model_name,
                                                             stages=["None"])
            self.version = model_metadata[0].version

        print(f"The current model: {self.model_name}")
        print(f"Version model is {self.version}")

        self.model = mlflow.pyfunc.load_model(
            f"models:/{self.model_name}/{self.version}"
            )

    def get_data(self, quary: Quary) -> pd.DataFrame:
        """Преобразование данных для Inference
        """
        return self.data_class.preproccesing_data(quary)

    def singal_predict(self, data: pd.DataFrame) -> float:
        """Предсказание для одного элемента
        """
        predict = self.model.predict(data)[0]
        return predict

    def predict(self, quary: Quary) -> dict:
        """Предсказание модели
        """
        data = self.get_data(quary)

        result = {}
        for i in range(len(data)):
            result[i] = self.singal_predict(data.iloc[[i]])

        return result

    def get_info(self):
        """Вернуть информацию о модели
        """
        return {
            'model_name': self.model_name,
            'version': self.version
        }
