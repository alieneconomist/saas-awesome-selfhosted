from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="saas-awesome-selfhosted")

class Request(BaseModel):
    input: str
    options: dict = {}

@app.get("/")
def home():
    return {"name": "saas-awesome-selfhosted", "source": "https://github.com/?/saas-awesome-selfhosted"}

@app.get("/health")
def health():
    return {"status": "ok", "service": "saas-awesome-selfhosted"}

@app.get("/readyz")
def readyz():
    return {"status": "ready", "service": "saas-awesome-selfhosted"}

@app.post("/run")
def run(req: Request):
    return {"status": "prototype", "input": req.input, "message": "Coming soon"}
