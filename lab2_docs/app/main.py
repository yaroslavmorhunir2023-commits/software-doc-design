from fastapi import FastAPI
from pl.endpoints import router

app = FastAPI(title="Spotify Enterprise API", version="2.0")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)