[![Static Badge](https://img.shields.io/badge/Телеграм-Наш_канал-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/hidden_coding)

[![Static Badge](https://img.shields.io/badge/Телеграм-Наш_чат-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/hidden_codding_chat)

[![Static Badge](https://img.shields.io/badge/Телеграм-Ссылка_на_бота-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/blum/app?startapp=ref_WyOWiiqWa4)

## Рекомендация перед использованием

# 🔥🔥 Используйте PYTHON версии 3.10 🔥🔥

> 🇪🇳 README in english available [here](README-EN)

## Функционал  
|                   Функционал                   | Поддерживается |
|:----------------------------------------------:|:--------------:|
|                Многопоточность                 |       ✅        | 
|            Привязка прокси к сессии            |       ✅        | 
| Авто-регистрация аккаунта по вашей реф. ссылке |       ✅        |
|     Авто игра с выбором рандомных поинтов      |       ✅        |
|     Поддержка telethon И pyrogram .session     |       ✅        |

_Скрипт осуществляет поиск файлов сессий в следующих папках:_
* /sessions
* /sessions/pyrogram
* /session/telethon


## [Настройки](https://github.com/SP-l33t/Blum-Telethon/blob/main/.env-example/)
|          Настройки          |                                                                                                                              Описание                                                                                                                               |
|:---------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|    **API_ID / API_HASH**    |                                                                                         Данные платформы, с которой будет запущена сессия Telegram (по умолчанию - android)                                                                                         |
|   **GLOBAL_CONFIG_PATH**    | Определяет глобальный путь для accounts_config, proxies, sessions. <br/>Укажите абсолютный путь или используйте переменную окружения (по умолчанию - переменная окружения: **TG_FARM**)<br/> Если переменной окружения не существует, использует директорию скрипта |
|        **FIX_CERT**         |                                                                                              Попытаться исправить ошибку SSLCertVerificationError ( True / **False** )                                                                                              |
|    **TRACK_BOT_UPDATES**    |                                                                         Отслеживать обновления бота и останавливать бота, если были обновления, для проверки изменений ( **True** /False )                                                                          |
|       **PLAY_GAMES**        |                                                                                                    Играть в игры или просто запускать фарм (по умолчанию - True)                                                                                                    |
|     **GAMES_PER_CYCLE**     |                                                                                                               Количество игр за цикл (**[min, max]**)                                                                                                               |
|         **POINTS**          |                                                                                              Кол-во очков за игру (по умолчанию - [190, 230] (То есть от 190 до 230))                                                                                               |
|   **SESSION_START_DELAY**   |                                                                                     Рандомная задержка в секундах для сессий (от 1 до указанного значения. По умолчанию - 360)                                                                                      |
|         **USE_REF**         |                                                                                          Регистрировать ваши аккаунты по вашей реф. ссылке или нет (по умолчанию - False)                                                                                           |
|         **REF_ID**          |                                                                                               Ваш реферальный аргумент (идет после app/startapp? в вашей реф. ссылке)                                                                                               |
|   **SESSIONS_PER_PROXY**    |                                                                                           Количество сессий, которые могут использовать один прокси (По умолчанию **1** )                                                                                           |
|   **USE_PROXY_FROM_FILE**   |                                                                                             Использовать ли прокси из файла `bot/config/proxies.txt` (**True** / False)                                                                                             |
|  **DISABLE_PROXY_REPLACE**  |                                                                                   Отключить автоматическую проверку и замену нерабочих прокси перед стартом ( True / **False** )                                                                                    |
|      **DEVICE_PARAMS**      |                                                                                  Вводить параметры устройства, чтобы сделать сессию более похожую, на реальную  (True / **False**)                                                                                  |
|      **DEBUG_LOGGING**      |                                                                                               Включить логирование трейсбэков ошибок в папку /logs (True / **False**)                                                                                               |

## Быстрый старт 📚

Для быстрой установки и последующего запуска - запустите файл run.bat на Windows или run.sh на Линукс

## Предварительные условия
Прежде чем начать, убедитесь, что у вас установлено следующее:
- [Python](https://www.python.org/downloads/) **версии 3.10**

## Получение API ключей
1. Перейдите на сайт [my.telegram.org](https://my.telegram.org) и войдите в систему, используя свой номер телефона.
2. Выберите **"API development tools"** и заполните форму для регистрации нового приложения.
3. Запишите `API_ID` и `API_HASH` в файле `.env`, предоставленные после регистрации вашего приложения.

## Установка
Вы можете скачать [**Репозиторий**](https://github.com/SP-l33t/Blum-Telethon) клонированием на вашу систему и установкой необходимых зависимостей:
```shell
git clone https://github.com/SP-l33t/Blum-Telethon.git
cd Blum-Telethon
```

Затем для автоматической установки введите:

Windows:
```shell
run.bat
```

Linux:
```shell
run.sh
```

# Linux ручная установка
```shell
sudo sh install.sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cp .env-example .env
nano .env  # Здесь вы обязательно должны указать ваши API_ID и API_HASH , остальное берется по умолчанию
python3 main.py
```

Также для быстрого запуска вы можете использовать аргументы, например:
```shell
~/Blum-Telethon >>> python3 main.py --action (1/2)
# Or
~/Blum-Telethon >>> python3 main.py -a (1/2)

# 1 - Запускает кликер
# 2 - Создает сессию
```


# Windows ручная установка
```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env-example .env
# Указываете ваши API_ID и API_HASH, остальное берется по умолчанию
python main.py
```

Также для быстрого запуска вы можете использовать аргументы, например:
```shell
~/Blum-Telethon >>> python main.py --action (1/2)
# Или
~/Blum-Telethon >>> python main.py -a (1/2)

# 1 - Запускает кликер
# 2 - Создает сессию
```


### Благодарность:
Огромная благодарность [sanjithacks](https://github.com/sanjithacks) за помощь с локальным шифрованием для игр. ♥
