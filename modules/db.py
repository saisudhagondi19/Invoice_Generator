import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("database/invoicegen.db")
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zipcode TEXT,
            country TEXT,
            phone TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dealers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zipcode TEXT,
            country TEXT,
            phone TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            date TEXT,
            subtotal REAL,
            tax REAL,
            discount REAL,
            total REAL,
            notes TEXT,
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoice_lines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER,
            description TEXT,
            qty INTEGER,
            rate REAL,
            FOREIGN KEY(invoice_id) REFERENCES invoices(id)
        )
        """)

        self.conn.commit()

    # ----------------------------------------------------
    # ADD THESE FUNCTIONS HERE (AFTER create_tables)
    # ----------------------------------------------------

    def get_customer_by_id(self, customer_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE id=?", (customer_id,))
        row = cursor.fetchone()
        if row is None:
            raise ValueError(f"No customer found with ID {customer_id}")
            
        return dict(zip([col[0] for col in cursor.description], row))
        

    def get_dealer_details(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM dealers ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if row is None:
            raise ValueError("No dealer information found! Please add delaer first")
        
        return dict(zip([col[0] for col in cursor.description], row))
        

    # ----------------------------------------------------
    # Existing save_invoice function
    # ----------------------------------------------------
    def save_invoice(self, invoice, lines):
        cursor = self.conn.cursor()

        cursor.execute("""
        INSERT INTO invoices (customer_id, date, subtotal, tax, discount, total, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            invoice["customer_id"],
            invoice["date"],
            invoice["subtotal"],
            invoice["tax"],
            invoice["discount"],
            invoice["total"],
            invoice["notes"]
        ))

        invoice_id = cursor.lastrowid

        for l in lines:
            cursor.execute("""
            INSERT INTO invoice_lines (invoice_id, description, qty, rate)
            VALUES (?, ?, ?, ?)
            """, (
                invoice_id, l["description"], l["qty"], l["rate"]
            ))

        self.conn.commit()
        return invoice_id
