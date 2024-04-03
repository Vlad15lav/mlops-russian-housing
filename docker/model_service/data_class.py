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

        # Заменяем категориальные значения для модели
        df_data["city_name"] = df_data["city_name"].map({
            "Москва": "moskva",
            "Санкт-Петербург": "sankt-peterburg",
            "Казань": "kazan"
        })
        df_data["repair_type"] = df_data["repair_type"].map({
            "Евро": "евро",
            "Косметический": "косметический",
            "Дизайнерский": "дизайнерский",
            "Требуется ремонт": "требует"
        })
        df_data["home_type"] = df_data["home_type"].map({
            "Панельный": "панельный",
            "Кирпичный": "кирпичный",
            "Монолитный": "монолитный",
            "Монолитно-Кирпичный": "монолитно",
            "Блочный": "блочный"
        })

        return df_data
