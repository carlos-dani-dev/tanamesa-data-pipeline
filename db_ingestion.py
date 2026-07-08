from sqlalchemy import create_engine, insert,  text
from config import SQLALCHEMY_DATABASE_URL
import time

time.sleep(5)

engine=create_engine(SQLALCHEMY_DATABASE_URL)
conn=engine.connect()

query=text("INSERT INTO identity (_name, surname) VALUES ('Carlos', 'Daniel'), ('Maria', 'Eduarda');")
conn.execute(query)
conn.commit()