import pandas as pd
import mlflow

from mlflow.models import infer_signature

from catboost import CatBoostRegressor, Pool
from sklearn.metrics import r2_score, mean_absolute_error, \
    mean_squared_error, mean_absolute_percentage_error

MODEL_PARAMS = {
    'eval_metric': 'MAE',
    'task_type': 'CPU',
    'random_seed': 42,
    'iterations': 3000,
    'boosting_type': 'Plain',
    'bootstrap_type': 'Bayesian',
    'grow_policy': 'Depthwise',
    'learning_rate': 0.037297597071406306,
    'depth': 7,
    'l2_leaf_reg': 0.12185690368805563,
    'random_strength': 1.5112665096214164,
    'rsm': 0.6975599491377841,
    'border_count': 176,
    'leaf_estimation_method': 'Newton',
    'min_data_in_leaf': 3,
    'bagging_temperature': 0.03690571959358184
}

TRAIN_SIZE = 0.85
CAT_FEATURES = (
    'city_name',
    'repair_type',
    'home_type'
)

mlflow.set_tracking_uri('http://localhost:5000')
mlflow.set_experiment('houses_price_prediction')


def train_model():
    print('MLFlow Tracking Server: ', mlflow.get_tracking_uri())

    train_data = pd.read_csv('./data/processed/train_houses.csv')
    test_data = pd.read_csv('./data/processed/test_houses.csv')

    train_data.sort_values(by='create_date', inplace=True)
    train_data.drop(columns='create_date', inplace=True)
    test_data.drop(columns='create_date', inplace=True)

    data_size = len(train_data)
    train_split = int(TRAIN_SIZE * data_size)
    X_data, y_data = train_data.drop(columns='price'), train_data['price']

    X_train, y_train = X_data.iloc[:train_split], y_data.iloc[:train_split]
    X_valid, y_valid = X_data.iloc[train_split:], y_data.iloc[train_split:]
    X_test, y_test = test_data.drop(columns='price'), test_data['price']

    train_pool = Pool(X_train, y_train, cat_features=CAT_FEATURES)
    valid_pool = Pool(X_valid, y_valid, cat_features=CAT_FEATURES)

    with mlflow.start_run():
        model = CatBoostRegressor(**MODEL_PARAMS)
        model.fit(
            train_pool,
            eval_set=valid_pool,
            verbose=30,
            use_best_model=True,
            plot=False,
            early_stopping_rounds=30
        )

        test_predict = model.predict(X_test)

        test_mae = mean_absolute_error(test_predict, y_test)
        test_mse = mean_squared_error(test_predict, y_test)
        test_mape = mean_absolute_percentage_error(test_predict, y_test)
        test_r2 = r2_score(test_predict, y_test)

        print('Test MAE: ', test_mae)
        print('Test MSE: ', test_mse)
        print('Test MAPE: ', test_mape)
        print('Test R2: ', test_r2)

        mlflow.set_tag("CatBoost", "Finale model")
        mlflow.log_params(MODEL_PARAMS)

        mlflow.log_metric('Test MAE', test_mae)
        mlflow.log_metric('Test MSE', test_mse)
        mlflow.log_metric('Test MAPE', test_mape)
        mlflow.log_metric('Test R2', test_r2)

        signature = infer_signature(X_train, model.predict(X_train))

        mlflow.catboost.log_model(
            cb_model=model,
            artifact_path='model',
            signature=signature,
            input_example=X_train,
            registered_model_name="catboost_model"
        )


if __name__ == '__main__':
    train_model()
