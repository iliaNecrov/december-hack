# december-hack

Frontend - https://github.com/ragen1337/moex-hack

Backend состоит из нескольких независимых модулей - stocks, chatbot, forecasting, strategies

В main.py реализованы все необходимые роуты. API - https://acoustic-snap-63d.notion.site/Api-d6c31b42c65b4b7d89272fb56d7e10a6?pvs=4

Для запуска:
1) cd src
2) uvicorn main:app --host 0.0.0.0 --port 8000

В strategies есть модуль rl - библиотека для создания агентов, обученных при помощи Reinforcement Learning.
