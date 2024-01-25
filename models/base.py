from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from dotenv import load_dotenv
# import os


# DATABASE_URL = os.getenv("DATABASE_URL")
# print(DATABASE_URL)

#DATABASE_URL = "postgresql+psycopg2://root:RKYvsJGOpo2HJMrTEtngc7eSstkW94GA@dpg-cmp5ooun7f5s73dc1i30-a.oregon-postgres.render.com/stock_db_ip4u"
DATABASE_URL="postgresql+psycopg2://root:RKYvsJGOpo2HJMrTEtngc7eSstkW94GA@dpg-cmp5ooun7f5s73dc1i30-a/stock_db_ip4u"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# DATABASE_URL=postgres://root:RKYvsJGOpo2HJMrTEtngc7eSstkW94GA@dpg-cmp5ooun7f5s73dc1i30-a.oregon-postgres.render.com/stock_db_ip4u