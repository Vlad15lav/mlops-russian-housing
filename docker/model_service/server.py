import os
from fastapi import FastAPI
from data_class import DataLoader, Quary
from model_class import Model

app = FastAPI()
model = Model(data_class=DataLoader(),
              model_name='catboost_model',
              version=None)


@app.post("/predict")
async def get_predict(quary: Quary):
    # Запрос предсказание цены
    return model.predict(quary)


@app.get("/model_info")
async def get_info():
    # Запрос для получения информации о модели
    return model.get_info()


# Проверяем наличие переменных для загрузки модели
if os.getenv('MLFLOW_TRACKING_URI') is None:
    exit(1)
