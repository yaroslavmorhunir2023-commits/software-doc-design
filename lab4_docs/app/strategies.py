import json
import redis
from confluent_kafka import Producer
from abc import ABC, abstractmethod

class IOutputStrategy(ABC):
    @abstractmethod
    def write(self, data: list[dict]) -> None:
        pass

class ConsoleOutputStrategy(IOutputStrategy):
    def write(self, data: list[dict]) -> None:
        print(f"--- Console output: {len(data)} records ---")
        for item in data:
            print(item)

class RedisOutputStrategy(IOutputStrategy):
    def __init__(self, url: str):
        self.client = redis.from_url(url, decode_responses=True)
        self.list_name = "spotify_data_list"

    def write(self, data: list[dict]) -> None:
        print(f"--- Writing to Redis: {len(data)} records ---")
        for item in data:
            self.client.rpush(self.list_name, json.dumps(item))
        print("Successfully written to Redis!")

class KafkaOutputStrategy(IOutputStrategy):
    def __init__(self, bootstrap_servers: str, topic: str):
        self.topic = topic
        conf = {
            'bootstrap.servers': bootstrap_servers,
            'client.id': 'spotify_data_producer'
        }
        self.producer = Producer(conf)

    def write(self, data: list[dict]) -> None:
        print(f"--- Writing to Kafka (topic: {self.topic}): {len(data)} records ---")
        
        def delivery_report(err, msg):
            if err is not None:
                print(f"Message delivery failed: {err}")

        for item in data:
            value_bytes = json.dumps(item).encode('utf-8')
            self.producer.produce(
                topic=self.topic, 
                value=value_bytes, 
                callback=delivery_report
            )
            self.producer.poll(0)

        self.producer.flush()
        print("Successfully written to Kafka!")