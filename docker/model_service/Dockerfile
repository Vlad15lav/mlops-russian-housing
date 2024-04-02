FROM python:3.9

WORKDIR /app 

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./data_class.py ./data_class.py
COPY ./model_class.py ./model_class.py
COPY ./server.py ./server.py

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]
