from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship
from backend.database.base import Base

class Board(Base):
    __tablename__ = 'boards'
    
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    
    topics = relationship('Topic', back_populates='board_rel')
