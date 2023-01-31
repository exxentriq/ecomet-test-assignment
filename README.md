
# ecomet-test-assignment

Тестовое задание для e-Comet.io
## Как запустить сервер

Склонируйте репозиторий

```bash
  git clone https://github.com/exxentriq/ecomet-test-assignment
```

Укажите API-ключ для OpenWeatherMap в `.env` файлах по данным путям

```bash
  /ecomet-test-assignment/parser/.env
  /ecomet-test-assignment/server/.env
```

Перейдите в папку с репозиторием на диске

```bash
  cd ecomet-test-assignment
```

Соберите контейнер

```bash
  docker-compose build
```

Запустите контейнер

```bash
  docker-compose up
```

Сервер будет доступен по адресу

```bash
  127.0.0.1:80
```
## Справка по API

#### Получить по заданному городу все данные за выбранный период

```http
  GET /city_stats?city_id={city_id}&time_from={time_from}&time_to={time_to}
```

| Параметр | Тип     | Описание                |
| :-------- | :------- | :------------------------- |
| `city_id` | `int` | **Необходимый параметр.** OpenWeatherMap ID города |
| `time_from` | `timestamp` | Время "от" в формате Unix timestamp |
| `time_to` | `timestamp` | Время "до" в формате Unix timestamp |

## Пример использования

Запрос

```http
  GET 127.0.0.1:80/city_stats/?city_id=554234&time_to=1675182300
```

Ответ сервера

```json
{
    "city_id": 554234,
    "records_count": 5,
    "average_temperature": 3.03,
    "average_pressure": 1004.0,
    "average_wind_speed": 5.88,
    "time_from": "2023-01-31T16:20:08",
    "time_to": "2023-01-31T16:25:00",
    "all_records": [
        {
            "temperature_celsius": 3.03,
            "atmospheric_pressure": 1004,
            "wind_speed": 5.88,
            "time_updated": "2023-01-31T16:24:11"
        },
        {
            "temperature_celsius": 3.03,
            "atmospheric_pressure": 1004,
            "wind_speed": 5.88,
            "time_updated": "2023-01-31T16:23:10"
        },
        {
            "temperature_celsius": 3.03,
            "atmospheric_pressure": 1004,
            "wind_speed": 5.88,
            "time_updated": "2023-01-31T16:22:11"
        },
        {
            "temperature_celsius": 3.03,
            "atmospheric_pressure": 1004,
            "wind_speed": 5.88,
            "time_updated": "2023-01-31T16:21:11"
        },
        {
            "temperature_celsius": 3.03,
            "atmospheric_pressure": 1004,
            "wind_speed": 5.88,
            "time_updated": "2023-01-31T16:20:08"
        }
    ]
}
```