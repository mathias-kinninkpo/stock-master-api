from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from dotenv import load_dotenv
# import os


# DATABASE_URL = os.getenv("DATABASE_URL")
# print(DATABASE_URL)

engine = create_engine("mysql+mysqlconnector://root:rootroot@localhost/stock")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



# DATABASE_URL=mysql+mysqlconnector://root:rootroot@localhost/stock
