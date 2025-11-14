from fastapi import FastAPI
from api.routes import auth, products, orders
from utils.logging_middleware import RequestLoggingMiddleware
from app.database import Base
from app.database import engine
from app.config import settings

def create_app():
    app = FastAPI(title=settings.PROJECT_NAME)

   
    Base.metadata.create_all(bind=engine)

    app.add_middleware(RequestLoggingMiddleware)
    app.include_router(auth.router)
    app.include_router(products.router)
    app.include_router(orders.router)

    return app

app = create_app()
