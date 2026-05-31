from abc import ABC, abstractmethod
from typing import List, Dict, Any

class ISpotifyRepository(ABC):
    @abstractmethod
    def read_csv(self, filepath: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def save_bulk_data(self, data: List[Dict[str, Any]]) -> None:
        pass

class ISpotifyService(ABC):
    @abstractmethod
    def import_data_from_file(self, filename: str) -> str:
        pass