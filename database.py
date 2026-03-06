from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
DB_USER = "root"
DB_PASSWORD = ""
DB_HOST = "127.0.0.1"
DB_PORT = "3307"
DB_NAME = "data_quality_db"
DATABASE_URL = "mysql+mysqlconnector://root:@127.0.0.1:3307/data_quality_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 
try:
    connection = engine.connect()
    print("✅ MySQL Connected Successfully")
except Exception as e:
    print("❌ Database Connection Failed:", e)