from sqlalchemy import create_engine, insert,  text
from config import SQLALCHEMY_DATABASE_URL, CSV_PATH
import pandas as pd
import time

time.sleep(5)

engine=create_engine(SQLALCHEMY_DATABASE_URL)

df = pd.read_csv(CSV_PATH)
df.head(0).to_sql("responses", engine, if_exists="replace", index=False)

conn=engine.raw_connection()
cur=conn.cursor()

with open(CSV_PATH, "r", encoding="utf-8") as csv_file:
    cur.copy_expert(
        "COPY responses FROM STDIN WITH CSV HEADER",
        csv_file
    )

conn.commit()
cur.close()
conn.close()