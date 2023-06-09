# YouTubebot
Бот, который получает на входе ссылку на видеоролик YouTube. в ответ присылает пользователю аудиотрек, полученный из видеоролика. 
Также бот, пытается полученный аудиотрек проверить черех Shazam (правда эта часть кода у меня заработала только под линуксом, поэтому 
эта часть кода в модуле common.py платорфо-зависимая).
Что нужно для работы приложения:
Установить пакеты (в виртуальное окружение): aiogram, pytube, shazamio, dotenv.
В корне приложения создать файл с переменными окружения (по умолчанию название файла app.env), в который надо добать строку
yt_token="Ваш Токен Телеграмм бота"
Для работы блока кода из модуля shazamio (распознование аудиотрека) я под Debian дополнительно установил пакет ffmpeg (sudo apt install ffmpeg).
Бот развернут на VPS (Debian 10), версия питона 3.11.3, запуск осуществляется через systemd.