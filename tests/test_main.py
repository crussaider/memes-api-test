import os
import pytest
import requests

BASE_URL = "http://localhost:8000"
IMAGE_PATH_1 = os.path.join(os.getcwd(), 'tests/images', 'test.png')
IMAGE_PATH_2 = os.path.join(os.getcwd(), 'tests/images', 'test2.png')


@pytest.fixture(scope="module")
def setup_teardown():
    yield


def test_get_memes(setup_teardown):
    response = requests.get(f"{BASE_URL}/memes")
    assert response.status_code == 200
    assert "total" in response.json()
    assert "memes" in response.json()


def test_create_meme(setup_teardown):
    files = {'file': open(IMAGE_PATH_1, 'rb')}
    data = {'title': 'Test Meme 1'}
    response = requests.post(f"{BASE_URL}/memes", files=files, params=data)
    print(response.json())
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["title"] == "Test Meme 1"


def test_get_meme(setup_teardown):
    files = {'file': open(IMAGE_PATH_2, 'rb')}
    data = {'title': 'Test Meme 2'}
    create_response = requests.post(f"{BASE_URL}/memes", files=files, params=data)
    assert create_response.status_code == 201
    meme_id = create_response.json()["id"]

    response = requests.get(f"{BASE_URL}/memes/{meme_id}")
    assert response.status_code == 200
    assert response.json()["id"] == meme_id


def test_update_meme(setup_teardown):
    files = {'file': open(IMAGE_PATH_1, 'rb')}
    data = {'title': 'Test Meme'}
    create_response = requests.post(f"{BASE_URL}/memes", files=files, params=data)
    assert create_response.status_code == 201
    meme_id = create_response.json()["id"]

    new_files = {'file': open(IMAGE_PATH_2, 'rb')}
    new_data = {'title': 'Updated Test Meme'}
    update_response = requests.put(f"{BASE_URL}/memes/{meme_id}", files=new_files, params=new_data)
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated Test Meme"


def test_delete_meme(setup_teardown):
    files = {'file': open(IMAGE_PATH_2, 'rb')}
    data = {'title': 'Test Meme'}
    create_response = requests.post(f"{BASE_URL}/memes", files=files, params=data)
    assert create_response.status_code == 201
    meme_id = create_response.json()["id"]

    delete_response = requests.delete(f"{BASE_URL}/memes/{meme_id}")
    assert delete_response.status_code == 204

    get_response = requests.get(f"{BASE_URL}/memes/{meme_id}")
    assert get_response.status_code == 404
