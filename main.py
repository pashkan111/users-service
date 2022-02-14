from fastapi import FastAPI
import uvicorn
from src.auth.urls import router


app = FastAPI()

app.include_router(router)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, port=8089, host='0.0.0.0')