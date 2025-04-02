import customtkinter
from PIL import Image
import os
import sqlite3 as db
import math

customtkinter.set_appearance_mode("dark")

class Find_flight_window(customtkinter.CTkToplevel):
    def __init__(self, cells: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x400")
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, fg_color="transparent", width=580, height=400)
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

    def get_suitable_flights(selfj, cells: list):
        con = db.connect("application_database.db")
        cur = con.cursor()
        sql = """ SELECT * FROM flights """
        cur.execute(sql)
        result = cur.fetchall()
        print(result)
        con.commit()
        con.close()

        flights = []
        for i in range(len(result)):
            for k in range(4):
                if cells[k] != "" and cells[k] == result[i][k+1]:
                    flights.append(result[i])

        return flights

class InfoLabel(customtkinter.CTkLabel):
    def __init__(self, master: customtkinter.CTkFrame, string: str, information: list, rows: int):
        super().__init__(master, text=f"{string} {information}", anchor="center")
        self.grid(row=rows, column=0)

class Flight(customtkinter.CTkFrame):
    cell_names = ["Departure place:", "Arrival place:", "Departure date:", "Arrival date:", "Departure time:", "Arrival time:", "Price:"]

    def __init__(self, master: customtkinter.CTkToplevel, rows: int, columns: int, index: int, flights: list):
        super().__init__(master)
        self.grid(row=rows, column=columns, padx=10, pady=10)
        self.grid_columnconfigure(0, weight=1)
        self.title = customtkinter.CTkLabel(self, text=f"Flight {index}", font=customtkinter.CTkFont(size=15, weight="bold"), width=270)
        self.title.grid(row=0, column=0)
        for i in range(1, len(flights)):
            self.departure_location_label = InfoLabel(self, self.cell_names[i-1], flights[i], i)

class All_flights_window(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x400")
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, fg_color="transparent", width=580, height=400)
        self.scrollable_frame.grid(row=0, column=0)

        flights = self.get_all_flights()
        self.flight_frames = []
        lenght = len(flights)
        index = 0
        for r in range(math.ceil(lenght / 2)):
            for c in range(2):
                if index > lenght - 1: break
                self.flight_frames.append(Flight(self.scrollable_frame, r, c, index+1, flights[index]))
                index += 1

    def get_all_flights(self):
        con = db.connect("application_database.db")
        cur = con.cursor()
        sql = """ SELECT * FROM flights """
        cur.execute(sql)
        result = cur.fetchall()
        con.commit()
        con.close()

        return result

