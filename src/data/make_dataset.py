import click
import pandas as pd


@click.command()
@click.argument('path_data', type=click.Path(exists=True))
@click.argument('path_save', type=click.Path())
@click.argument('proportion', type=click.INT)
def make_feature(
        path_data: str,
        path_save: str,
        proportion: int = 85
        ):
    """Функция для разбиения на обучающую и тестовую выборку

    Args:
        path_data: Путь к CSV данным
        path_save: Путь для сохранения итоговых данных
        proportion: Доля данных для обучения
    """
    df_data = pd.read_csv(path_data)
    df_data.sort_values(by='create_date', inplace=True)

    dataset_size = len(df_data)
    df_train = df_data.iloc[:int(dataset_size * proportion / 100)]
    df_test = df_data.iloc[int(dataset_size * proportion / 100):]

    df_train.to_csv(path_save + "/train_houses.csv", index=False)
    df_test.to_csv(path_save + "/test_houses.csv", index=False)


if __name__ == '__main__':
    make_feature()
