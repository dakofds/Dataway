from sqlalchemy import Column, BigInteger, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from backend.database.base import Base

class Reply(Base):
    __tablename__ = 'replies'
    
    id = Column(BigInteger, primary_key=True)
    content = Column(String, nullable=False)
    author = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    topic = Column(BigInteger, ForeignKey('topics.id'), nullable=False)
    
    author_user = relationship('User', back_populates='replies')
    topic_rel = relationship('Topic', back_populates='replies')
