from src.configs import *
from src.utils.flight_frame import Flight

import customtkinter
import math
import sqlite3 as db

class AllFlightsWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(f"{TOPLEVEL_WINDOW_HEIGHT}x{TOPLEVEL_WINDOW_WIDTH}")
        self.resizable(False, False)
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, fg_color="transparent", width=580, height=400)
        self.scrollable_frame.grid(row=0, column=0)

        flights = self.get_all_flights()
        flight_frames = []
        lenght = len(flights)
        index = 0
        for r in range(math.ceil(lenght / 2)):
            for c in range(2):
                if index > lenght - 1: break
                flight_frames.append(Flight(self.scrollable_frame, r, c, index+1, flights[index]))
                index += 1

    def get_all_flights(self):
        con = db.connect(database_path)
        cur = con.cursor()
        sql = """ SELECT * FROM flights """
        cur.execute(sql)
        result = cur.fetchall()
        con.commit()
        con.close()

        return result
