import tkinter as tk
from tkinter import ttk
from modules.invoice_form import InvoiceForm
from modules.customer_form import CustomerForm
from modules.dealer_form import DealerForm
from modules.db import Database

class MainUI:
    def __init__(self, root):
        self.root = root
        self.root.title("InvoiceGen")
        self.root.geometry("900x600")

        self.db = Database()
        self.build_ui()

    def build_ui(self):
        notebook = ttk.Notebook(self.root)

        invoice_page = InvoiceForm(notebook, self.db)
        customer_page = CustomerForm(notebook, self.db)
        dealer_page = DealerForm(notebook, self.db)

        notebook.add(invoice_page, text="Create Invoice")
        notebook.add(customer_page, text="Customers")
        notebook.add(dealer_page, text="Dealers")

        notebook.pack(expand=True, fill="both")
