from sqlalchemy import Column, BigInteger, String, Boolean
from sqlalchemy.orm import relationship
from backend.database.base import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)

    topics = relationship('Topic', back_populates='author_user', cascade="all, delete-orphan")
    replies = relationship('Reply', back_populates='author_user', cascade="all, delete-orphan")