"""
API Middleware - Error Handler
Global error handling middleware.

Author: Alexandre Albert Ndour
"""

import traceback
from datetime import datetime, timezone
import json

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware for global error handling."""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            response = await call_next(request)
            return response
        except ValueError as e:
            # Validation errors
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": str(e)
                    },
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
        except PermissionError as e:
            # Permission denied
            return JSONResponse(
                status_code=403,
                content={
                    "success": False,
                    "error": {
                        "code": "PERMISSION_DENIED",
                        "message": str(e)
                    },
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
        except FileNotFoundError as e:
            # Not found
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "error": {
                        "code": "NOT_FOUND",
                        "message": str(e)
                    },
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
        except Exception as e:
            # Internal server error
            return await self._handle_internal_error(request, e)
    
    async def _handle_internal_error(self, request: Request, exc: Exception) -> JSONResponse:
        """Handle internal server errors."""
        # Log the full error
        error_log = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "path": request.url.path,
            "method": request.method,
            "error": str(exc),
            "traceback": traceback.format_exc()
        }
        
        # In production, send to logging service
        print(json.dumps(error_log))
        
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred"
                },
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )
