import click
import pandas as pd

USE_FEATURES = (
    'create_date',
    'city_name',
    'room_count',
    'total_square',
    'square_coock',
    'square_rooms',
    'repair_type',
    'home_type',
    'year_build',
    'max_floors',
    'passanger_elevator'
)


@click.command()
@click.argument('path_data', type=click.Path(exists=True))
@click.argument('path_save', type=click.Path())
def make_feature(
        path_data: str,
        path_save: str,
        col_features: list = USE_FEATURES,
        target_col: str = None
        ):
    """Функция для генерация признаков

    Args:
        path_data: Путь к сырым CSV данным
        path_save: Путь для сохранения итогового файла
        col_features: используемые столбцы для обучения
        target_col: название столбца таргета
    """
    df_data = pd.read_csv(path_data)

    use_cols = list(col_features)
    if target_col:
        use_cols.append(target_col)

    df_features = df_data[use_cols].copy()

    if 'city_name' in use_cols:
        df_features['city_name'] = df_features['city_name'].apply(
            lambda x: 'sankt-peterburg' if 'sankt' in x else x
            )

    if target_col:
        df_features[target_col] = df_features[target_col].astype(float)

    df_features.to_csv(path_save, index=False)


if __name__ == '__main__':
    make_feature()
