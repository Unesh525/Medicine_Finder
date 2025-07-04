import pymysql

def make_connection():
    conn = pymysql.connect(host="localhost",
                           user="root",
                           passwd='',
                           db="medicine",
                           port=3306,
                           autocommit=True)
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