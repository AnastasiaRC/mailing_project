# Проект по отправке рассылок и их настройке

Цель проекта: автоматическая рассылка пользователям на почту, согласно настройкам.

Для работы программы необходимо:

1. Склонировать репозиторий в PyCharm (команда: git clone https://github.com/AnastasiaRC/mailing_project.git)
2. Установить зависимости, из файла requirements.txt
3. Заполнить файл .env своими данными
4. Cоздайте миграции: python manage.py makemigrations
5. Примените миграции: python manage.py migrate
6. Запустить команду python3 manage.py crontab add для добавления задачи планировщика
7. Запустить команду python3 manage.py csu для создания Суперпользователя
8. Запустить команду python3 manage.py cmg для создания группы "Контент-менеджер" и пользователя
9. Запустить команду python3 manage.py mg для создания группы "Менеджер" и пользователя

Описание приложений:

- mailing: создание и управление рассылками
- users: верификация, регистрация, авторизация пользователей
- blog: управление и редактирование статей для продвижения сервиса
- clients: создание и управление клиентами рассылок
- message: создание и настройка сообщениями рассылки

Кеширование:

Для блога и главной страницы

Права доступа:

- Пользователь (Вход, Регистрация с подтверждением по почте, не может изменить чужую рассылку но может работать со своим списком клиентов и со своим списком рассылок.)

- Менеджер (Может просматривать любые рассылки, список пользователей сервиса, блокировать пользователей сервиса, отключать рассылки.
Не может редактировать рассылки, управлять списком рассылок, изменять рассылки и сообщения.)

- Контент-менеджер (Может управлять блогом)
