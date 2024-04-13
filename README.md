# MLOps Russian Real Estate Price Prediction

Этот проект демонстрирует систему MLOps для прогнозирования цен на недвижимость. В нем используются различные инструменты и технологии для сбора данных, обучения моделей, тестирования, развертывания и мониторинга. 

## Структура MLOps платформы

Платформа MLOps состоит из следующих пунктов:
- Сбор данных с помощью Web парсера Selenium по расписанию AirFlow.
- Версионирования данных и автоматизация пайплайна обучения с помощью DVC.
- Автотестирование кода и проверка качества данных с помощью Continuous Integration.
- Отслеживание экспериментов с помощью MLFlow сервиса.
- Авторазвертывание REST API приложение с помощью FAST API и Continuous Deployment.
- Мониторинг модели с помощью Prometheus и визуализация в Grafana.
- Web сервис Streamlit для взаимодействия с моделью.

![Схема проекта MLOps](/reports/figures/MLOps%20Russian%20Housing.svg)

## Инструкция запуска

Укажите значения для набора переменных среды в ".env_example":
```shell
# Данные для AirFlow (id -u)
AIRFLOW_UID=<...>
AIRFLOW_S3_BUCKET=airflow-data

# Данные для S3 Minio
AWS_ACCESS_KEY_ID=<...>
AWS_SECRET_ACCESS_KEY=<...>
AWS_S3_BUCKET=mlflow-arts
MINIO_ROOT_USER=<...>
MINIO_ROOT_PASSWORD=<...>
...
```

Переименуйте ".env_example" в файл ".env":
```bash
mv .env_example .env
```

Запускаем ETL планировщик с AirFlow сервисом для сбора данных:
```bash
docker-compose -f ./docker-compose-airflow.yaml up -d
```

Запускаем MLFlow микросервис:
```bash
docker-compose -f ./docker-compose-mlflow.yaml up -d
```

Запустите DAG **extract_houses_data** в AirFlow, зайдя по адресу [localhost:8080](http://localhost:8080), дождитесь его завершения. 

Устанавливаем Python 3.11 с необходимыми пакетами:
```bash
python -m venv ./env
source ./env/bin/activate
# For Windows .\env\Scripts\Activate

pip install -r requirements.txt
```

Запускаем DVC pipeline с предобработкой данных, обучением и трекингом модели MLFlow:
```bash
dvc repro
```

Запускаем Production микросервис:
```bash
docker-compose -f ./docker-compose-app.yaml up -d
```

Получить предсказание стоимости жилья по ссылке [localhost:8501](http://localhost:8501).

Примечание:
- Для валидации модели можно использовать пример [ноутбука](/notebooks/feature_analysis.ipynb).
- Результаты экспериментов показаны в MLFlow Tracking сервере [localhost:5000](http://localhost:5000).
- Для заимодействия с Postgres используется pgAdmin [localhost:5050](http://localhost:5050).
- Для настройки CI/CD pipeline необходимо использовать [GitLab Runner](https://docs.gitlab.com/runner) с оболочкой PowerShell и указать ему теги **test**, **data**, **deploy**. 

## Возможные доработки платформы

Возможные доработки и сервисы для платформы:
- Использование очередей RabbitMQ/Kafka с Redis для асинхронного прогнозирования.
- Использование Feature Store и Metric Store.
- Мониторинг дрифта данных и качество модели с помощью [Evidently AI](https://www.evidentlyai.com).
- Масштабирование модели с помощью репликации Kubernetes.
- Настройка Canary развертывания и User сервиса для A/B тестирования.

## Полезные ссылки

- [MLOps и production в DS исследованиях 3.0](https://ods.ai/tracks/mlops3-course-spring-2024)
- [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp)