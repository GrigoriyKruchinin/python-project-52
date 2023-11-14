# Создать Django проект
# django-admin startproject task_manager .

# Создать приложение. Для этого нужно находиться в главном пакете проекта (task_manager)
# django-admin startapp <name_app>

install:
	poetry install

version:
	poetry run django-admin version

# Запуск приложения в product среде
start:
	gunicorn task_manager.wsgi

# Запуск приложения в среде разработки
dev:
	python manage.py runserver

commands:
	python manage.py


# Создать миграцию и Применить миграцию
migrate:
	python manage.py makemigrations && python manage.py migrate

# посмотреть, какой SQL-запрос будет выполняться при запуске миграции
# python manage.py sqlmigrate article 0001

shell:
	python manage.py shell

admin:
	python manage.py createsuperuser

# Создать или обновить директорию, указанную в STATIC_ROOT, собрав все статические файлы.
static:
	python manage.py collectstatic

# Создать локали для русского языка
loc:
	python manage.py makemessages -l ru

# Компилировать локали
loc_comp:
	python manage.py compilemessages

lint:
	poetry run flake8 .
