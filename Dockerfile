FROM python:3.12-alpine

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

EXPOSE 8080

COPY ./main.py /app/main.py
COPY ./app /app/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

