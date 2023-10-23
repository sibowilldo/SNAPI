from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Role(Base):
    __tablename__ = 'users'  
    id = Column(Integer, primary_key=True, index=True)

class User(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    registration = Column(Integer)
    contact = Column(Integer)
    createdby = Column(DateTime)
    updatedby = Column(DateTime)
    
    User_id = Column(Integer, ForeignKey("User_id")) 
    
    User = relationship("Role", back_populates="user")  

    def __repr__(self):
        return f'User {self.id}'

