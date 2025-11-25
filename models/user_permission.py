from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from models.user import User  

class UserPermission(Base):
    __tablename__ = "user_permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False)
    is_allowed = Column(Boolean, default=True, nullable=False)  # True: explicitly allowed;
    #False: explicitly denied the permission
    user = relationship("User", back_populates="user_permissions")
    permission = relationship("Permission", back_populates="user_links")
    # user relationship will be declared on User model (back_populates)
