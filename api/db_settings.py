from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from api.config import SQLALCHEMY_DATABASE_URL


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SQL_DIR = Path(__file__).resolve().parent.parent / "db" / "sql"

def apply_sql_views():
    with engine.begin() as conn:
        for sql_file in sorted(SQL_DIR.glob("*.sql")):
            with sql_file.open(encoding="utf-8") as f:
                conn.execute(text(f.read()))

def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()