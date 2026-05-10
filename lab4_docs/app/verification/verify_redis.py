import redis
import json

def verify_redis(config_path="config.json"):
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
            
        url = config["redis"]["url"]
        
        client = redis.from_url(url, decode_responses=True)
        list_name = "spotify_data_list"
        
        total_records = client.llen(list_name)
        print(f"Total records found in Redis (list '{list_name}'): {total_records}")
        
        if total_records > 0:
            print("\n--- First 5 records ---")
            first_five = client.lrange(list_name, 0, 4)
            for i, item in enumerate(first_five):
                parsed_item = json.loads(item)
                print(f"{i + 1}. {parsed_item}")
                
    except redis.exceptions.ConnectionError:
        print("Error: Could not connect to Redis. Ensure the URL is correct.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_redis()