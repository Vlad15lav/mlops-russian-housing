FROM python:3.9

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./web.py ./web.py

CMD ["streamlit", "run", "web.py" "--server.port" "8501"]