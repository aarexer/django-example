# Структура

## gitignore

В `.gitignore` добавляем:

```python
.vscode/
*.pyc
.env
core/project/settings/local.py
static/*
!static/.gitkeep
*.sqlite*
```

## Окружение и poetry

```sh
poetry init
```

Установка зависимостей:

```sh
poetry add django
poetry add psycopg2
poetry add environ
```

## django

Структура будет сильно переиначена, поэтому делаем по шагам.

### core

Создаем папку `core` в корне.

Создаем проект с названием `project`:

```sh
django-admin startproject project
```

Переносим созданный `project` в `core`.

Файл `manage.py` выносим в корень.

Создаем сразу в `project` папку `settings`, туда копируем `settings.py` и переименовываем в `main.py`.
Создаем `local.py` для локальных настроек и прописываем:

```python
from .main import *

DEBUG = True

```

Меням строчку `project.settings` во всех файлах на `core.project.settings.local`.

В `manage.py` меняем:

```python
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'core.project.settings.local')
```

В `wsgi.py`:

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.project.settings.local')
```

В `asgi.py`:

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.project.settings.local')
```

Меняем `ROOT_URLCONF` в `main.py` на:

```python
ROOT_URLCONF = 'core.project.urls'
```

А также:

```python
WSGI_APPLICATION = 'core.project.wsgi.application'
```

### env

В корне создаем файл `.env`, выносим туда `DJANGO_PORT` и `DJANGO_SECRET_KEY` (при необходимости другие переменные окружения):

```text
DJANGO_SECRET_KEY='django-insecure-2$cdfy4-o6dgkrr%xjd5xx*le!o3i3a2c2_540je6x$xvliz#-'
DJANGO_PORT=8000

POSTGRES_DB=habrdb
POSTGRES_USER=habrpguser
POSTGRES_PASSWORD=pgpwd4habr
POSTGRES_PORT=5435
POSTGRES_HOST=postgres
```

Для использования переменных меняем в `main.py`:

```python
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

# код код код

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

# код код код

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT')
    }
}
```

### docker compose

В корне создаем папку `docker_compose` для хранения компоуз файлов.

В корне храним `Dockerfile`.

### api

В `core` папка `api`.

Верисонность - это подпапки: `v1`.

Создаем файлы `urls.py` как в `api`, так и в `v1`. В этом файле будем прописывать url-ы от api.

```python
urlpatterns = [
    # urls
]
```

В `core.project.urls.py`:

```pyhton
    path('api/', include('core.api.urls'))
```

### apps

Приложения храним в `core/apps`.

Например, для продуктов:

```sh
python manage.py startapp products core/apps/products
```

На уровне приложений разбиваем на `entity`, `models`, `services` и `use_cases`.

### tests

Тесты на сервисы и фактори.
