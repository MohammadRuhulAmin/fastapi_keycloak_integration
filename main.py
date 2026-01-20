import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Depends

from schemas import userPayload
from routers import get_user_info

load_dotenv()
app = FastAPI()

@app.get("/healthy")
def health_check():
    return {"status": "healthy"}
@app.get("/healthy/about")
def health_check():
    return {"status": "healthy-about"}


@app.get("/secure")
async def root(user: userPayload = Depends(get_user_info)):
    return {"message": f"Hello {user.username} you have the access to the following service: {user.realm_roles}"}

if __name__ == '__main__':
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)