import logging
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

# Configure logging
log_filename = f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("task_management")



