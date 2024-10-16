# Task manager
***
![Hexlet Badge](https://img.shields.io/badge/Hexlet-116EF5?logo=hexlet&logoColor=fff&style=for-the-badge)
[![Actions Status](https://github.com/GrigoriyKruchinin/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/GrigoriyKruchinin/python-project-52/actions)
[![Check_linter](https://github.com/GrigoriyKruchinin/python-project-52/actions/workflows/lint_check.yml/badge.svg)](https://github.com/GrigoriyKruchinin/python-project-52/actions)
[![Tests](https://github.com/GrigoriyKruchinin/python-project-52/actions/workflows/run_tests.yml/badge.svg)](https://github.com/GrigoriyKruchinin/python-project-52/actions)
[![Test Coverage](https://api.codeclimate.com/v1/badges/9e4054d13d4b4b33f6a8/test_coverage)](https://codeclimate.com/github/GrigoriyKruchinin/python-project-52/test_coverage)
<!-- [![Maintainability](https://api.codeclimate.com/v1/badges/9e4054d13d4b4b33f6a8/maintainability)](https://codeclimate.com/github/GrigoriyKruchinin/python-project-52/maintainability) -->

__"Task manager__ - это сайт, который позволяет распределять задачи среди пользователей и следить за их выполнением.

***
## Перед установкой
Для установки и запуска проекта вам потребуется Python версии  3.10 и выше, инструмент для управления зависимостями Poetry.

Перед началом использования проекта убедитесь, что вышеописанные утилиты установлены на вашем устройстве. В противном случае используйте официальную документацию для установки.

## Установка

1. Склонируйте репозиторий с проектом на ваше локальное устройство:
```
git clone git@github.com:GrigoriyKruchinin/python-project-52.git
```
2. Перейдите в директорию проекта:
```
cd python-project-52
```
3. Установите необходимые зависимости с помощью Poetry:
```
poetry install
```
4. Создайте файл .env, который будет содержать ваши конфиденциальные настройки:

```
cp .env.sample .env
```

Откройте файл .env и ознакомтесь с его содержимым. Замените значение ключей SECRET_KEY и DATABASE_URL.

5. Выполните команды: 
```
make migrations
make migrate
```

***

## Использование
1. Для запуска сервера в продакшн среде с помощью Gunicorn выполните команду:

```
make start
```
По умолчанию сервер будет доступен по адресу http://0.0.0.0:8000.

2. Также можно запустить сервер локально в режиме разработки с активным отладчиком:

```
make dev
```
Сервер для разработки будет доступен по адресу http://127.0.0.1:5000.

3. Проект можно использовать онлайн (например с помощью стороннего сервиса [render.com](https://dashboard.render.com/)). Следуйте инструкциям с официального сайта для добавления веб-сервиса и онлайн базы данных. Не забывайте про использования переменных окружения.


***
## Контакты
- Автор: Grigoriy Kruchinin
- [GitHub](https://github.com/GrigoriyKruchinin)
- [Email](gkruchinin75@gmail.com)
- [LinkedIn](https://www.linkedin.com/in/grigoriy-kruchinin/)
***
