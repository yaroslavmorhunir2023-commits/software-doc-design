from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db, Track

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def list_tracks(request: Request, db: Session = Depends(get_db)):
    tracks = db.query(Track).all()
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"tracks": tracks})

@router.get("/tracks/new", response_class=HTMLResponse)
def new_track_form(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="form.html", 
        context={"track": None}
    )

@router.post("/tracks/new")
def create_track(
    title: str = Form(...),
    artist: str = Form(...),
    duration_sec: int = Form(...),
    db: Session = Depends(get_db)
):
    new_track = Track(title=title, artist=artist, duration_sec=duration_sec)
    db.add(new_track)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@router.get("/tracks/{track_id}/edit", response_class=HTMLResponse)
def edit_track_form(request: Request, track_id: int, db: Session = Depends(get_db)):
    track = db.query(Track).filter(Track.id == track_id).first()
    return templates.TemplateResponse(
        request=request, 
        name="form.html", 
        context={"track": track}
    )

@router.post("/tracks/{track_id}/edit")
def update_track(
    track_id: int,
    title: str = Form(...),
    artist: str = Form(...),
    duration_sec: int = Form(...),
    db: Session = Depends(get_db)
):
    track = db.query(Track).filter(Track.id == track_id).first()
    if track:
        track.title = title
        track.artist = artist
        track.duration_sec = duration_sec
        db.commit()
    return RedirectResponse(url="/", status_code=303)

@router.post("/tracks/{track_id}/delete")
def delete_track(track_id: int, db: Session = Depends(get_db)):
    track = db.query(Track).filter(Track.id == track_id).first()
    if track:
        db.delete(track)
        db.commit()
    return RedirectResponse(url="/", status_code=303)