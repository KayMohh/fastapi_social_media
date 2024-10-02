# from sqlalchemy import Column
# from sqlalchemy import ForeignKey
# from sqlalchemy import Integer
# from sqlalchemy import String
# from sqlalchemy.orm import declarative_base
# from sqlalchemy.orm import relationship

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:11111111@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


sessionLocal =  sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()