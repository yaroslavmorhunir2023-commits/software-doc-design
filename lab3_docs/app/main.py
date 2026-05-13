from fastapi import FastAPI
from controller import router

app = FastAPI(title="Lab 3 - MVC")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)