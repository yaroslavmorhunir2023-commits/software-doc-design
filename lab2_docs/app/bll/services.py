from interfaces.interfaces import ISpotifyService, ISpotifyRepository

class SpotifyService(ISpotifyService):
    def __init__(self, repository: ISpotifyRepository):
        self.repository = repository

    def import_data_from_file(self, filename: str) -> str:
        data = self.repository.read_csv(filename)
        if len(data) < 1000:
            raise ValueError("Файл занадто малий")
        
        self.repository.save_bulk_data(data)
        return f"Успішно імпортовано {len(data)} записів"