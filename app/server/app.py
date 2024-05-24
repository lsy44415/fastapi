from fastapi import FastAPI
from .routes.bci import router as BciRouter
import psutil
import os

app = FastAPI()

app.include_router(BciRouter, tags=["Bci"], prefix="/bci")

@app.get("/")
async def read_root():
    return {"message": "Welcome to this fantastic app!"}



@app.get("/quit")
def iquit():
    parent_pid = os.getpid()
    parent = psutil.Process(parent_pid)
    for child in parent.children(recursive=True):  # or parent.children() for recursive=False
        child.kill()
    parent.kill()

