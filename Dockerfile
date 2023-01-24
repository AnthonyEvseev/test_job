FROM python:3.10

WORKDIR /app
EXPOSE 80

ENV REDIS_DSN="" \
    REBBIT_DSM=""

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir --upgrade -r requirements.txt


COPY . .

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "80"]