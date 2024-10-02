from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from .database import Base


class Posts(Base):
    __tablename__ = "posts"


    id = Column(Integer, primary_key = True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default = True)