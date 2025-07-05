import psycopg2
import os
def make_connection():
    conn = psycopg2.connect(
        host="ep-orange-thunder-a8bytc5c-pooler.eastus2.azure.neon.tech",
        database="neondb",
        user="neondb_owner",
        password="npg_pc9zXM7YwDEL",
        sslmode="require"
    )
    cur = conn.cursor()
    return cur

   

def check_photo(email):
    cur = make_connection()
    sql = "SELECT * FROM photos WHERE email = '"+email+"'"
    cur.execute(sql)
    n = cur.rowcount
    photo = "no"
    if n==1:
        row=cur.fetchone()
        photo=row[1]

    return photo
