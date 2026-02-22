"""
API Middleware - Logging
Structured JSON logging middleware.

Author: Alexandre Albert Ndour
"""

import time
import uuid
import json
from datetime import datetime, timezone
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for structured JSON logging."""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Start timer
        start_time = time.time()
        
        # Get request details
        method = request.method
        path = request.url.path
        client_host = request.client.host if request.client else "unknown"
        
        # Process request
        try:
            response = await call_next(request)
        except Exception as e:
            # Log error
            self._log_error(
                request_id=request_id,
                method=method,
                path=path,
                client_host=client_host,
                error=str(e),
                duration=time.time() - start_time
            )
            raise
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log request
        self._log_request(
            request_id=request_id,
            method=method,
            path=path,
            client_host=client_host,
            status_code=response.status_code,
            duration=duration
        )
        
        # Add headers
        response.headers["X-Request-ID"] = request_id
        
        return response
    
    def _log_request(
        self,
        request_id: str,
        method: str,
        path: str,
        client_host: str,
        status_code: int,
        duration: float
    ):
        """Log HTTP request."""
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": "info",
            "type": "http_request",
            "request_id": request_id,
            "method": method,
            "path": path,
            "client_host": client_host,
            "status_code": status_code,
            "duration_ms": round(duration * 1000, 2)
        }
        
        # Print or send to logging service
        print(json.dumps(log_data))
    
    def _log_error(
        self,
        request_id: str,
        method: str,
        path: str,
        client_host: str,
        error: str,
        duration: float
    ):
        """Log HTTP error."""
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": "error",
            "type": "http_error",
            "request_id": request_id,
            "method": method,
            "path": path,
            "client_host": client_host,
            "error": error,
            "duration_ms": round(duration * 1000, 2)
        }
        
        print(json.dumps(log_data))
