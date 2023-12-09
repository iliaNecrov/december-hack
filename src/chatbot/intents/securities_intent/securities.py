from moexalgo import Ticker
from datetime import datetime, timedelta
from typing import Tuple
from ...gpt_api import GPT_API as gpt
import pandas as pd
from tabulate import tabulate


class SecuritiesIntent:
    available_tickers = ["SBER", "OZON", "YNDX", "TCSG"]
    columns_to_use = ['ts', 'pr_open', 'pr_high', 'pr_low', 'pr_close']
    columns_to_replace = {
                            "ts": "Date",
                            "pr_open": "Open",
                            "pr_high": "Close",
                            "pr_low": "MIN",
                            "pr_close": "MAX"
                         }

    @staticmethod
    def _preprocess_data(ticker: str, start_date: str, end_date: str) -> Tuple[str, str, str]:
        """
        Предобработка данных
        """

        if isinstance(ticker, str):
            ticker = ticker.upper()

        if not start_date:
            # Если нет даты в сообщении, смотрим новости за последнюю нелелю
            start_date = end_date = (datetime.now() - timedelta(weeks=1)).date().strftime("%Y-%m-%d")
            end_date = datetime.now().date().strftime("%Y-%m-%d")

        if not end_date:
            # Если нет даты окончания, то делаем ее такой же как и дата начала
            end_date = start_date

        return ticker, start_date, end_date

    @staticmethod
    def _make_grid_table(data: pd.DataFrame) -> str:
        """
        Сделать строчную таблицу для вывода в UI
        """
        return tabulate(data, headers = "keys", tablefmt='grid')


    def __prepare_output_table(self, data: pd.DataFrame) -> str:
        """
        Перевести пандас в строку и вывести только head и tail
        """
        # убрать секунды из датафрейма
        data['Date'] = pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d %H:%M')

        # длина нашей таблица и серединное значение
        length = len(self._make_grid_table(data.tail()).split("\n")[0])
        middle = int(length/2)
        # добавление сепаратора для верхней части таблицы и нижней
        string = " "*length
        separator_string = "|" + string[1:middle-3] + '...' + string[middle:-1] + "|"
        # верхняя и нижняя часть таблицы для вывода
        head = self._make_grid_table(data.head())
        tail = "\n".join(self._make_grid_table(data.tail()).split("\n")[2:])
        # table adjuster
        data.rename(columns={"Date": "Date                           1"}, inplace=True) 

        return "\n".join([head, separator_string, tail]).replace("=", '-')

    @staticmethod
    def get_prompt(message: str) -> str:
        """
        Создать промпт GPT для парсинга запроса на цены акций
        """
        today = datetime.now().date().strftime("%Y-%m-%d")
        yesturday = (datetime.now().date() - timedelta(days=1)).strftime("%Y-%m-%d")
        two_days_ago = (datetime.now().date() - timedelta(days=2)).strftime("%Y-%m-%d")

        prompt = (
            f"""Из сообщения пользователя выдели в json имя тикера, стартовую дату и дату окончания, опираясь на информацию. Если имя тикера/даты старта/даты окончания нет, выдай null в значении json словаря\n"""
            f"""Возможные тикеры: Яндекс(Yandex): "YNDX", Сбербанк(Sberbank): "SBER", Озон(Ozon): "OZON", Тинькофф(Tinkoff): "TCSG"\n\n"""
            f"""Дата сегодня: {today}\n\n"""
            f"""Выведи таблицу акций сбербанка за сегодня: {{"ticker": "SBER", "start_date": "{today}", "end_date": null}}\n"""
            f"""Выдай акции Тинькофф за с 24 по 26 декабря: {{"ticker": "TCSG", "start_date": "2023-12-24", "end_date": "2023-12-26"}}\n"""
            f"""Стоимость Озона: {{"ticker": "OZON", "start_date": null, "end_date": null}}\n"""
            f"""Информация по акциям Яндекса: {{"ticker": "YNDX", "start_date": "{yesturday}", "end_date": null}}\n"""
            f"""Акции за 2 дня назад: {{"ticker": null, "start_date": "{two_days_ago}", "end_date": null}}\n"""
            f"""Акции Тинькова за сегодняшний день: {{"ticker": "TCSG", "start_date": "{today}", "end_date": null}}\n"""
            f"""{message}: """
        )

        return prompt
    
    def get_ticker_info(self, message: str) -> dict:
        """
        Составить промпт для парсинга, а после получить спаршенную информацию в json формате
        пример return-a: {"ticker": "OZON", "start_date": null, "end_date": null}
        """
        prompt = self.get_prompt(message)
        return gpt.get_response(prompt, json_output=True)

    def get_table(self, ticker: str, start_date: str, end_date: str) -> str:
        """
        Получить табличную информацию об акциях через API, преобразовать в строку
        """

        # Исправить данные
        ticker, start_date, end_date = self._preprocess_data(ticker, start_date, end_date)

        # На случай если тикера нет или его нет в списке
        if ticker not in self.available_tickers:
            return "К сожалению не найдена информация по данной организации"

        # Получение данных по API
        table = Ticker(ticker).tradestats(date=start_date, till_date=end_date)

        if not isinstance(table, pd.DataFrame):
            table = pd.DataFrame(table)

        # В случае если данные в таблице отсутствуют, сообщаем об этом пользователю
        if len(table) == 0:
            return "Нет данных за данный временной интервал!"
        
        # Используем ограниченное количество столбцов и переименовываем в удобный для нас формат
        table = table[self.columns_to_use]
        table.rename(columns=self.columns_to_replace, inplace=True)

        return self.__prepare_output_table(table)
        
    
    @classmethod
    def get_result(cls, message: str) -> str:
        """
        Получить таблицу цен акций по заданной дате
        """
        ticker_info = cls().get_ticker_info(message)

        table = cls().get_table(**ticker_info)

        return table