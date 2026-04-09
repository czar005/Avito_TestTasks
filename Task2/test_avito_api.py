import requests
import random
import re
import pytest

BASE_URL = "https://qa-internship.avito.com/api/1"

def generate_seller_id():
    return random.randint(111111, 999999)

def extract_id_from_status(response_json):
    """Парсим id из строки status: 'Сохранили объявление - <uuid>'"""
    match = re.search(r'Сохранили объявление - (\S+)', response_json.get("status", ""))
    if match:
        return match.group(1)
    return None

def create_item(seller_id=None):
    if seller_id is None:
        seller_id = generate_seller_id()
    payload = {
        "sellerID": seller_id,
        "name": "Тестовое объявление",
        "price": 1000,
        "statistics": {
            "likes": 1,
            "viewCount": 1,
            "contacts": 1
        }
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{BASE_URL}/item", json=payload, headers=headers)
    print(response.status_code, response.text)  # дебаг
    return response

def get_item(item_id):
    return requests.get(f"{BASE_URL}/item/{item_id}")

def get_items_by_seller(seller_id):
    return requests.get(f"{BASE_URL}/{seller_id}/item")

def get_statistics(item_id):
    return requests.get(f"{BASE_URL}/statistic/{item_id}")


# Тесты

def test_create_item_success():
    response = create_item()
    assert response.status_code == 200
    item_id = extract_id_from_status(response.json())
    assert item_id is not None, "Не удалось извлечь id из ответа"
    print("Созданный id:", item_id)

def test_create_item_missing_sellerID():
    payload = {
        "name": "Тестовое объявление",
        "price": 1000,
        "statistics": {"likes":1, "viewCount":1, "contacts":1}
    }
    response = requests.post(f"{BASE_URL}/item", json=payload)
    assert response.status_code == 400

def test_get_item_success():
    response_create = create_item()
    assert response_create.status_code == 200
    item_id = extract_id_from_status(response_create.json())
    assert item_id is not None
    response = get_item(item_id)
    assert response.status_code == 200
    data_list = response.json()
    assert isinstance(data_list, list) and len(data_list) > 0
    data = data_list[0]  # берём первый объект
    assert "id" in data
    assert data["id"] == item_id

def test_get_statistics_success():
    response_create = create_item()
    item_id = extract_id_from_status(response_create.json())
    assert item_id is not None
    response = get_statistics(item_id)
    assert response.status_code == 200
    stats_list = response.json()
    assert isinstance(stats_list, list) and len(stats_list) > 0
    stats = stats_list[0]  # берём первый объект
    assert "likes" in stats and "viewCount" in stats and "contacts" in stats

def test_get_nonexistent_item():
    response = get_item("non-existent-id")
    assert response.status_code in [404, 400]

def test_get_items_by_seller_success():
    seller_id = generate_seller_id()
    id1 = extract_id_from_status(create_item(seller_id=seller_id).json())
    id2 = extract_id_from_status(create_item(seller_id=seller_id).json())
    response = get_items_by_seller(seller_id)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Вернулись хотя бы созданные объявления
    returned_ids = [item.get("id") for item in data]
    assert id1 in returned_ids
    assert id2 in returned_ids

def test_get_items_by_nonexistent_seller():
    response = get_items_by_seller(99999999)
    assert response.status_code in [404, 200]

def test_get_item_success():
    response_create = create_item()
    assert response_create.status_code == 200
    item_id = extract_id_from_status(response_create.json())
    assert item_id is not None
    response = get_item(item_id)
    assert response.status_code == 200
    data_list = response.json()
    assert isinstance(data_list, list) and len(data_list) > 0
    data = data_list[0]  # берём первый объект
    assert "id" in data
    assert data["id"] == item_id

def test_get_statistics_nonexistent_item():
    response = get_statistics("non-existent-id")
    assert response.status_code in [404, 400]

def test_response_time():
    response = create_item()
    assert response.elapsed.total_seconds() < 10