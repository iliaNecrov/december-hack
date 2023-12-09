import json
import requests
from typing import Union

class GPT_API:
    url = "https://api.theb.ai/v1/chat/completions"
    headers = {
        'Authorization': 'Bearer sk-JApJa6EYfVf0193B3PLTVGhlQi5BSQ9fKAZRLDnJVP9UalpI',
        'Content-Type': 'application/json'
            }
    
    @staticmethod
    def _create_gpt_message(prompt: str) -> dict:
        '''
        Создает GPT формат для отправки с сообщением (промптом) и выбранной моделью)
        '''
        return json.dumps({
          "model": "gpt-3.5-turbo",
          "messages": [{"role": "user", "content": prompt}],
          "stream": False })

    @classmethod
    def get_response(cls, message: str, json_output: bool = False) -> Union[str, dict]:
        '''
        Отправляет запрос с нужным промптом и получает ответ в текстовом или json представлении
        '''
        response =  requests.request("POST", cls.url, headers=cls.headers, 
                        data=cls._create_gpt_message(message)).json()["choices"][0]["message"]["content"]
                        
        if json_output:
            return json.loads(response)

        return response
