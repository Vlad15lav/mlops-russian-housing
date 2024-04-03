import os
import requests
import json
import streamlit as st

from datetime import datetime

st.set_page_config(
        page_title="Houses Price Prediction",
        page_icon="🏙️"
    )

QUARY_FIELDS = (
    "city_name",
    "room_count",
    "total_square",
    "square_coock",
    "square_rooms",
    "repair_type",
    "home_type",
    "year_build",
    "max_floors"
)


def main():
    st.title('Узнай цену недвижимости🏡')
    st.text('Укажите параметры жилья и узнайте примерную цену:')

    # Блок для указание параметров
    col1, col2 = st.columns(2)

    with col1:
        city_name = st.selectbox(
            'Ваш город:',
            ('Москва', 'Санкт-Петербург', 'Казань')
        )
        repair_type = st.selectbox(
            'Тип ремонта:',
            (
                'Евро', 'Косметический',
                'Дизайнерский', 'Требуется ремонт'
            )
        )
        home_type = st.selectbox(
            'Тип конструкции:',
            (
                'Панельный', 'Кирпичный', 'Монолитный',
                'Монолитно-Кирпичный', 'Блочный'
            )
        )
        max_floors = st.number_input(
            'Этажей в доме:',
            min_value=1, max_value=45,
            value=16
        )
        year_build = st.number_input(
            'Год постройки:',
            min_value=1900, max_value=datetime.now().year,
            value=1976
        )

    with col2:
        room_count = st.number_input(
            'Количество комнат:',
            min_value=1, max_value=6,
            value=3, step=1
        )
        total_square = st.number_input(
            'Общая площадь:',
            min_value=10.0, max_value=200.0,
            value=75.0
        )
        square_coock = st.number_input(
            'Площадь кухни:',
            min_value=5.0, max_value=40.0,
            value=10.2
        )
        square_rooms = st.number_input(
            'Жилая площадь:',
            min_value=5.0, max_value=90.0,
            value=44.0
        )

    # Кнопка для запроса
    if st.button("Отправить"):
        values = [
            city_name,
            room_count,
            total_square,
            square_coock,
            square_rooms,
            repair_type,
            home_type,
            year_build,
            max_floors
        ]
        data_params = dict(zip(QUARY_FIELDS, values))

        try:
            response = requests.post(
                url=f'{os.getenv("MODEL_API_URL")}/predict',
                headers={
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                data=json.dumps(data_params)
            )

            if response.status_code == 200:
                response_json = response.json()
                price = int(response_json['0'] * 1_000_000)

                price_str = "{:,}".format(price).replace(',', ' ')
                st.write(f"Оценка стоимости: {price_str} рублей!💸")
            else:
                st.title("Сервер недоступен!😔")
        except requests.exceptions.ConnectionError:
            st.title("Сервер недоступен!😔")


if __name__ == '__main__':
    main()
