# Создать Django проект
# django-admin startproject <project_name> .

# Создать приложение. Для этого нужно находиться в главном пакете проекта (<project_name>)
# django-admin startapp <name_app>

install:
	poetry install

version:
	poetry run django-admin version

# Запуск приложения в product среде
start:
	gunicorn task_manager.wsgi:application

# Запуск приложения в среде разработки
dev:
	python manage.py runserver

commands:
	python manage.py


# Создать миграцию 
migrations:
	python manage.py makemigrations

# Применить миграцию
migrate:
	python manage.py migrate

# посмотреть, какой SQL-запрос будет выполняться при запуске миграции
# python manage.py sqlmigrate article 0001

shell:
	django-admin shell

admin:
	python manage.py createsuperuser

# Создать или обновить директорию, указанную в STATIC_ROOT, собрав все статические файлы.
# Сделать это нужно с DEBUG=True и DEBUG=False

static_files:
	python manage.py collectstatic

# Создать локали для русского языка
loc:
	python manage.py makemessages -l ru

# Компилировать локали
loc_comp:
	python manage.py compilemessages

lint:
	poetry run flake8 .
