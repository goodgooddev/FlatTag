from typing import Protocol, Dict


class MetadataStripper(Protocol):
    def inspect(self, data: bytes) -> Dict:
        #  Анализирует файл и возвращает информацию о метаданных
        ...

    def strip(self, data: bytes) -> bytes:
        #  Возвращает очищенные байты файла
        ...