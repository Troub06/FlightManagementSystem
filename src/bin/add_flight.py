from src.configs import *
from src.utils.datetime_checker import DatetimeChecker

import sqlite3 as db
import customtkinter

class FlightAdder:
    def __init__(self, app: customtkinter.CTk):
        self.app = app
        self.datetime_checker = DatetimeChecker()

    def add_flight(self):
        try:
            self.flight_id = self.get_flight_id()
            self.flight = self.get_flight_data()

            for i in range(2, 4):
                if self.datetime_checker.is_valid_date(self.flight[i]) == False and self.flight[i] != "":
                    print("The date was written in a wrong format!")
                    return
            for i in range(4, 6):
                if self.datetime_checker.is_valid_time(self.flight[i]) == False and self.flight[i] != "":
                    print("The time was written in a wrong format!")
                    return

            self.insert_data()
        except Exception as e:
            print("Error adding flight:", e)

    def get_flight_data(self):
        return [cell.entry.get() for cell in self.app.flight_adding_frame.cells]

    def get_flight_id(self):
        con = db.connect(database_path)
        cur = con.cursor()
        sql = """ SELECT MAX(flight_id) FROM flights """
        cur.execute(sql)
        result = cur.fetchone()
        con.commit()
        con.close()
        return (result[0] or 0) + 1
    
    def insert_data(self):
        con = db.connect(database_path)
        cur = con.cursor()
        sql = f""" INSERT INTO "flights"
        (flight_id, departure_location, arrival_location, departure_date, arrival_date, departure_time, arrival_time, price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        cur.execute(sql, (self.flight_id, *self.flight))
        con.commit()
        con.close()
