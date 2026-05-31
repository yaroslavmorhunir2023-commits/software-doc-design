from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from lab2_docs.app.data_access.database import SessionLocal
from lab2_docs.app.interfaces.interfaces import ISpotifyService
from lab2_docs.app.dal.repositories import SpotifyRepository
from lab2_docs.app.bll.services import SpotifyService

from lab2_docs.app.generate_csv import generate_spotify_data


router = APIRouter(prefix="/spotify", tags=["Spotify API"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def get_spotify_service(db: Session = Depends(get_db)) -> ISpotifyService:
    repository = SpotifyRepository(db)
    return SpotifyService(repository)

@router.post("/import")
def run_import(service: ISpotifyService = Depends(get_spotify_service)):
    try:
        message = service.import_data_from_file("spotify_data.csv")
        return {"status": "success", "detail": message}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/generate-csv", summary="Generate CSV")
def generate_csv_file(num_records: int = Query(1500, description="Number of rows(at least 1000)")):
    try:
        if num_records < 1000:
            raise ValueError("At least 1000 rows needed")
            
        generate_spotify_data("spotify_data.csv", num_records=num_records)
        return {"status": "success", "detail": f"File spotify_data.csv successfully generated with {num_records} rows."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
