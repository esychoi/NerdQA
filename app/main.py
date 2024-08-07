from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from core.middlewares import log_and_handle_exceptions

app = FastAPI()
app.middleware("http")(log_and_handle_exceptions)


@app.get("/")
def main():
    return "Welcome to the NerdQA chatbot!"


@app.get("/healthz")
def health_check():
    return JSONResponse(status_code=200, content={"status": "ok"})
