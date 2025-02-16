import pytest
import requests

# Базовый URL API
BASE_URL = "https://qa-internship.avito.com/api/1"


# Тест-кейс 1: Проверка успешного создания объявления
def test_create_ad_success():
    url = f"{BASE_URL}/item"
    payload = {
        "sellerID": 111111,
        "name": "Antoha",
        "price": 1,
        "statistics": {
            "contacts": 3,
            "likes": 123,
            "viewCount": 12
        }
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    assert "Сохранили объявление -" in response.text


# Тест-кейс 2: Проверка успешного создания объявления с дробным значением цены
def test_create_ad_with_float_price():
    url = f"{BASE_URL}/item"
    payload = {
        "sellerID": 111111,
        "name": "Antoha",
        "price": 1.9,
        "statistics": {
            "contacts": 3,
            "likes": 123,
            "viewCount": 12
        }
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    assert "Сохранили объявление -" in response.text


# Тест-кейс 3: Проверка создания объявления с отрицательными числовыми значениями
def test_create_ad_with_negative_values():
    url = f"{BASE_URL}/item"
    payload = {
        "sellerID": 111111,
        "name": "Antoha",
        "price": -1,
        "statistics": {
            "contacts": -3,
            "likes": -123,
            "viewCount": -12
        }
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 400
    assert "message" in response.json()


# Тест-кейс 4: Попытка отправки запроса без поля name
def test_create_ad_without_name():
    url = f"{BASE_URL}/item"
    payload = {
        "sellerID": 111111,
        "price": 1,
        "statistics": {
            "contacts": 3,
            "likes": 123,
            "viewCount": 12
        }
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 400
    assert "message" in response.json()


# Тест-кейс 5: Успешный запрос на получение объявления по валидному ID
def test_get_ad_by_valid_id():
    ad_id = "648c6163-86dd-4769-91cd-3ebd584c4891"
    url = f"{BASE_URL}/item/{ad_id}"
    response = requests.get(url)

    # Проверка статус-кода
    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"

    # Проверка структуры и значений ответа
    response_json = response.json()

    # Если ответ — это список, берем первый элемент
    if isinstance(response_json, list):
        response_json = response_json[0]  # Берем первый элемент списка

    # Проверка поля id
    assert response_json["id"] == ad_id, f"Ожидался id {ad_id}, получен {response_json['id']}"

    # Проверка поля name
    assert response_json["name"] == "Antoha", f"Ожидалось name 'dsdsd', получено {response_json['name']}"

    # Проверка поля price
    assert response_json["price"] == 1, f"Ожидался price 1, получен {response_json['price']}"

    # Проверка поля sellerId
    assert response_json["sellerId"] == 112113, f"Ожидался sellerId 111113, получен {response_json['sellerId']}"

    # Проверка поля statistics
    statistics = response_json["statistics"]
    assert statistics["contacts"] == 35, f"Ожидалось contacts 35, получено {statistics['contacts']}"
    assert statistics["likes"] == 9, f"Ожидалось likes -8, получено {statistics['likes']}"
    assert statistics["viewCount"] == -12, f"Ожидалось viewCount -12, получено {statistics['viewCount']}"

# Тест-кейс 6: Попытка получения объявления по невалидному ID
def test_get_ad_by_invalid_id():
    ad_id = "563bd265-49d1-44da-b1ce-0e3a5d664000"
    url = f"{BASE_URL}/item/{ad_id}"
    response = requests.get(url)

    # Проверка статус-кода
    assert response.status_code == 404, f"Ожидался статус-код 404, получен {response.status_code}"

    # Проверка наличия ключа "result" в ответе
    assert "result" in response.json(), "Ключ 'result' отсутствует в ответе"

    # Проверка структуры и содержимого ответа
    response_json = response.json()
    assert response_json["status"] == "404", f"Ожидался статус '404', получен {response_json['status']}"
    assert response_json["result"]["message"] == f"item {ad_id} not found", \
        f"Ожидалось сообщение 'item {ad_id} not found', получено '{response_json['result']['message']}'"
    assert response_json["result"]["messages"] is None, "Поле 'messages' должно быть null"

# Тест-кейс 7: Успешный запрос на получение объявлений продавца по валидному ID
def test_get_ads_by_valid_seller_id():
    seller_id = "111113"
    url = f"{BASE_URL}/{seller_id}/item"
    response = requests.get(url)
    assert response.status_code == 200
    for ad in response.json():
        assert ad["sellerId"] == int(seller_id)

# Тест-кейс 8: Попытка получения объявлений продавца по невалидному ID
def test_get_ads_by_invalid_seller_id():
    seller_id = "11111G"
    url = f"{BASE_URL}/{seller_id}/item"
    response = requests.get(url)
    assert response.status_code == 400
    assert "передан некорректный идентификатор продавца" in response.json()["result"]["message"]


# Тест-кейс 9: Успешный запрос на получение статистики объявления по валидному ID
def test_get_statistics_by_valid_ad_id():
    ad_id = "72ccc331-b760-406d-a460-64eee3940f98"
    url = f"{BASE_URL}/statistic/{ad_id}"
    response = requests.get(url)

    # Проверка статус-кода
    assert response.status_code == 200, f"Ожидался статус-код 200, получен {response.status_code}"

    # Проверка структуры и значений ответа
    response_json = response.json()

    # Если ответ — это список, берем первый элемент
    if isinstance(response_json, list):
        response_json = response_json[0]  # Берем первый элемент списка

    # Проверка поля contacts
    assert response_json["contacts"] == 35, f"Ожидалось contacts 35, получено {response_json['contacts']}"

    # Проверка поля likes
    assert response_json["likes"] == 9, f"Ожидалось likes 8, получено {response_json['likes']}"

    # Проверка поля viewCount
    assert response_json["viewCount"] == 12, f"Ожидалось viewCount 12, получено {response_json['viewCount']}"


# Тест-кейс 10: Попытка получения статистики объявления по невалидному ID
def test_get_statistics_by_invalid_ad_id():
    ad_id = "ff23c626-874e-406d-90ed-f29d99144f00"
    url = f"{BASE_URL}/statistic/{ad_id}"
    response = requests.get(url)
    assert response.status_code == 404
    assert f"statistic {ad_id} not found" in response.json()["result"]["message"]
