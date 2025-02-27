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

        # background
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + "/assets/bg_gradient.jpg"),
                                               size=(width, height))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

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
        self.username_login_entry = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="username")
        self.username_login_entry.grid(row=3, column=0, padx=30, pady=(15, 15))
        self.password_login_entry = customtkinter.CTkEntry(self.login_frame, width=200, show="*", placeholder_text="password")
        self.password_login_entry.grid(row=4, column=0, padx=30, pady=(0, 15))
        self.login_button = customtkinter.CTkButton(self.login_frame, text="Login", command=self.login_event, width=200)
        self.login_button.grid(row=5, column=0, padx=30, pady=(15, 15))
        # create register frame
        self.register_frame = customtkinter.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.register_frame.grid(row=3, column=0, sticky="ns")
        self.username_register_entry = customtkinter.CTkEntry(self.register_frame, width=200, placeholder_text="username")
        self.username_register_entry.grid(row=3, column=0, padx=30, pady=(15, 15))
        self.password_register_entry = customtkinter.CTkEntry(self.register_frame, width=200, show="*", placeholder_text="password")
        self.password_register_entry.grid(row=4, column=0, padx=30, pady=(0, 15))
        self.register_button = customtkinter.CTkButton(self.register_frame, text="Register", command=self.register_event, width=200)
        self.register_button.grid(row=5, column=0, padx=30, pady=(15, 15))

        self.select_frame_by_name("login")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_label = customtkinter.CTkLabel(self.home_frame, text="Flight Management System\nHome Page",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.home_label.grid(row=0, column=0, padx=30, pady=(30, 15))
        self.logout_button = customtkinter.CTkButton(self.home_frame, text="Logout", command=self.back_event, width=200)
        self.logout_button.grid(row=1, column=0, padx=30, pady=(15, 15))

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
            self.home_frame.grid(row=0, column=0, sticky="nsew", padx=100)  # show main frame

    def register_event(self):
        # add a user to the database
        con = db.connect("application_database.db")
        cur = con.cursor()
        
        sql = """ SELECT user_id FROM users """
        cur.execute(sql)
        result = cur.fetchall()
        # print(result[-1][0])

        sql = f""" INSERT INTO "users"
        (user_id, username, password)
        VALUES ({result[-1][0] + 1}, {self.username_register_entry.get()}, {self.password_register_entry.get()})
        """
        cur.execute(sql)
        con.commit()
        con.close()

    def back_event(self):
        self.home_frame.grid_forget()  # remove home frame
        self.main_frame.grid(row=0, column=0, sticky="ns")  # show main frame


if __name__ == "__main__":
    app = App(900, 600)
    app.mainloop()

