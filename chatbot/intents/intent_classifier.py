from .google_intent.google_news import GoogleNewsIntent
from .database_intent.algo_database import DatabaseIntent
from gpt_api import GPT_API as gpt
import warnings


class IntentClassifier:
    intents = {"новости": GoogleNewsIntent, "goalgo": DatabaseIntent}

    @staticmethod
    def get_prompt(message: str) -> str:
        """
        Классификация сообщения на основе примеров few-shot
        """
        return (f"""Классифицируй intent на основе следующей информации:\n\n"""
                f""""goalgo" - информация по порталу goalgo (algo pack, алго пак), специфические термины, касающиеся биржи.\n"""
                f""""новости" - если пользователь спросит новости относительно какой-либо компании\n"""
                f""""другое" - все остальное, что не подходит по описанию к новостям или goalgo\n\n"""
                f"""Пожалуйста предоставь информацию по акциям сбербанка": {{"intent": "новости"}}\n"""
                f"""Опиши данные goalgo: {{"intent": "goalgo"}}\n"""
                f"""Что означает параметр cancel_orders_b в данных?": {{"intent": "goalgo"}}\n"""
                f"""Как зовут собаку, которая ждала своего хозяина?": {{"intent": "другое"}}\n"""
                f"""Какие новости Тинькоффа на рынке?": {{"intent": "новости"}}\n"""
                f"""Привет, как дела?": {{"intent": "другое"}}\n"""
                f"""{message}: """)
    
    @classmethod
    def get_answer(cls, message: str) -> str:
        """
        После определения интента, используем не обходимый класс для ответа
        на пользовательское сообщение, возвращаем полученный ответ

        В случае если сообщение не классифицировано ни как "новости", ни как "goalgo"
        отправляем обычный запрос в GPT без промпта
        """
        prompt = cls.get_prompt(message)
        intent_class = gpt.get_response(prompt, json_output=True)["intent"]

        warnings.warn(f"Класс намерения: {intent_class}")

        if intent_class not in cls.intents:
            return gpt.get_response(message)
        
        intent = cls.intents[intent_class]

        return intent.get_result(message)
        

