# app/core/db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import oracledb

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "1521")
DB_NAME = os.getenv("DB_NAME", "XEPDB1")  # 常見的 Oracle PDB 名稱
DB_USER = os.getenv("DB_USER", "system")
DB_PASSWORD = os.getenv("DB_PASSWORD", "oracle")
DB_MAXPOOLSIZE = int(os.getenv("DB_MAXPOOLSIZE", "10"))

dsn = oracledb.makedsn(DB_HOST, int(DB_PORT), service_name=DB_NAME)
print(dsn)  # 確認輸出應該是 (DESCRIPTION=...)

DATABASE_URL = f"oracle+oracledb://system:oracle@{dsn}"
print(DATABASE_URL)
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# 依賴 injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()
