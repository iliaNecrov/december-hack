# GOALGO HACK
Наше решение представляет собой MVP сервиса помощи инвесторам в принятии торговых решений.
В нём используются современные технологии обучения с подкреплением, обработки естественного языка и прогнозирования.
Сервис позволяет пользователю создавать персонализированные стратегии.

Решение в данном репозитории предоставляется для участия как в основной части соревнования, так и в дополнительных номинациях.

Frontend - https://github.com/ragen1337/moex-hack

# Техническая часть

Backend состоит из нескольких независимых модулей - stocks, chatbot, forecasting, strategies

В main.py реализованы все необходимые роуты. API - https://acoustic-snap-63d.notion.site/Api-d6c31b42c65b4b7d89272fb56d7e10a6?pvs=4

Для запуска:
1) cd src
2) uvicorn main:app --host 0.0.0.0 --port 8000

В strategies есть модуль rl - библиотека для создания агентов, обученных при помощи Reinforcement Learning.

# Контакты

При проблеме с запуском - https://t.me/kimbrisvv
