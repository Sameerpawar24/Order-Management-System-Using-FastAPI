from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import time, json, traceback
from app.database import SessionLocal
from models.audit import RequestLog
from jose import jwt
from fastapi.responses import JSONResponse
from app.config import settings


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        user_id = None

        # extracting user_id from JWT
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user_id = payload.get("user_id")
            except:
                pass

        db = SessionLocal()
        response_body = None
        message = None
        error_trace = None

        try:
            # PROCESS REQUEST
            response = await call_next(request)

            # Read response body
            resp_body = [section async for section in response.body_iterator]
            response.body_iterator = iterate_in_memory(resp_body)

            response_body = resp_body[0].decode() if resp_body else None
            message = "SUCCESS"

        except Exception as e:
            # CAPTURE ERROR
            message = str(e)
            error_trace = traceback.format_exc()

            response = JSONResponse(
                status_code=500,
                content={'status_code':500,"detail": "Internal Server Error"}
            )

        #  STORE LOG INTO DATABASE
        try:
            log = RequestLog(
                user_id=user_id,
                method=request.method,
                url=str(request.url),
                ip_address=request.client.host,
                status_code=response.status_code,
                latency=time.time() - start,
                user_agent=request.headers.get("User-Agent"),
                message=message,
                response_body=response_body,
                error_trace=error_trace
            )
            db.add(log)
            db.commit()

        except Exception as db_err:
            print("Request log DB error:", db_err)

        return response


#  Helper to rebuild body iterator
async def iterate_in_memory(data):
    for item in data:
        yield item


