from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.core.middlewares import log_and_handle_exceptions
from app.routers import router

app = FastAPI()
app.middleware("http")(log_and_handle_exceptions)
app.include_router(router)


@app.get("/")
def main():
    return "Welcome to the NerdQA chatbot!"


@app.get("/healthz")
def health_check():
    return JSONResponse(status_code=200, content={"status": "ok"})
