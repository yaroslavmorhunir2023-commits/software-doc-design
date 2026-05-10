import csv
import random
from faker import Faker

fake = Faker()

def generate_spotify_data(filename="spotify_data.csv", num_records=1500):
    users = [{"username": fake.user_name(), "email": fake.email()} for _ in range(50)]
    playlists = [{"title": fake.catch_phrase()} for _ in range(100)]
    tracks = [
        {
            "title": fake.sentence(nb_words=3)[:-1], 
            "artist": fake.name(), 
            "duration": random.randint(120, 360)
        } for _ in range(200)
    ]

    headers = [
        "user_username", "user_email", "playlist_title", 
        "track_title", "track_artist", "track_duration_sec", 
        "played_at", "listen_duration_sec"
    ]
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        
        for _ in range(num_records):
            u = random.choice(users)
            p = random.choice(playlists)
            t = random.choice(tracks)
            played_at = fake.date_time_between(start_date="-1y", end_date="now").isoformat()
            listen_dur = random.randint(30, t["duration"]) # Прослухав від 30 сек до повної довжини
            
            writer.writerow([
                u["username"], u["email"], p["title"], 
                t["title"], t["artist"], t["duration"], 
                played_at, listen_dur
            ])
            
    print(f"Generated {num_records} rows in {filename}")

if __name__ == "__main__":
    generate_spotify_data()