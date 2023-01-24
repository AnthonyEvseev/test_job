### В docker-compose.yaml есть баг =(
### Воспользуйся пока что инструкцией ниже
# Порядок запуска приложения через Docker

1) RabbitMQ```sudo docker run -d --name rabbit_mq_api -p 15672:15672 -p 5672:5672 -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password  rabbitmq:3-management```

2) Redis ```sudo docker run -d --name redis_api -p 6379:6379 redis/redis-stack-server:latest```

3) Билд контейнера сервисов
   ```docker build -t app_api .```

4) Запуск контейнера сервисов
   ```sudo docker run -d --name kontainer -p 8022:80 -e REDIS_DSN=redis://{external_ip}:6379 -e RABBIT_DSN=amqp://user:password@{external_ip}:5672/ app_api```
   

Переменные строки запуска контейнера:

- external_ip - Внешний IP адрес инстанса сервера (адрес который тебе даёт роутер)
- если ты сменишь имя 3го контейнера, не забудь его изменить в 4й контейнере (последняя переменная)

5) Точка входа в API

- http://127.0.0.1:8022/docs

6) Чтобы Swagger работал корректно отключи в браузере блокировщики рекламы