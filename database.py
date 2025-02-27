import sqlite3 as db

def main():
    con = db.connect("application_database.db")
    cur = con.cursor()

    # sql = """ CREATE TABLE IF NOT EXISTS users(
    # user_id INTEGER,
    # username TEXT,
    # password TEXT,
    # PRIMARY KEY(user_id)
    # ) """
   
    # sql = """ CREATE TABLE IF NOT EXISTS flights(
    # flight_id INTEGER,
    # departure_location TEXT,
    # arrival_location TEXT,
    # departure_date DATE,
    # arrival_date DATE,
    # departure_time TEXT,
    # arrival_time TEXT,
    # price INTEGER,
    # PRIMARY KEY(flight_id)
    # ) """

    # sql = """ SELECT user_id FROM users """

    # cur.execute(sql)
    # result = cur.fetchall()
    # con.close()

    # print(result[-1][0])

main()