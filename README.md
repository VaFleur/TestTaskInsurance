# TestTaskInsurance

## Описание

Это API-сервис для расчёта стоимости страхования в зависимости от типа груза и объявленной стоимости.

### Технологии

- FastAPI
- PostgreSQL
- SQLAlchemy
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

### 4. Открытие приложения в браузере
Перейдите по адресу:
```
http://localhost:8000/docs
```

## Примеры использования

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

### 2. Расчёт стоимости страхования
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
