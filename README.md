## 1. Склонировать репозиторий и перейти в папку проекта

git clone https://github.com/fikfok/news.git


cd news

## 2. Установить зависимости с помощью менеджера пакетов poetry

poetry install

## 3. Запустить docker

sudo docker-compose up -d

## 4. Запустить alembic миграции

alembic upgrade head

## 5. Запустить celery очередь

celery --app=news.celery_workers.celery worker --beat --loglevel=debug

## 6. Запустить fastapi приложение

uvicorn news.main:app --reload

## 7. Открыть приложение в браузере

http://127.0.0.1:8000/docs

## 8. Добавить новый источник новостей

[Ссылка](http://127.0.0.1:8000/docs#/%D0%98%D0%BC%D0%BF%D0%BE%D1%80%D1%82%20%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B5%D0%B9/add_source_api_v1_sources__post)


```
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/sources/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "news_label": "Lenta 24",
  "news_url": "https://lenta.ru/rss/last24",
  "interval_sec": 86400,
  "source_type": "rss"
}'
```

## 9. Запросить список новостных источников

```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/sources/?page=1&page_size=10' \
  -H 'accept: application/json'
```

## 10. Запросить список новостей по конкретному источнику

```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/sources/1/news?page=1&page_size=10' \
  -H 'accept: application/json'
```

## Комментарии

1. Сохранение новостей реализовано далеко не оптимально - весь новостной блок сохраняется в виде текста. Соответственно возможно дублирование новостных блоков;
2. При выборе новостей по конкретному источнику извлекаются все новости сразу и только потом происходить извлечение подмножества новостей из блока согласно пагинации;
3. Не успел сделать запаковку в докер всего приложения.