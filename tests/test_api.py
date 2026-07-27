from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Сервис работает!"}


def test_clean_invalid_file_type():
    #  Проверяем защиту от загрузки не-картинок
    #  Создаём текстовый файл, маскирующийся под картинку
    fake_file = ("text.jpg", b"This is not a real image", "image/jpeg")

    response = client.post("/clean", files={"file": fake_file})

    assert response.status_code == 400
    assert "Недопустимый тип файла" in response.json()["detail"]


def test_inspect_jpeg(fake_jpeg_with_exif):
    #  Проверяем эндпоинт /inspect с валидной картинкой
    file_data = ("test.jpg", fake_jpeg_with_exif, "image/jpeg")
    response = client.post("/inspect", files={"file": file_data})

    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.jpg"
    assert data["has_metadata"] is True
    assert data["file_type"] == "image/jpeg"