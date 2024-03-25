import pandas as pd
import great_expectations as ge


def test_data_filling():
    df_data = pd.read_csv('./data/interim/fill_data.csv')
    df_ge = ge.from_pandas(df_data)

    # Тест наличие столбцов
    columns = [
        'id', 'create_date', 'city_name',
        'room_count', 'total_square',
        'square_coock', 'square_rooms', 'floor',
        'loggia', 'room_type', 'repair_type',
        'home_type', 'year_build', 'max_floors',
        'passanger_elevator', 'cargo_elevator', 'price'
        ]
    assert df_ge.expect_table_columns_to_match_ordered_list(
            column_list=columns
        ).success

    # Тест на отсутствие пропусков в данных
    for col in columns:
        assert df_ge.expect_column_values_to_not_be_null(
            column=col
        ).success
