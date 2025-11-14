from sqlalchemy import Column, Integer, String, Numeric, DateTime, func, Text
from sqlalchemy.orm import relationship
from app.database import Base
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10,2), nullable=False)
    stock = Column(Integer, default=0, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)

    order_items = relationship("OrderItem", back_populates="product")
