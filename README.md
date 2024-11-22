# TestTaskInsurance

## Описание

Это API-сервис для расчёта стоимости страхования в зависимости от типа груза и объявленной стоимости.

### Технологии

- FastAPI
- PostgreSQL
- SQLAlchemy
- Kafka
- Docker & Docker Compose

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/VaFleur/TestTaskInsurance.git
cd TestTaskInsurance
```

### 2. Запуск Docker-контейнеров

```commandline
docker compose up --build
```

### 3. Применение миграций

```commandline
docker compose exec web python -m app.main
```

### 4. Создане топика в Kafka
```commandline
docker-compose exec kafka kafka-topics --create \
  --topic insurance-logs \
  --bootstrap-server kafka:9092 \
  --partitions 1 \
  --replication-factor 1
```

### 5. Просмотр логов топика
```commandline
docker-compose exec kafka kafka-console-consumer \
  --topic insurance-logs \
  --from-beginning \
  --bootstrap-server kafka:9092
```

### 6. Открытие приложения в браузере
Перейдите по адресу:
```
http://localhost:8000/docs
```

## Использование API

### 1. Добавление тарифа
- URL: /api/rate
- Метод: POST
- Тело запроса:
```commandline
{
  "cargo_type": "electronics",
  "rate": 0.05,
  "effective_date": "2024-11-01"
}
```

### 2. Редактирование тарифа
- URL: /api/rate/{rate_id}
- Метод: PUT
- Тело запроса:
```commandline
{
  "rate": 0.07,
}
```

### 3. Удаление тарифа
- URL: /api/rate/{rate_id}
- Метод: DELETE

### 4. Получение тарифа
- URL: /api/rate/{rate_id}
- Метод: GET

### 5. Получение всех тарифов
- URL: /api/rates
- Метод: GET

### 6. Расчёт стоимости страхования
- URL: /api/calculate
- Метод: GET
- Пример запроса:

```commandline
/api/calculate?cargo_type=electronics&declared_value=1000&date=2024-11-07
```
- Ответ:

```commandline
{
  "cargo_type": "electronics",
  "declared_value": 1000,
  "rate": 0.05,
  "insurance_cost": 50.0
}
```
