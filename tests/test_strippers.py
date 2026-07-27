from app.strippers.jpeg import JpegStripper


def test_jpeg_inspect_detects_metadata(fake_jpeg_with_exif):
    #  Проверяем, что inspect видит EXIF
    stripper = JpegStripper()
    result = stripper.inspect(fake_jpeg_with_exif)

    assert result["has_metadata"] is True
    assert result["tags_count"] > 0


def test_jpeg_strip_removes_metadata(fake_jpeg_with_exif):
    #  Проверяем, что strip реально удаляет EXIF
    stripper = JpegStripper()
    clean_data = stripper.strip(fake_jpeg_with_exif)
    result = stripper.inspect(clean_data)

    assert result["has_metadata"] is False
    assert result["tags_count"] == 0