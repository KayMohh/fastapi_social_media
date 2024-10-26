# from sqlalchemy import Column
# from sqlalchemy import ForeignKey
# from sqlalchemy import Integer
# from sqlalchemy import String
# from sqlalchemy.orm import declarative_base
# from sqlalchemy.orm import relationship

# import psycopg2
# from  psycopg2.extras import RealDictCursor 
# import time

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


sessionLocal =  sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()



# db  conn with psycopg
# while True:

#     # Connect to an existing database
#     try:
#         conn =  psycopg2.connect(host = "localhost", database="fastapi", user="postgres", password="11111111", cursor_factory=RealDictCursor)

#         # Open a cursor to perform database operations
#         cursor= conn.cursor() 
#         print("Success")
#         break
#     except Exception as error:
#         print("Connecting to db failed")
#         print("Error: ", error)
#         time.sleep(3)