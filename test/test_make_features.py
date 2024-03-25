import pandas as pd
import great_expectations as ge


def test_make_features():
    df_data = pd.read_csv('./data/interim/features_data.csv')
    df_ge = ge.from_pandas(df_data)

    # Тест наличие столбцов
    columns = ['create_date', 'price']
    for col in columns:
        assert df_ge.expect_column_to_exist(
                column=col
            ).success

    # Тест на количество уникальных значений
    assert df_ge.expect_column_unique_value_count_to_be_between(
            column='city_name',
            max_value=5
        ).success
    assert df_ge.expect_column_unique_value_count_to_be_between(
            column='repair_type',
            max_value=10
        ).success
    assert df_ge.expect_column_unique_value_count_to_be_between(
            column='home_type',
            max_value=10
        ).success

    # Тест на тип данных
    assert df_ge.expect_column_values_to_be_of_type(
            column='city_name',
            type_='str'
        ).success
    assert df_ge.expect_column_values_to_be_of_type(
            column='total_square',
            type_='float64'
        ).success
    assert df_ge.expect_column_values_to_be_of_type(
            column='square_coock',
            type_='float64'
        ).success
    assert df_ge.expect_column_values_to_be_of_type(
            column='square_rooms',
            type_='float64'
        ).success
    assert df_ge.expect_column_values_to_be_of_type(
            column='price',
            type_='float64'
        ).success
