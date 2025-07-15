from dotenv import load_dotenv
import os

from app.services.create_iam import create_iam_token

load_dotenv()

YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")
YANDEX_IAM_TOKEN = create_iam_token()
NINJAS_API_KEY = os.getenv("NINJAS_API_KEY")
API_LAYER_KEY = os.getenv("API_LAYER_KEY")
KEYS_PATH = os.getenv("KEYS_PATH", "app/core/keys.json")
YANDEX_API_URL = os.getenv(
    "YANDEX_API_URL", "https://llm.api.cloud.yandex.net/foundationModels/v1/completion")

NINJAS_API_URL = os.getenv(
    "NINJAS_API_URL", "https://api.api-ninjas.com/v1/sentiment")
APILAYER_URL = os.getenv(
    "APILAYER_URL", "https://api.apilayer.com/spamchecker?threshold={threshold}")

