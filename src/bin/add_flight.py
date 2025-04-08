import sqlite3 as db
from src.configs import *
from src.utils.datetime_checker import DatetimeChecker

class FlightAdder:
    def __init__(self, app):
        self.app = app
        self.datetime_checker = DatetimeChecker()

    def add_flight(self):
        con = db.connect(database_path)
        cur = con.cursor()

        sql = """ SELECT flight_id FROM flights """
        cur.execute(sql)
        result = cur.fetchall()

        if len(result) == 0:
            result.append([0])

        flight = [self.app.flight_adding_frame.cells[0].entry.get(), 
                                                self.app.flight_adding_frame.cells[1].entry.get(), self.app.flight_adding_frame.cells[2].entry.get(),
                                                self.app.flight_adding_frame.cells[3].entry.get(), self.app.flight_adding_frame.cells[4].entry.get(),
                                                self.app.flight_adding_frame.cells[5].entry.get(), self.app.flight_adding_frame.cells[6].entry.get()]

        for i in range(2, 4):
            if self.datetime_checker.is_valid_date(flight[i]) == False and flight[i] != "":
                print("The date was written in a wrong format!")
                return
        for i in range(4, 6):
            if self.datetime_checker.is_valid_time(flight[i]) == False and flight[i] != "":
                print("The time was written in a wrong format!")
                return

        sql = f""" INSERT INTO "flights"
        (flight_id, departure_location, arrival_location, departure_date, arrival_date, departure_time, arrival_time, price)
        VALUES ({result[-1][0] + 1}, "{flight[0]}",  "{flight[1]}", "{flight[2]}", "{flight[3]}", "{flight[4]}", "{flight[5]}", "{flight[6]}")
        """
        cur.execute(sql)
        con.commit()
        con.close()
