from sqlalchemy import (Column,BigInteger,
                        LargeBinary, String, Table,Integer,ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    FirstName = Column(String(110), nullable=False)
    password = Column(String(128))
    Email = Column(String(320))
    Phone = Column(BigInteger)


class Profile(Base):
    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True)
    profile_picture = Column(String(450))
    profile_picture_name = Column(String(150))
    user_id = Column(Integer, ForeignKey("user.id"))
    extension = Column(String(30))
    
    user = relationship('User', primaryjoin='Profile.user_id == User.id')


