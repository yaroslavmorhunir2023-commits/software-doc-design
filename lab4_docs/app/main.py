import json
from data_reader import SpotifyDataReader
from strategies import ConsoleOutputStrategy, RedisOutputStrategy, KafkaOutputStrategy

class DataProcessor:
    def __init__(self, strategy):
        self._strategy = strategy

    def set_strategy(self, strategy):
        self._strategy = strategy

    def process(self, data: list[dict]):
        self._strategy.write(data)

def load_config(config_path="config.json"):
    with open(config_path, "r") as file:
        return json.load(file)

def get_strategy_from_config(config: dict):
    strategy_type = config.get("output_strategy")

    if strategy_type == "console":
        return ConsoleOutputStrategy()
    
    elif strategy_type == "redis":
        redis_cfg = config["redis"]
        # UPDATED: Use 'url' instead of 'host', 'port', 'db'
        return RedisOutputStrategy(url=redis_cfg["url"])
    
    elif strategy_type == "kafka":
        kafka_cfg = config["kafka"]
        return KafkaOutputStrategy(
            bootstrap_servers=kafka_cfg["bootstrap_servers"],
            topic=kafka_cfg["topic"]
        )
    else:
        raise ValueError(f"Unknown strategy: {strategy_type}")

if __name__ == "__main__":
    config = load_config("config.json")
    strategy = get_strategy_from_config(config)

    reader = SpotifyDataReader("spotify_data.csv")
    data = reader.read_data()

    if data:
        processor = DataProcessor(strategy)
        processor.process(data)