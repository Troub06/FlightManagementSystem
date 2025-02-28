import customtkinter
from PIL import Image
import os
import sqlite3 as db

customtkinter.set_appearance_mode("dark")

# Добавление полетов
# Поиск полетов
# Отчеты/вывод информации

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
        self.report_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=60, border_spacing=10, text="Create a report",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="center", font=customtkinter.CTkFont(size=14), command=self.report_button_event)
        self.report_button.grid(row=3, column=0, sticky="ew")
        self.logout_button = customtkinter.CTkButton(self.navigation_frame, text="Logout", command=self.back_event, width=200)
        self.logout_button.grid(row=6, column=0, padx=30, pady=(15, 15))

        # create flight adding frame
        self.flight_adding_frame = customtkinter.CTkFrame(self.home_frame, corner_radius=0, fg_color="transparent")
        self.flight_adding_frame.grid_columnconfigure(1, weight=1)
        self.flight_adding_label = customtkinter.CTkLabel(self.flight_adding_frame, text="Add a flight",
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.flight_adding_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        self.departure_place_label = customtkinter.CTkLabel(self.flight_adding_frame, text="Departure place:", font=customtkinter.CTkFont(size=15))
        self.departure_place_label.grid(row=1, column=0, padx=(20, 0), pady=(0, 15))
        self.departure_place_entry = customtkinter.CTkEntry(self.flight_adding_frame, width=200)
        self.departure_place_entry.grid(row=1, column=1, padx=20, pady=(0, 15))

        self.arrival_place_label = customtkinter.CTkLabel(self.flight_adding_frame, text="Arrival place:", font=customtkinter.CTkFont(size=15))
        self.arrival_place_label.grid(row=2, column=0, padx=(20, 0), pady=(0, 15))
        self.arrival_place_entry = customtkinter.CTkEntry(self.flight_adding_frame, width=200)
        self.arrival_place_entry.grid(row=2, column=1, padx=20, pady=(0, 15))

        self.departure_date_label = customtkinter.CTkLabel(self.flight_adding_frame, text="Departure date:", font=customtkinter.CTkFont(size=15))
        self.departure_date_label.grid(row=3, column=0, padx=(20, 0), pady=(0, 15))
        self.departure_date_entry = customtkinter.CTkEntry(self.flight_adding_frame, width=200, placeholder_text="dd.mm.yyyy")
        self.departure_date_entry.grid(row=3, column=1, padx=20, pady=(0, 15))

        self.arrival_date_label = customtkinter.CTkLabel(self.flight_adding_frame, text="Arrival date:", font=customtkinter.CTkFont(size=15))
        self.arrival_date_label.grid(row=4, column=0, padx=(20, 0), pady=(0, 15))
        self.arrival_date_entry = customtkinter.CTkEntry(self.flight_adding_frame, width=200, placeholder_text="dd.mm.yyyy")
        self.arrival_date_entry.grid(row=4, column=1, padx=20, pady=(0, 15))

        self.departure_time_label = customtkinter.CTkLabel(self.flight_adding_frame, text="Departure time:", font=customtkinter.CTkFont(size=15))
        self.departure_time_label.grid(row=5, column=0, padx=(20, 0), pady=(0, 15))
        self.departure_time_entry = customtkinter.CTkEntry(self.flight_adding_frame, width=200, placeholder_text="hh:mm")
        self.departure_time_entry.grid(row=5, column=1, padx=20, pady=(0, 15))
        
        self.arrival_time_label = customtkinter.CTkLabel(self.flight_adding_frame, text="Arrival time:", font=customtkinter.CTkFont(size=15))
        self.arrival_time_label.grid(row=6, column=0, padx=(20, 0), pady=(0, 15))
        self.arrival_time_entry = customtkinter.CTkEntry(self.flight_adding_frame, width=200, placeholder_text="hh:mm")
        self.arrival_time_entry.grid(row=6, column=1, padx=20, pady=(0, 15))

        self.price_label = customtkinter.CTkLabel(self.flight_adding_frame, text="Price:", font=customtkinter.CTkFont(size=15))
        self.price_label.grid(row=7, column=0, padx=(20, 0), pady=(0, 15))
        self.price_entry = customtkinter.CTkEntry(self.flight_adding_frame, width=200, placeholder_text="")
        self.price_entry.grid(row=7, column=1, padx=20, pady=(0, 15))

        self.add_button = customtkinter.CTkButton(self.flight_adding_frame, text="Add", command=self.add_flight, width=200)
        self.add_button.grid(row=8, column=0, columnspan=2)

        # create flight finding frame
        self.flight_finding_frame = customtkinter.CTkFrame(self.home_frame, corner_radius=0, fg_color="transparent")
        self.flight_finding_label = customtkinter.CTkLabel(self.flight_finding_frame, text="Finding",
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.flight_finding_label.grid(row=0, column=0, padx=20, pady=20)

        # create report frame
        self.report_frame = customtkinter.CTkFrame(self.home_frame, corner_radius=0, fg_color="transparent")
        self.report_label = customtkinter.CTkLabel(self.report_frame, text="Report",
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.report_label.grid(row=0, column=0, padx=20, pady=20)

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
        VALUES ({result[-1][0] + 1}, "{self.departure_place_entry.get()}", "{self.arrival_place_entry.get()}", 
                                                            "{self.departure_date_entry.get()}", "{self.arrival_date_entry.get()}",
                                                            "{self.departure_time_entry.get()}", "{self.arrival_time_entry.get()}",
                                                            {self.price_entry.get()})
        """
        # Изменить базу данных с DATE на TEXT
        cur.execute(sql)
        con.commit()
        con.close()

    def main_select_frame_by_name(self, name):
        # set button color for selected button
        self.flight_adding_button.configure(fg_color=("gray75", "gray25") if name == "adding" else "transparent")
        self.flight_finding_button.configure(fg_color=("gray75", "gray25") if name == "finding" else "transparent")
        self.report_button.configure(fg_color=("gray75", "gray25") if name == "report" else "transparent")

        # show selected frame
        if name == "adding":
            self.flight_adding_frame.grid(row=0, column=1, sticky="ns")
        else:
            self.flight_adding_frame.grid_forget()
        if name == "finding":
            self.flight_finding_frame.grid(row=0, column=1, sticky="ns")
        else:
            self.flight_finding_frame.grid_forget()
        if name == "report":
            self.report_frame.grid(row=0, column=1, sticky="ns")
        else:
            self.report_frame.grid_forget()

    def flight_adding_button_event(self):
        self.main_select_frame_by_name("adding")
    
    def flight_finding_button_event(self):
        self.main_select_frame_by_name("finding")
    
    def report_button_event(self):
        self.main_select_frame_by_name("report")

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
