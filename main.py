import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Depends


load_dotenv()
app = FastAPI()

@app.get("/healthy")
def health_check():
    return {"status": "healthy"}