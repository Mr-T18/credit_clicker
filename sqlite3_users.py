import sqlite3

def create_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        id STRING,
        num_credit INTEGER,
        store_0 INTERGER,
        store_1 INTERGER,
        store_2 INTERGER,
        store_3 INTERGER,
        store_4 INTERGER,
        store_5 INTERGER,
        store_6 INTERGER,
        store_7 INTERGER,
        store_8 INTERGER,
        store_9 INTERGER,
        store_level_0 INTERGER,
        store_level_1 INTERGER,
        store_level_2 INTERGER,
        store_level_3 INTERGER,
        store_level_4 INTERGER,
        store_level_5 INTERGER,
        store_level_6 INTERGER,
        store_level_7 INTERGER,
        store_level_8 INTERGER,
        store_level_9 INTERGER,
        click_level INTERGER,
        click_count INTERGER,
        lastdate INTERGER,
        reincarnation INTERGER,
        PRIMARY KEY(id))""")
    pass

def create_user(id):
    cur.execute("""INSERT INTO users VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (id,234,1,2,3,4,5,6,7,8,9,10,1,1,1,1,2,3,2,2,2,1,3,30,111,0))
    pass

def delete_user(id):
    cur.execute("""DELETE FROM users WHERE id = ?""",(id,))

def read_user(id):
    if not cur.execute(f"SELECT * FROM users WHERE id = ?",[id]).fetchone():
        cur.execute("""INSERT INTO users VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (id,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0))
    cur.execute(f"""SELECT * FROM users WHERE id = ?""",[id])
    result = cur.fetchone()
    return result
    pass

def save_user(id="a0001",credit=0,stores=[0]*10,store_level=[0]*10,click_level=[0]*3,click_count=0,lastdate=0,rein=0):
    cur.execute("""REPLACE INTO users VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (id,credit,stores[0],stores[1],stores[2],stores[3],stores[4],stores[5],stores[6],stores[7],stores[8],stores[9],
                 store_level[0],store_level[1],store_level[2],store_level[3],store_level[4],store_level[5],
                 store_level[6],store_level[7],store_level[8],store_level[9],click_level,click_count,lastdate,rein))

def open_file():
    global dbname,conn,cur
    dbname = "cc_user.db"
    conn = sqlite3.connect(dbname)
    conn.row_factory = sqlite3.Row
    cur=conn.cursor()
    create_table()
    
def close_file():
    conn.commit()
    cur.close()
    conn.close()
# open_file()
# delete_user("j0001")
# close_file()