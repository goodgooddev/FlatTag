import pytest
import io
from PIL import Image


@pytest.fixture
def fake_jpeg_with_exif():
    #  Создает JPEG в памяти с фейковыми EXIF-данными для тестов
    img = Image.new("RGB", (100, 100), color="red")

    #  Создаем минимальный EXIF-словарь
    exif = img.getexif()
    #  271 - это тег 'Make' (Производитель камеры)
    exif[271] = "TestCamera"
    output = io.BytesIO()
    img.save(output, format="JPEG", exif=exif)
    return output.getvalue()


@pytest.fixture
def fake_clean_png():
    #  Создает чистый PNG в памяти
    img = Image.new("RGB", (50, 50), color="blue")
    output = io.BytesIO()
    img.save(output, format="PNG")
    return output.getvalue()
