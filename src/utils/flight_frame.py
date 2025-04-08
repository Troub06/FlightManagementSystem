import customtkinter

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
