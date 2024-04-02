import pandas as pd

from pydantic import BaseModel


class Quary(BaseModel):
    """Класс для валидации входных данных
    """
    city_name: str
    room_count: int
    total_square: float
    square_coock: float
    square_rooms: float
    repair_type: str
    home_type: str
    year_build: int
    max_floors: int


class DataLoader:
    def preproccesing_data(self, quary):
        """Обработка входных данных для модели
        """
        df_data = pd.DataFrame([quary.dict()])
        return df_data
