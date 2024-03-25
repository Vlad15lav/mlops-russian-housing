import pandas as pd
import great_expectations as ge


def test_make_dataset():
    df_train = pd.read_csv('./data/processed/train_houses.csv')
    df_test = pd.read_csv('./data/processed/test_houses.csv')

    df_train_ge = ge.from_pandas(df_train)
    df_test_ge = ge.from_pandas(df_test)

    # Тест наличие столбцов
    columns = ['create_date', 'price']
    for col in columns:
        assert df_train_ge.expect_column_to_exist(
                column=col
            ).success

    columns = ['create_date', 'price']
    for col in columns:
        assert df_test_ge.expect_column_to_exist(
                column=col
            ).success

    # Тест на train size split выборок
    assert len(df_train) / len(df_test) >= 5

    # Тест на datetime split выборок
    train_max_date = df_train['create_date'].max()
    train_min_date = df_test['create_date'].min()
    assert train_max_date <= train_min_date
