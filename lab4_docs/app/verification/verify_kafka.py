import json
from confluent_kafka import Consumer, KafkaError

def verify_kafka(bootstrap_servers='localhost:9092', topic='spotify_tracks'):
    conf = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'spotify_verifier_group',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(conf)
    consumer.subscribe([topic])
    
    print(f"Listening to topic '{topic}'... (Press Ctrl+C to stop)")
    
    messages_read = 0
    
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            
            if msg is None:
                if messages_read > 0:
                    print(f"\nRead {messages_read} messages. No new data.")
                    break
                continue
                
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Kafka error: {msg.error()}")
                    break
            
            record_value = msg.value().decode('utf-8')
            parsed_record = json.loads(record_value)
            
            messages_read += 1
            
            if messages_read <= 5:
                print(f"[{messages_read}] {parsed_record}")
            elif messages_read == 6:
                print("... (subsequent messages hidden) ...")
                
    except KeyboardInterrupt:
        print("\nReading stopped by user.")
    finally:
        consumer.close()
        if messages_read > 0:
            print(f"Successfully read a total of {messages_read} messages from Kafka.")

if __name__ == "__main__":
    verify_kafka()