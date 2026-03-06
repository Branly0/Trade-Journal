from sqlalchemy import Boolean, Boolean, Column, Integer, String, DateTime, ForeignKey, Uuid, func
from sqlalchemy.orm import relationship
from app.db.session import Base


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE"))  # Foreign key to users table

    user = relationship("User", back_populates="tokens")