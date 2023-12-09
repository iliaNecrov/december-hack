from ...gpt_api import GPT_API as gpt
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import os

PATH = "chatbot/intents/database_intent/data"

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens")
vectordb = Chroma(persist_directory=PATH, embedding_function=embeddings)

class DatabaseIntent:

    @staticmethod
    def create_structed_text(documents: list) -> str:
        return "\n\n".join([document.page_content for document in documents])

    @staticmethod
    def create_prompt(question: str, document_info: list) -> str:
        return f"Основываясь на информации ниже, отвеь на вопрос пользователя:\n [ИНФОРМАЦИЯ]\n{document_info} [ВОПРОС]\n{question}"

    @classmethod
    def get_result(cls, message:str) -> str:
        possible_documents = vectordb.similarity_search(message)
        document_info = cls.create_structed_text(possible_documents)
        prompt = cls.create_prompt(message, document_info)
        return gpt.get_response(prompt)