import csv

class SpotifyDataReader:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def read_data(self) -> list[dict]:
        """Reads data from CSV file"""
        data = []
        try:
            with open(self.filepath, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
            return data
        except FileNotFoundError:
            print(f"Error: file {self.filepath} not found!")
            return []