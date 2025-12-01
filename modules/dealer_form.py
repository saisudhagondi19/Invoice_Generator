import tkinter as tk
from tkinter import ttk, messagebox

class DealerForm(ttk.Frame):
    def __init__(self, container, db):
        super().__init__(container)
        self.db = db
        self.build_form()

    def build_form(self):
        # First Name
        ttk.Label(self, text="First Name").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.first_name = ttk.Entry(self, width=30)
        self.first_name.grid(row=0, column=1, padx=5, pady=5)

        # Last Name
        ttk.Label(self, text="Last Name").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.last_name = ttk.Entry(self, width=30)
        self.last_name.grid(row=1, column=1, padx=5, pady=5)

        # Address
        ttk.Label(self, text="Address").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.address = ttk.Entry(self, width=30)
        self.address.grid(row=2, column=1, padx=5, pady=5)

        # City
        ttk.Label(self, text="City").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.city = ttk.Entry(self, width=30)
        self.city.grid(row=3, column=1, padx=5, pady=5)

        # State
        ttk.Label(self, text="State").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.state = ttk.Entry(self, width=30)
        self.state.grid(row=4, column=1, padx=5, pady=5)

        # Zip Code
        ttk.Label(self, text="Zip Code").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.zipcode = ttk.Entry(self, width=30)
        self.zipcode.grid(row=5, column=1, padx=5, pady=5)

        # Country
        ttk.Label(self, text="Country").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.country = ttk.Entry(self, width=30)
        self.country.grid(row=6, column=1, padx=5, pady=5)

        # Phone Number
        ttk.Label(self, text="Phone Number").grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.phone = ttk.Entry(self, width=30)
        self.phone.grid(row=7, column=1, padx=5, pady=5)

        # Save button
        ttk.Button(self, text="Save Dealer", command=self.save_dealer).grid(row=8, column=0, columnspan=2, pady=10)

    def save_dealer(self):
        cursor = self.db.conn.cursor()
        cursor.execute(
            """
            INSERT INTO dealers 
            (first_name, last_name, address, city, state, zipcode, country, phone) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                self.first_name.get(),
                self.last_name.get(),
                self.address.get(),
                self.city.get(),
                self.state.get(),
                self.zipcode.get(),
                self.country.get(),
                self.phone.get()
            )
        )
        self.db.conn.commit()

        messagebox.showinfo("Saved", "Dealer added successfully!")

        # Clear fields
        for field in [
            self.first_name, self.last_name, self.address,
            self.city, self.state, self.zipcode,
            self.country, self.phone
        ]:
            field.delete(0, tk.END)
