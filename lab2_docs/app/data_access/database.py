from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DATABASE_URL = "sqlite:///./spotify_v2.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class UserORM(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True, index=True)
    
    playlists = relationship("PlaylistORM", back_populates="owner")
    statistics = relationship("PlaybackStatisticORM", back_populates="user")

class PlaylistORM(Base):
    __tablename__ = "playlists"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("UserORM", back_populates="playlists")
    tracks = relationship("TrackORM", back_populates="playlist")

class TrackORM(Base):
    __tablename__ = "tracks"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    artist = Column(String)
    duration_sec = Column(Integer)
    playlist_id = Column(Integer, ForeignKey("playlists.id"))
    
    playlist = relationship("PlaylistORM", back_populates="tracks")
    statistics = relationship("PlaybackStatisticORM", back_populates="track")

class PlaybackStatisticORM(Base):
    __tablename__ = "playback_statistics"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    track_id = Column(Integer, ForeignKey("tracks.id"))
    played_at = Column(String)
    listen_duration = Column(Integer)
    
    user = relationship("UserORM", back_populates="statistics")
    track = relationship("TrackORM", back_populates="statistics")

Base.metadata.create_all(bind=engine)