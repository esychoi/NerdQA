import json
import time
import traceback
from collections.abc import Callable

from fastapi import Request
from starlette.responses import JSONResponse

from app.core.logger import logger


async def log_and_handle_exceptions(request: Request, call_next: Callable):
    """
    A middleware function that logs API requests, handles custom exceptions, and logs other exceptions.

    Args:
        request (fastapi.Request): The incoming API request.
        call_next (Callable): The next middleware or handler in the chain.

    Returns:
        JSONResponse: The API response with appropriate status and content.
    """

    try:
        logger.info(f"Request: {request.method} {request.url}")

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        logger.info(f"Response: {response.status_code} | Time: {process_time:.2f}s for {request.method} {request.url}")
        return response

    except Exception as e:
        process_time = time.time() - start_time
        error_response = {"detail": f"Exception during {request.method} {request.url} after {process_time:.2f}s: {e}"}
        logger.error(error_response)
        logger.error(traceback.format_exc())
        return JSONResponse(status_code=500, content=error_response)
