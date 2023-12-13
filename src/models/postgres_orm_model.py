from sqlalchemy import (Column,BigInteger,
                        LargeBinary, String, Table,Integer)
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


# class Profile(Base):
#     __tablename__ = 'profile'

#     id = Column(Integer, primary_key=True)
#     profile_picture = Column(LargeBinary)
#     user_id = Column(Integer, ForeignKey("users.id"))
    
#     usermaster = relationship('User', primaryjoin='Profile.user_id == User.id')
    

