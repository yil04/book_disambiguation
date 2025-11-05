import pandas as pd
import sqlite3
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE_PATH = os.path.join(SCRIPT_DIR, 'latest.db')

# add dynasties to filter, the values should be integers, NOT strings
# example: DY_FILTER_LIST = [15, 16, 17]
DY_FILTER_LIST = [15]

base_sql_query = """
SELECT
    tc.c_textid,
    COALESCE(NULLIF(btd.c_personid, ''), 0) AS c_personid,
    bm.c_name_chn,
    bm.c_dy,
    tc.c_title_chn,
    tc.c_text_dy,
    tc.c_title_alt_chn,
    tc.c_source
FROM
    TEXT_CODES AS tc
LEFT JOIN
    BIOG_TEXT_DATA AS btd ON tc.c_textid = btd.c_textid
LEFT JOIN
    BIOG_MAIN AS bm ON bm.c_personid = COALESCE(btd.c_personid, 0);
"""

def join():
    final_sql_query = base_sql_query.strip().rstrip(';')
    if DY_FILTER_LIST:
        filter_values = ", ".join(map(str, DY_FILTER_LIST))
        where_clause = f" WHERE (bm.c_dy IN ({filter_values}) OR bm.c_dy IS NULL)"
        final_sql_query += where_clause

    with sqlite3.connect(DB_FILE_PATH) as conn:
        df = pd.read_sql_query(final_sql_query, conn)
    df.index.name = 'row_id'

    return df

if __name__ == "__main__":
    join().to_excel("JOINED_BIOG_TEXT.xlsx")