from src.configs import *
from src.utils.datetime_checker import DatetimeChecker
from src.utils.flight_frame import Flight

import customtkinter
import sqlite3 as db
import math

class FindFlightWindow(customtkinter.CTkToplevel):
    def __init__(self, cells: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(f"{TOPLEVEL_WINDOW_WIDTH}x{TOPLEVEL_WINDOW_HEIGHT}")
        self.resizable(False, False)
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, fg_color="transparent", width=TOPLEVEL_WINDOW_WIDTH - 20, height=TOPLEVEL_WINDOW_HEIGHT)
        self.scrollable_frame.grid(row=0, column=0)

        flights = self.get_suitable_flights(cells)
        self.flight_frames = []
        lenght = len(flights)
        index = 0
        for r in range(math.ceil(lenght / 2)):
            for c in range(2):
                if index > lenght - 1: break
                self.flight_frames.append(Flight(self.scrollable_frame, r, c, index+1, flights[index]))
                index += 1

    def get_suitable_flights(self, cells: list):
        con = db.connect(database_path)
        cur = con.cursor()
        sql = """ SELECT * FROM flights """
        cur.execute(sql)
        result = cur.fetchall()
        con.commit()
        con.close()

        flights = []
        for i in range(len(result)):
            for k in range(4):
                if cells[k] != "" and cells[k] == result[i][k+1]:
                    flights.append(result[i])

        return flights

class FlightFinder:
    def __init__(self, app: customtkinter.CTk):
        self.app = app
        self.datetime_checker = DatetimeChecker()

    def find_flight(self):
        cells = []
        for i in range(len(self.app.flight_finding_frame.cells)):
            information = self.app.flight_finding_frame.cells[i].entry.get()
            cells.append(information)

        con = db.connect(database_path)
        cur = con.cursor()

        sql = """ SELECT * FROM flights """
        cur.execute(sql)
        result = cur.fetchall()

        con.commit()
        con.close()

        self.find_flight_window = FindFlightWindow(cells)
