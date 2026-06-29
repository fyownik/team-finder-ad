# TeamFinder

**TeamFinder** - платформа создана для разработчиков, дизайнеров, тестировщиков и других IT-специалистов. Она решает проблему поиска команды для совместной работы над Pet-проектами. Авторизованные пользователи могут публиковать свои идеи, заявлять о поиске определённых стеков технологий, добавлять чужие проекты в «Избранное», откликаться на предложения и находить контакты единомышленников.

## Функциональность

- Регистрация, вход, выход и смена пароля.
- Просмотр и редактирование профиля пользователя.
- Загрузка аватара пользователя.
- Создание, редактирование и завершение проектов.
- Просмотр списка проектов с пагинацией.
- Добавление проектов в избранное без перезагрузки страницы.
- Присоединение к проектам и выход из команды проекта.
- Просмотр участников платформы.

## Технологии

- Python 3.12
- Django 5.2
- PostgreSQL
- Gunicorn
- Nginx
- Docker
- Docker Compose
- HTML, CSS, JavaScript

## Структура проекта

```text
team_finder/          настройки Django-проекта
users/                приложение пользователей
projects/             приложение проектов
templates_var1/       HTML-шаблоны варианта 1
static/               CSS, JS, изображения
media/                загруженные пользователями файлы, создается при работе
staticfiles/          собранная статика, создается командой collectstatic
Dockerfile            сборка Django-приложения
docker-compose.yml    запуск PostgreSQL, Django и Nginx
nginx.conf            конфигурация Nginx
requirements.txt      зависимости Python
```

## Переменные окружения

В корне проекта должен быть файл `.env`.

Пример содержимого:

```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=teamfinder
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

Назначение переменных:

| Переменная | Назначение |
|---|---|
| `DEBUG` | Режим отладки Django. Для локального запуска можно оставить `True`. |
| `SECRET_KEY` | Секретный ключ Django. |
| `ALLOWED_HOSTS` | Разрешенные хосты для запуска без Docker. |
| `POSTGRES_DB` | Название базы данных PostgreSQL. |
| `POSTGRES_USER` | Пользователь PostgreSQL. |
| `POSTGRES_PASSWORD` | Пароль PostgreSQL. |
| `POSTGRES_HOST` | Хост базы данных. В Docker используется `db`. |
| `POSTGRES_PORT` | Порт PostgreSQL внутри Docker-сети. |

## Запуск через Docker

Docker обязателен для запуска базы данных PostgreSQL и всего проекта.

### 1. Полная очистка старых контейнеров

Если проект уже запускался раньше, сначала можно удалить старые контейнеры и тома:

```bash
docker compose down -v --remove-orphans
docker rm -f teamfinder_db teamfinder_web teamfinder_gateway
```

Если какой-то контейнер уже удален, Docker может вывести ошибку для него. Это не страшно.

### 2. Сборка и запуск

```bash
docker compose up --build
```

После запуска приложение будет доступно по адресу:

```text
http://localhost/
```

## Служебные команды

Остановить проект:

```bash
docker compose down
```

Остановить проект и удалить базу данных:

```bash
docker compose down -v
```

Пересобрать статику:

```bash
docker compose exec web python manage.py collectstatic --clear --noinput
docker compose restart gateway
```

Создать суперпользователя:

```bash
docker compose exec web python manage.py createsuperuser
```

Если менялись модели и база стала несовместимой:

```bash
docker compose down -v
docker compose up --build
```

## Миграции

При запуске контейнера `web` миграции применяются автоматически командой из `docker-compose.yml`.

Если нужно выполнить миграции вручную:

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

## Статика и media-файлы

Статические файлы лежат в папке `static/`.

После команды `collectstatic` Django собирает их в папку `staticfiles/`, а Nginx отдает их по адресу:

```text
http://localhost/static/
```

Загруженные пользователями файлы, например аватары, сохраняются в `media/` и доступны по адресу:

```text
http://localhost/media/
```

## Основные адреса

```text
http://localhost/                  главная страница
http://localhost/users/register/   регистрация
http://localhost/users/login/      вход
http://localhost/users/list/       участники
http://localhost/projects/list/    проекты
http://localhost/admin/            админ-панель
```

## Примечание

В проекте используется набор шаблонов `templates_var1`.


## Автор проекта
- Запара Дарья 
- Email: dashazapara2021@gmail.com