class Flight_add_frame(customtkinter.CTkFrame):
    cell_names = ["Departure place:", "Arrival place:", "Departure date:", "Arrival date:", "Departure time:", "Arrival time:", "Price:"]
    placeholders = ["", "", "dd.mm.yyyy", "dd.mm.yyyy", "hh:mm", "hh:mm", ""]

    def __init__(self, master: customtkinter.CTkFrame, corner_radius: int):
        super().__init__(master.home_frame, corner_radius)
        self.grid_columnconfigure(1, weight=1)
        self.flight_adding_label = customtkinter.CTkLabel(self, text="Add a flight",
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.flight_adding_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        self.cells = []
        for i in range(len(self.cell_names)):
            self.cells.append(Cell(self, i+1, self.cell_names[i], self.placeholders[i]))

        self.add_button = customtkinter.CTkButton(self, text="Add", command=master.add_flight, width=200)
        self.add_button.grid(row=8, column=0, columnspan=2, pady=15)

class Flight_find_frame(customtkinter.CTkFrame):
    cell_names = ["Departure place:", "Arrival place:", "Departure date:", "Arrival date:"]
    placeholders = ["", "", "dd.mm.yyyy", "dd.mm.yyyy"]
    def __init__(self, master: customtkinter.CTkFrame,  corner_radius: int):
        super().__init__(master.home_frame, corner_radius)
        self.grid_columnconfigure(1, weight=1)
        self.flight_finding_label = customtkinter.CTkLabel(self, text="Find a flight",
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.flight_finding_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        self.cells = []
        for i in range(len(self.cell_names)):
            self.cells.append(Cell(self, i+1, self.cell_names[i], self.placeholders[i]))

        self.add_button = customtkinter.CTkButton(self, text="Find", command=master.find_flight, width=200)
        self.add_button.grid(row=8, column=0, columnspan=2, pady=15)

class Cell():
    def __init__(self, flight_adding_frame, cell_row: int, cell_name: str, placeholder: str):
        self.label = customtkinter.CTkLabel(flight_adding_frame, text=cell_name, font=customtkinter.CTkFont(size=15))
        self.label.grid(row=cell_row, column=0, padx=(20, 0), pady=(0, 15))
        self.entry = customtkinter.CTkEntry(flight_adding_frame, width=200, placeholder_text=placeholder)
        self.entry.grid(row=cell_row, column=1, padx=20, pady=(0, 15))

class App(customtkinter.CTk):
    def __init__(self, width: int, height: int):
        super().__init__()

        self.title("Flight Management System")
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)

        # load images
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + "/assets/bg_gradient.jpg"),
                                               size=(width, height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)
        self.logo_image = customtkinter.CTkImage(Image.open(current_path + "/assets/logo_picture.png"), size=(36, 36))
        self.logo_image_big = customtkinter.CTkImage(Image.open(current_path + "/assets/logo_picture.png"), size=(150, 150))

        # main frame
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=0, sticky="ns")
        self.main_label = customtkinter.CTkLabel(self.main_frame, text="Flight Managemet System\nLogin Page",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.main_label.grid(row=0, column=0, padx=30, pady=(150, 15))
        # choice between logging in and registering
        self.login_button = customtkinter.CTkButton(self.main_frame, corner_radius=0, height=40, border_spacing=10, text="Login",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="center", command=self.login_button_event)
        self.login_button.grid(row=1, column=0, sticky="ew")
        self.register_button = customtkinter.CTkButton(self.main_frame, corner_radius=0, height=40, border_spacing=10, text="Register",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="center", command=self.register_button_event)
        self.register_button.grid(row=2, column=0, sticky="ew")
        # create login frame
        self.login_frame = customtkinter.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.login_frame.grid(row=3, column=0, sticky="ns")
        self.username_login_entry = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="Username")
        self.username_login_entry.grid(row=3, column=0, padx=30, pady=(15, 15))
        self.password_login_entry = customtkinter.CTkEntry(self.login_frame, width=200, show="*", placeholder_text="Password")
        self.password_login_entry.grid(row=4, column=0, padx=30, pady=(0, 15))
        self.login_enter_button = customtkinter.CTkButton(self.login_frame, text="Login", command=self.login_event, width=200)
        self.login_enter_button.grid(row=5, column=0, padx=30, pady=(15, 15))
        # create register frame
        self.register_frame = customtkinter.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.register_frame.grid(row=3, column=0, sticky="ns")
        self.username_register_entry = customtkinter.CTkEntry(self.register_frame, width=200, placeholder_text="Username")
        self.username_register_entry.grid(row=3, column=0, padx=30, pady=(15, 15))
        self.password_register_entry = customtkinter.CTkEntry(self.register_frame, width=200, show="*", placeholder_text="Password")
        self.password_register_entry.grid(row=4, column=0, padx=30, pady=(0, 15))
        self.register_enter_button = customtkinter.CTkButton(self.register_frame, text="Register", command=self.register_event, width=200)
        self.register_enter_button.grid(row=5, column=0, padx=30, pady=(15, 15))

        self.select_frame_by_name("login")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.home_frame.grid_rowconfigure(0, weight=1)
        self.home_frame.grid_columnconfigure(1, weight=1)

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self.home_frame, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="ns")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text=" Flight Management System", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        self.flight_adding_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=60, border_spacing=10, text="Add a flight",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="center", font=customtkinter.CTkFont(size=14), command=self.flight_adding_button_event)
        self.flight_adding_button.grid(row=1, column=0, sticky="ew")
        self.flight_finding_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=60, border_spacing=10, text="Find a flight",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="center", font=customtkinter.CTkFont(size=14), command=self.flight_finding_button_event)
        self.flight_finding_button.grid(row=2, column=0, sticky="ew")
        self.all_flights_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=60, border_spacing=10, text="See all flights",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="center", font=customtkinter.CTkFont(size=14), command=self.all_flights_button_event)
        self.all_flights_button.grid(row=3, column=0, sticky="ew")
        self.logout_button = customtkinter.CTkButton(self.navigation_frame, text="Logout", command=self.back_event, width=200)
        self.logout_button.grid(row=6, column=0, padx=30, pady=(15, 15))

        # create flight adding frame
        self.flight_adding_frame = Flight_add_frame(self, 20)

        # create flight finding frame
        self.flight_finding_frame = Flight_find_frame(self, 20)

        # create another window with a frame with all flights
        self.all_flights_frame = None
        # self.tmp_frame = customtkinter.CTkFrame(self.all_flights_frame, corner_radius=20, width=280)
        # self.tmp_frame.grid(row=0, column=0, padx=10, pady=10)
        # self.tmp_frame2 = customtkinter.CTkFrame(self.all_flights_frame, corner_radius=20, width=280)
        # self.tmp_frame2.grid(row=0, column=1, padx=10, pady=10)
        # self.tmp_frame3 = customtkinter.CTkFrame(self.all_flights_frame, corner_radius=20, width=280)
        # self.tmp_frame3.grid(row=0, column=2, padx=10, pady=10)

    def add_flight(self):
        con = db.connect("application_database.db")
        cur = con.cursor()

        sql = """ SELECT flight_id FROM flights """
        cur.execute(sql)
        result = cur.fetchall()

        if len(result) == 0:
            result.append([0])

        sql = f""" INSERT INTO "flights"
        (flight_id, departure_location, arrival_location, departure_date, arrival_date, departure_time, arrival_time, price)
        VALUES ({result[-1][0] + 1}, "{self.flight_adding_frame.cells[0].entry.get()}", "{self.flight_adding_frame.cells[1].entry.get()}", 
                                                            "{self.flight_adding_frame.cells[2].entry.get()}", "{self.flight_adding_frame.cells[3].entry.get()}",
                                                            "{self.flight_adding_frame.cells[4].entry.get()}", "{self.flight_adding_frame.cells[5].entry.get()}",
                                                            {self.flight_adding_frame.cells[6].entry.get()})
        """
        cur.execute(sql)
        con.commit()
        con.close()

    def find_flight(self):
        cells = []
        for i in range(len(self.flight_finding_frame.cells)):
            information = self.flight_finding_frame.cells[i].entry.get()
            cells.append(information)

        con = db.connect("application_database.db")
        cur = con.cursor()

        sql = """ SELECT * FROM flights """
        cur.execute(sql)
        result = cur.fetchall()

        con.commit()
        con.close()

        Find_flight_window(cells)
        # print(cells)

    def main_select_frame_by_name(self, name):
        # set button color for selected button
        self.flight_adding_button.configure(fg_color=("gray75", "gray25") if name == "adding" else "transparent")
        self.flight_finding_button.configure(fg_color=("gray75", "gray25") if name == "finding" else "transparent")
        self.all_flights_button.configure(fg_color=("gray75", "gray25") if name == "all_flights" else "transparent")

        # show selected frame
        if name == "adding":
            self.flight_adding_frame.grid(row=0, column=1)
        else:
            self.flight_adding_frame.grid_forget()
        if name == "finding":
            self.flight_finding_frame.grid(row=0, column=1)
        else:
            self.flight_finding_frame.grid_forget()
        if name == "all_flights":
            if self.all_flights_frame is None or not self.all_flights_frame.winfo_exists():
                self.all_flights_frame = All_flights_window(self)
            else:
                self.all_flights_frame.focus()

    def flight_adding_button_event(self):
        self.main_select_frame_by_name("adding")
    
    def flight_finding_button_event(self):
        self.main_select_frame_by_name("finding")
    
    def all_flights_button_event(self):
        self.main_select_frame_by_name("all_flights")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.login_button.configure(fg_color=("gray75", "gray25") if name == "login" else "transparent")
        self.register_button.configure(fg_color=("gray75", "gray25") if name == "register" else "transparent")

        # show selected frame
        if name == "login":
            self.login_frame.grid(row=3, column=0, sticky="ns")
        else:
            self.login_frame.grid_forget()
        if name == "register":
            self.register_frame.grid(row=3, column=0, sticky="ns")
        else:
            self.register_frame.grid_forget()
    
    def login_button_event(self):
        self.select_frame_by_name("login")

    def register_button_event(self):
        self.select_frame_by_name("register")

    def login_event(self):
        # check if there is such a user in the database
        con = db.connect("application_database.db")
        cur = con.cursor()
        sql = f" SELECT username, password FROM Users WHERE username='{self.username_login_entry.get()}' AND password='{self.password_login_entry.get()}' "
        cur.execute(sql)
        result = cur.fetchall()
        con.close()

        if len(result) != 0:
            self.main_frame.grid_forget()  # remove login frame
            self.home_frame.grid(row=0, column=0, sticky="nsew")
            self.main_select_frame_by_name("adding")
            self.username_login_entry.delete(0, 100)
            self.password_login_entry.delete(0, 100)

    def register_event(self):
        # add a user to the database
        con = db.connect("application_database.db")
        cur = con.cursor()
        
        sql = """ SELECT user_id FROM users """
        cur.execute(sql)
        result = cur.fetchall()

        sql = f""" INSERT INTO "users"
        (user_id, username, password)
        VALUES ({result[-1][0] + 1}, {self.username_register_entry.get()}, {self.password_register_entry.get()})
        """
        cur.execute(sql)
        con.commit()
        con.close()
        self.username_register_entry.delete(0, 100)
        self.password_register_entry.delete(0, 100)

    def back_event(self):
        self.home_frame.grid_forget()  # remove home frame
        self.main_frame.grid(row=0, column=0, sticky="ns")  # show main frame
        self.login_button_event()

if __name__ == "__main__":
    app = App(1200, 675)
    app.mainloop()
