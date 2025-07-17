from sqlalchemy import Column, BigInteger, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from backend.database.base import Base

class Topic(Base):
    __tablename__ = 'topics'
    
    id = Column(BigInteger, primary_key=True)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    media = Column(String, nullable=True)
    author = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    board = Column(BigInteger, ForeignKey('boards.id'), nullable=False)
    
    author_user = relationship('User', back_populates='topics')
    board_rel = relationship('Board', back_populates='topics')
    replies = relationship('Reply', back_populates='topic_rel')
