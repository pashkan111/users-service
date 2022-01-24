from fastapi import FastAPI
import uvicorn


app = FastAPI()

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, port=8089, host='0.0.0.0')