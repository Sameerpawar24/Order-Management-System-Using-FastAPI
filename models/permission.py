from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False)     # e.g. "orders:create"
    description = Column(String(255), nullable=True)

    # backrefs for ORM navigation
    role_links = relationship("RolePermission", back_populates="permission", cascade="all, delete-orphan")
    user_links = relationship("UserPermission", back_populates="permission", cascade="all, delete-orphan")
