import os
import requests
import logging
from dotenv import load_dotenv

from app.core.config import NINJAS_API_URL, YANDEX_API_URL, APILAYER_URL

load_dotenv()
logger = logging.getLogger(__name__)


class ApisInterface:
    def __init__(self, **kwargs):
        self.iam_token = kwargs.get('iam_token')
        self.folder_id = kwargs.get('folder_id')
        self.x_api_key = kwargs.get('x_api_key')
        self.user_text = kwargs.get('user_text')
        self.api_layer_key = kwargs.get('api_layer_key')
        self.ip = kwargs.get('ip')

    def yandexapi(self) -> str:
        """Определяет категорию жалобы через YandexGPT."""
        try:
            data = {
                "modelUri": f"gpt://{self.folder_id}/yandexgpt",
                "completionOptions": {"temperature": 0.3, "maxTokens": 1000},
                "messages": [
                    {"role": "system", "text": "Определи категорию жалобы. Варианты: техническая, оплата, другое. Ответь одним словом."},
                    {"role": "user", "text": self.user_text},
                ]
            }
            response = requests.post(
                YANDEX_API_URL,
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.iam_token}"
                },
                json=data,
                timeout=10
            )
            response.raise_for_status()
            result = response.json().get('result', {}).get('alternatives', [{}])[
                0].get('message', {}).get('text', '').strip()
            if len(result.join(' ').split()) > 1:
                result = result.join('')[-1]
            logger.info(f"Yandex API ответ: {result}")
            return result or "другое"
        except Exception as e:
            logger.error(f"Ошибка Yandex API: {e}", exc_info=True)
            return "другое"

    def ninjasapi(self) -> str:
        """Определяет сентимент жалобы через API Ninjas."""
        try:
            api_url = f"{NINJAS_API_URL}?text={self.user_text}"
            response = requests.get(
                api_url, headers={'X-Api-Key': self.x_api_key}, timeout=10)
            response.raise_for_status()
            sentiment = response.json().get('sentiment', 'unknown')
            logger.info(f"Ninjas API ответ: {sentiment}")
            return sentiment
        except Exception as e:
            logger.error(f"Ошибка Ninjas API: {e}", exc_info=True)
            return "unknown"

    def apilayer(self) -> bool:
        """Проверяет, является ли текст спамом через API Layer."""
        try:
            url = APILAYER_URL
            payload = self.user_text.encode("utf-8")
            headers = {
                "apikey": self.api_layer_key
            }
            response = requests.post(
                url, headers=headers, data=payload, timeout=10)
            response.raise_for_status()
            is_spam = response.json().get('is_spam', False)
            logger.info(f"API Layer ответ: {is_spam}")
            return is_spam
        except Exception as e:
            logger.error(f"Ошибка API Layer: {e}", exc_info=True)
            return False

    def get_ip_location(self) -> str:
        """Определяет регион по IP-адресу."""
        if not self.ip:
            logger.warning("IP не указан")
            return "не указано"
        try:
            response = requests.get(
                f"http://ip-api.com/json/{self.ip}?fields=8", timeout=10)
            response.raise_for_status()
            region = response.json().get('regionName', 'не указано')
            logger.info(f"Регион по IP: {region}")
            return region
        except Exception as e:
            logger.error(
                f"Ошибка определения региона по IP: {e}", exc_info=True)
            return "не указано"

    def run(self) -> dict:
        """Запускает все API и возвращает результаты."""
        return {
            "yandex": self.yandexapi(),
            "ninjas": self.ninjasapi(),
            "apilayer": self.apilayer(),
            "ip_location": self.get_ip_location()
        }
