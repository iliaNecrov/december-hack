import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from urllib.parse import quote
from typing import Tuple
#from gpt_api import GPT_API as gpt

from ...gpt_api import GPT_API as gpt


class GoogleNewsIntent:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }
    
    @staticmethod
    def _preprocess_data(company: str, start_date: str, end_date: str) -> Tuple[str, str, str]:
        """
        Предобработка данных
        """
        if not company: 
            # Если нет компании в сообщении, смотрим обычные "новости акций"
            company = "Новости Акций"

        if not start_date:
            # Если нет даты в сообщении, смотрим новости за сегодня
            start_date = end_date = datetime.now().date().strftime('%m/%d/%Y')

        if not end_date:
            # Если нет даты окончания, то делаем ее такой же как и дата начала
            end_date = start_date

        return company, start_date, end_date
    
    @staticmethod
    def get_prompt(message: str) -> str:
        """
        Создать промпт GPT для парсинга новостей
        """
        today = datetime.now().date().strftime('%m/%d/%Y')
        yesturday = (datetime.now().date() - timedelta(days=1)).strftime('%m/%d/%Y')
        two_days_ago = (datetime.now().date() - timedelta(days=2)).strftime('%m/%d/%Y')

        prompt = (
            f"""Из сообщения пользователя выдели в json имя компании, стартовую дату и дату окончания, опираясь на информацию. Если имя компании/даты старта/даты окончания нет, выдай null в значении json словаря\n\n"""
            f"""дата сегодня: {today}\n\n"""
            f"""Подскажи новости сбербанка за сегодня: {{"company": "Сбербанк", "start_date": "{today}", "end_date": null}}\n"""
            f"""Выдай новости Тинькофф за с 24 по 26 декабря: {{"company": "Тинькофф", "start_date": "12/24/2023", "end_date": "12/26/2023"}}\n"""
            f"""Новости Озона: {{"company": "Озон", "start_date": null, "end_date": null}}\n"""
            f"""Информация по компании НЛМК за вчера: {{"company": "НЛМК", "start_date": "{yesturday}", "end_date": null}}\n"""
            f"""Новости за 2 дня назад: {{"company": null, "start_date": "{two_days_ago}", "end_date": null}}\n"""
            f"""Акции Газпрома за сегодняшний день: {{"company": "Газпром", "start_date": "{today}", "end_date": null}}\n"""
            f"""{message}: """
        )

        return prompt
    
    def get_news_info(self, message: str) -> dict:
        """
        Составить промпт для парсинга, а после получить спаршенную информацию в json формате
        пример return-a: {"company": "Озон", "start_date": null, "end_date": null}
        """
        prompt = self.get_prompt(message)
        return gpt.get_response(prompt, json_output=True)

    def get_news(self, company: str, start_date: str, end_date: str) -> str:
        """
        Получить новости по API
        """
        # Исправить данные
        company, start_date, end_date = self._preprocess_data(company, start_date, end_date)

        # Заменить новости в нужный формат для отправки URL
        query_url = quote(company)
        
        # Задать URL со всеми параметрами запроса
        url = f"https://www.google.com/search?start=0&q={query_url}&tbm=nws&tbs=cdr:1,cd_min:{start_date},cd_max:{end_date},sbd:1&lr=lang_ru"
        
        response = requests.get(url, headers=self.headers)

        soup = BeautifulSoup(response.content, "html.parser")
        news_results = []

        news = ""
        for el in soup.select("div.SoaBEf")[:5]: # парсим html, берем первые 5 новости
            title = "Заголовок: {}".format(el.select_one("div.MBeuO").get_text().strip(" \t\n"))
            snippet = "Содежание: {}".format(el.select_one(".GI74Re").get_text().strip(" \t\n"))
            one_news = " \n".join([title, snippet]) + "\n\n"
            # собираем все новости воедино
            news += one_news
        return news.strip('\n')
    
    @classmethod
    def get_result(cls, message: str) -> str:
        """
        Получить суммаризацию по новостям
        """
        news_info = cls().get_news_info(message)
        news = cls().get_news(**news_info)

        if not news.strip():
            return 'Не найдено новостей по данному запросу!'

        return gpt.get_response(f"Суммаризируй новости тезисно по пунктам:\n {news}")