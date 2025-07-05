import psycopg2

def make_connection():
    conn = psycopg2.connect(
        host="ep-calm-night-1234567.us-east-2.aws.neon.tech",  # Neon DB host
        database="neondb",
        user="neondb_owner",
        password="YOUR_PASSWORD",  
        sslmode="require"
    )
     cur = conn.cursor()
    return cur

   

def check_photo(email):
    conn  = pymysql.connect(host="localhost",user="root",port=3306,passwd='',db="medicine",autocommit=True)
    cur = conn.cursor()
    sql = "SELECT * FROM photos WHERE email = '"+email+"'"
    cur.execute(sql)
    n = cur.rowcount
    photo = "no"
    if n==1:
        row=cur.fetchone()
        photo=row[1]

    return photo
