import csv
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from interfaces.interfaces import ISpotifyRepository
from data_access.database import UserORM, PlaylistORM, TrackORM, PlaybackStatisticORM

class SpotifyRepository(ISpotifyRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def read_csv(self, filepath: str) -> List[Dict[str, Any]]:
        with open(filepath, mode='r', encoding='utf-8') as f:
            return list(csv.DictReader(f))

    def save_bulk_data(self, data: List[Dict[str, Any]]) -> None:
        user_cache = {}
        playlist_cache = {}
        track_cache = {}

        for row in data:
            email = row['user_email']
            if email not in user_cache:
                user = self.db.query(UserORM).filter_by(email=email).first()
                if not user:
                    user = UserORM(username=row['user_username'], email=email)
                    self.db.add(user)
                    self.db.flush() # flush щоб отримати ID без повного коміту
                user_cache[email] = user.id
            user_id = user_cache[email]

            p_key = (row['playlist_title'], user_id)
            if p_key not in playlist_cache:
                playlist = self.db.query(PlaylistORM).filter_by(title=p_key[0], user_id=p_key[1]).first()
                if not playlist:
                    playlist = PlaylistORM(title=p_key[0], user_id=p_key[1])
                    self.db.add(playlist)
                    self.db.flush()
                playlist_cache[p_key] = playlist.id
            playlist_id = playlist_cache[p_key]

            t_key = (row['track_title'], row['track_artist'], playlist_id)
            if t_key not in track_cache:
                track = self.db.query(TrackORM).filter_by(
                    title=t_key[0], artist=t_key[1], playlist_id=t_key[2]
                ).first()
                if not track:
                    track = TrackORM(
                        title=t_key[0], 
                        artist=t_key[1], 
                        duration_sec=int(row['track_duration_sec']), 
                        playlist_id=t_key[2]
                    )
                    self.db.add(track)
                    self.db.flush()
                track_cache[t_key] = track.id
            track_id = track_cache[t_key]

            stat = PlaybackStatisticORM(
                user_id=user_id,
                track_id=track_id,
                played_at=row['played_at'],
                listen_duration=int(row['listen_duration_sec'])
            )
            self.db.add(stat)

        self.db.commit()