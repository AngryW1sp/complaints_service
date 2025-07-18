# complaints_service

Сервис для сбора и анализа пользовательских жалоб с использованием FastAPI, YandexGPT, API Ninjas и API Layer.

## Быстрый старт

1. Клонируйте репозиторий и установите зависимости:
    ```sh
    git clone <ваш-репозиторий>
    cd complaints_service
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```

2. Создайте файл `.env` в корне проекта и укажите ваши ключи и токены:

### Пример `.env`

```properties
YANDEX_FOLDER_ID=ваш_foulder_id
YANDEX_IAM_TOKEN=ваш_yandex_iam_token
NINJAS_API_KEY=ваш_ninjas_api_key
API_LAYER_KEY=ваш_api_layer_key
KEYS_PATH=app/services/authorized_key.json
YANDEX_API_URL=https://llm.api.cloud.yandex.net/foundationModels/v1/completion
NINJAS_API_URL=https://api.api-ninjas.com/v1/sentiment
APILAYER_URL=https://api.apilayer.com/spamchecker?threshold={threshold}
```

**Внимание:**  
- Все ключи и токены должны быть действующими.
- Файл `authorized_key.json` для Yandex.Cloud должен быть размещён по пути, указанному в `KEYS_PATH`.

3. Инициализируйте базу данных:
    ```bash
    python create_db.py
    ```

4. Запустите сервис:
    ```bash
    run.bat
    ```

## Переменные окружения

- `YANDEX_FOLDER_ID` — ID каталога Yandex.Cloud.
- `YANDEX_IAM_TOKEN` — IAM токен для доступа к YandexGPT.
- `NINJAS_API_KEY` — API-ключ для сервиса API Ninjas.
- `API_LAYER_KEY` — API-ключ для сервиса API Layer.
- `KEYS_PATH` — путь к файлу с сервисным ключом Yandex.Cloud.
- `YANDEX_API_URL` — URL для запроса к YandexGPT.
- `NINJAS_API_URL` — URL для анализа сентимента.
- `APILAYER_URL` — URL для проверки текста на спам.

## Примеры запросов

### Создать жалобу

**curl:**
```sh
curl -X POST "http://localhost:8000/complaints/" ^
     -H "Content-Type: application/json" ^
     -d "{\"text\": \"У меня не работает оплата\"}"
```

**Postman:**
- Метод: POST
- URL: http://localhost:8000/complaints/
- Body: raw, JSON
```json
{
  "text": "У меня не работает оплата"
}
```

---

### Получить жалобы за последний час

**curl:**
```sh
curl -X GET "http://localhost:8000/complaints/"
```

**Postman:**
- Метод: GET
- URL: http://localhost:8000/complaints/

---

### Обновить статус жалобы

**curl:**
```sh
curl -X PATCH "http://localhost:8000/complaints/1" ^
     -H "Content-Type: application/json" ^
     -d "{\"status\": \"closed\"}"
```

**Postman:**
- Метод: PATCH
- URL: http://localhost:8000/complaints/1
- Body: raw, JSON
```json
{
  "status": "closed"
}
```
