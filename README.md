### Описание проекта

Проект BannerService представляет собой сервис баннеров, с помощью которого пользователям показывается
разный контент в зависимости от их принадлежности к какой-либо группе. Принцип создания интерфейса - REST,
переход к API осуществлен на основе Django REST Framework.

Данные для авторизации в админ-зоне:

логин: admin пароль: admin123

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Amica24/banner_service.git
```

```
cd banner_service
```

Запустить сборку контейнеров:

```
make dev
```
`docker-compose exec backend python manage.py migrate` # Выполнить миграции

`docker-compose exec backend python manage.py createsuperuser` # Создать суперпользователя

### Примеры запросов к API:

POST-запрос для получения токена пользователя
http://127.0.0.1:8080/api-token-auth/
* Права доступа: Доступно без токена. 

```
{
    "username": "no_admin",
    "password": "0o9i8u7y6t"
}
```

Пример ответа при удачном выполнении запроса:

```
{
    "token": "2d3db7280089de69f6967f5971f798f5b1c5d843"
}
```

GET-запрос для получения баннера для пользователя
http://127.0.0.1:8080/user_banner/?feature_id=3243432&tag_id=53432478
* Права доступа: Авторизованный пользователь.

Headers:
```
{
    "Authorization": "Token ef47819b4b65078fcf2f9d49d6e51ef9bc96c13e"
}
```
Пример ответа при удачном выполнении запроса:

```
{
    "title": "some_title",
    "text": "some_text",
    "url": "some_url"
}
```

Все следующие запросы выполняются с токеном администратора
Headers:
```
{
    "Authorization": "Token ef47819b4b65078fcf2f9d49d6e51ef9bc96c13e"
}
```

GET-запрос для получения всех баннеров c фильтрацией по фиче и/или тегу 
http://127.0.0.1:8000/banner/?feature_id=3243432
* Права доступа: Администратор.

Пример ответа при удачном выполнении запроса:

```
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "tag_id": [
                456456,
                534324,
                434534
            ],
            "feature_id": 3243432,
            "content": {
                "text": "some_text",
                "url3": "some_url",
                "title": "some_title"
            },
            "is_active": false,
            "created_on": "2024-04-13T20:00:39Z",
            "updated_on": "2024-04-14T10:58:39.415686Z"
        },
        {
            "id": 5,
            "tag_id": [
                53432478
            ],
            "feature_id": 3243432,
            "content": {
                "ok": "ok2",
                "yes": "yes2"
            },
            "is_active": true,
            "created_on": "2024-04-14T10:32:40.244110Z",
            "updated_on": "2024-04-14T10:32:40.244462Z"
        }
    ]
}
```
POST-запрос для создания нового баннера
http://127.0.0.1:8000/banner/?feature_id=3243432
* Права доступа: Администратор.
```
{
    "tag_ids": [
        456456,
        534324,
        434534
    ],
    "feature_id": 3243432,
    "content": {
        "text": "some_text",
        "url3": "some_url",
        "title": "some_title"
    },
    "is_active": true,
    "created_on": "2024-04-13T20:00:39Z",
    "updated_on": "2024-04-14T10:58:39.415686Z"
}
```
PATCH-запрос для обновления содержания баннера
http://127.0.0.1:8000/banner/1/
* Права доступа: Администратор
```
{
    "tag_ids": [
        456456,
        534324
    ],
    "feature_id": 3243432,
    "content": {
        "text": "some_text",
        "url3": "some_url",
        "title": "some_title"
    },
    "is_active": true,
    "created_on": "2024-04-13T20:00:39Z",
    "updated_on": "2024-04-14T10:58:39.415686Z"
}
```

PATCH-запрос для удаления баннера
http://127.0.0.1:8000/banner/1/
* Права доступа: Администратор.


## Шаблон наполнения env-файла

`DB_ENGINE` # указываем, что работаем с postgresql

`DB_NAME` # имя базы данных

`DB_USER` # логин для подключения к базе данных

`DB_PASSWORD` # пароль для подключения к БД

`DB_HOST` # название сервиса (контейнера)

`DB_PORT` # порт для подключения к БД

`SECRET_KEY` # секретный ключ

`REDIS_URL` 

`REDIS_PORT` 

`REDIS_ENDPOINT` 

тесты дописаны не до конца. Не проходила авторизация, не стала добивать