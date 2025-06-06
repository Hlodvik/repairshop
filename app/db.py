from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://root:password@localhost:3306/repairshop"

 
engine = create_engine(DATABASE_URL, echo=True)
 
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)