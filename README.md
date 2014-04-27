## Описание
Хендлеры определены в handlers/gateways.py. Функция get_handler определена в handlers/views.py. Кроме двух требуемых хендлеров для smsc.ru и smstraffic.ru реализован простейший хендлер для реального API smsc.ru - для его использования необходимо определить SMSC_LOGIN и SMSC_PASSWORD в settings.py или localsettings.py.

Доступен минимальный веб-интерфейс для отправки сообщения и просмотра логов.
Логи хранятся в БД (sqlite3).

## Установка и использование

    make deps
    make assets
    ./manage.py runserver
