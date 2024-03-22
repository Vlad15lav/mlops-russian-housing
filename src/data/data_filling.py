import click
import pandas as pd

MEDIAN_FILL_COLS = (
    'square_coock',
    'square_rooms',
    'year_build'
)
MODE_FILL_COLS = (
    'room_count',
    'loggia',
    'room_type',
    'repair_type',
    'passanger_elevator',
    'cargo_elevator'
)


@click.command()
@click.argument('path_data', type=click.Path(exists=True))
@click.argument('path_save', type=click.Path())
def fill_nans(
        path_data: str,
        path_save: str,
        median_fill_cols: tuple = MEDIAN_FILL_COLS,
        mode_fill_cols: tuple = MODE_FILL_COLS
        ):
    """Обработка пропусков в данных

    Args:
        path_data: Путь к сырым CSV данным
        path_save: Путь для сохранения итогового файла
        median_fill_cols: столбцы, которые нужно заполнить медианой
        mode_fill_cols: столбцы, которые нужно заполнить модой
    """
    df_proc = pd.read_csv(path_data)

    for col in median_fill_cols:
        df_proc[col] = df_proc[col].fillna(df_proc[col].median())
    for col in mode_fill_cols:
        df_proc[col] = df_proc[col].fillna(df_proc[col].mode()[0])

    df_proc.to_csv(path_save, index=False)


if __name__ == '__main__':
    fill_nans()
