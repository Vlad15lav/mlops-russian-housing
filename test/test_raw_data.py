import pandas as pd
import great_expectations as ge

from datetime import datetime, timedelta


def test_raw_data():
    df_data = pd.read_csv('./data/raw/houses_dataset.csv')
    df_ge = ge.from_pandas(df_data)

    # Тест наличие столбцов
    raw_columns = [
        'id', 'create_date', 'city_name',
        'room_count', 'total_square',
        'square_coock', 'square_rooms', 'floor',
        'loggia', 'room_type', 'repair_type',
        'home_type', 'year_build', 'max_floors',
        'passanger_elevator', 'cargo_elevator', 'price'
        ]
    assert df_ge.expect_table_columns_to_match_ordered_list(
            column_list=raw_columns
        ).success

    # Тест на уникальность идентификатора
    assert df_ge.expect_column_values_to_be_unique(column='id').success

    # Тест на формат временных столбцов
    assert df_ge.expect_column_values_to_match_strftime_format(
            column="create_date",
            strftime_format="%Y-%m-%d %H:%M:%S"
        ).success

    # Тест на актуальность данных (за 60 дней)
    now = datetime.now()
    min_date = now - timedelta(days=60)
    assert df_ge.expect_column_values_to_be_between(
            "create_date",
            min_value=min_date,
            parse_strings_as_datetimes=True,
            meta={"dimension": 'Timelessness'}
        ).success
