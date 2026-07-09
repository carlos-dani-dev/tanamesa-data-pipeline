import pandas as pd
import time

from api.config import CSV_PATH
from api.db_settings import engine



time.sleep(5)

df = pd.read_csv(CSV_PATH)
df.head(0).to_sql("responses", engine, if_exists="replace", index=False)

conn = engine.raw_connection()
cur = conn.cursor()

with open(CSV_PATH, "r", encoding="utf-8") as csv_file:
    cur.copy_expert(
        "COPY responses FROM STDIN WITH CSV HEADER",
        csv_file,
    )

conn.commit()
cur.close()
conn.close()