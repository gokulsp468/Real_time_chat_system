from fastapi import FastAPI, Request
from routers import auth, chat, rooms
import time
from app.middleware import logger

app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    request_body = await request.body()
    logger.info(f"Incoming request: {request.method} {request.url} - Body: {request_body.decode('utf-8') or 'No Body'}")

    response = await call_next(request)

    duration = time.time() - start_time
    logger.info(
        f"Response: {response.status_code} {request.method} {request.url} - Duration: {duration:.2f}s"
    )
    return response

app.include_router(chat.router)
app.include_router(rooms.router)
app.include_router(auth.router)
