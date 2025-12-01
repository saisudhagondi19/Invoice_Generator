import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
from modules.pdf_generator import generate_invoice_pdf

class InvoiceForm(ttk.Frame):
    def __init__(self, container, db):
        super().__init__(container)
        self.db = db
        self.lines = []
        self.build_form()

    def build_form(self):
        # Customer ID
        ttk.Label(self, text="Customer ID").grid(row=0, column=0, padx=5, pady=5)
        self.customer_id = ttk.Entry(self)
        self.customer_id.grid(row=0, column=1, padx=5, pady=5)

        # Date
        ttk.Label(self, text="Date").grid(row=1, column=0, padx=5, pady=5)
        self.date = ttk.Entry(self)
        self.date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date.grid(row=1, column=1, padx=5, pady=5)

        # Items Frame
        self.items_frame = ttk.LabelFrame(self, text="Items")
        self.items_frame.grid(row=2, column=0, columnspan=6, pady=10)

        # Column Headers
        ttk.Label(self.items_frame, text="Description").grid(row=0, column=0, padx=5)
        ttk.Label(self.items_frame, text="Qty").grid(row=0, column=1, padx=5)
        ttk.Label(self.items_frame, text="Rate").grid(row=0, column=2, padx=5)
        ttk.Label(self.items_frame, text="Tax %").grid(row=0, column=3, padx=5)
        ttk.Label(self.items_frame, text="Discount %").grid(row=0, column=4, padx=5)
        ttk.Label(self.items_frame, text="Action").grid(row=0, column=5, padx=5)

        # First empty row
        self.add_item_row()

        # Buttons
        ttk.Button(self, text="Add Item", command=self.add_item_row).grid(row=3, column=0, pady=5)
        ttk.Button(self, text="Save Invoice", command=self.save_invoice).grid(row=4, column=0, pady=5)
        ttk.Button(self, text="Export PDF", command=self.export_pdf).grid(row=4, column=1, pady=5)

    def add_item_row(self):
        row = len(self.lines) + 1

        desc = ttk.Entry(self.items_frame, width=30)
        desc.grid(row=row, column=0, padx=5, pady=2)

        qty = ttk.Entry(self.items_frame, width=10)
        qty.grid(row=row, column=1, padx=5, pady=2)

        rate = ttk.Entry(self.items_frame, width=10)
        rate.grid(row=row, column=2, padx=5, pady=2)

        tax = ttk.Entry(self.items_frame, width=10)
        tax.grid(row=row, column=3, padx=5, pady=2)

        discount = ttk.Entry(self.items_frame, width=10)
        discount.grid(row=row, column=4, padx=5, pady=2)

        remove_btn = ttk.Button(
            self.items_frame, text="Remove",
            command=lambda r=row: self.remove_item_row(r)
        )
        remove_btn.grid(row=row, column=5, padx=5, pady=2)

        self.lines.append({
            "desc": desc,
            "qty": qty,
            "rate": rate,
            "tax": tax,
            "discount": discount,
            "btn": remove_btn
        })

    def remove_item_row(self, row_index):
        line = self.lines[row_index - 1]
        for widget in line.values():
            if isinstance(widget, ttk.Entry) or isinstance(widget, ttk.Button):
                widget.destroy()

        self.lines.pop(row_index - 1)

        for idx, line in enumerate(self.lines, start=1):
            line["btn"].config(command=lambda r=idx: self.remove_item_row(r))
            line["desc"].grid(row=idx, column=0, padx=5, pady=2)
            line["qty"].grid(row=idx, column=1, padx=5, pady=2)
            line["rate"].grid(row=idx, column=2, padx=5, pady=2)
            line["tax"].grid(row=idx, column=3, padx=5, pady=2)
            line["discount"].grid(row=idx, column=4, padx=5, pady=2)
            line["btn"].grid(row=idx, column=5, padx=5, pady=2)

    def get_invoice_items(self):
        items = []
        subtotal = 0
        total_tax = 0
        total_discount = 0

        for row in self.lines:
            desc = row["desc"].get().strip()
            qty = row["qty"].get().strip()
            rate = row["rate"].get().strip()
            tax = row["tax"].get().strip()
            discount = row["discount"].get().strip()

            if not desc or not qty or not rate:
                raise ValueError("Description, Qty and Rate are required for all items.")

            try:
                qty = int(qty)
                rate = float(rate)
                tax = float(tax) if tax else 0
                discount = float(discount) if discount else 0
            except ValueError:
                raise ValueError("Qty must be integer; Rate, Tax %, Discount % must be numeric.")

            item_total = qty * rate
            item_tax = item_total * (tax / 100)
            item_discount = item_total * (discount / 100)

            subtotal += item_total
            total_tax += item_tax
            total_discount += item_discount

            items.append({
                "description": desc,
                "qty": qty,
                "rate": rate,
                "tax_percent": tax,
                "discount_percent": discount,
                "total": item_total
            })

        total_amount = subtotal + total_tax - total_discount
        return items, subtotal, total_tax, total_discount, total_amount

    def save_invoice(self):
        try:
            customer_id = self.customer_id.get().strip()
            if not customer_id:
                messagebox.showerror("Error", "Customer ID is required.")
                return

            items, subtotal, total_tax, total_discount, total_amount = self.get_invoice_items()

            invoice = {
                "customer_id": int(customer_id),
                "date": self.date.get(),
                "subtotal": subtotal,
                "tax": total_tax,
                "discount": total_discount,
                "total": total_amount,
                "notes": ""
            }

            invoice_id = self.db.save_invoice(invoice, items)
            messagebox.showinfo("Saved", f"Invoice ID {invoice_id} saved successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_pdf(self):
        try:
            os.makedirs("exports", exist_ok=True)
            filename = f"exports/invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

            items, subtotal, total_tax, total_discount, total_amount = self.get_invoice_items()

            customer_id = self.customer_id.get().strip()
            if not customer_id:
                raise ValueError("Customer ID is required.")

            invoice = {
                "customer_id": int(customer_id),
                "date": self.date.get(),
                "subtotal": subtotal,
                "tax": total_tax,
                "discount": total_discount,
                "total": total_amount,
                "notes": ""
            }

            # Save invoice and get invoice_id
            invoice_id = self.db.save_invoice(invoice, items)
            invoice["invoice_id"] = invoice_id

            # Fetch customer and dealer
            customer = self.db.get_customer_by_id(invoice["customer_id"])
            dealer = self.db.get_dealer_details()

            # Generate PDF
            generate_invoice_pdf(invoice, items, dealer, customer, filename)

            messagebox.showinfo("PDF Exported", f"PDF saved to {filename}")

            self.clear_form()

        except Exception as e:
            messagebox.showerror("PDF Error", str(e))

    def clear_form(self):
        self.customer_id.delete(0, tk.END)
        self.date.delete(0, tk.END)
        self.date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        for line in self.lines:
            for widget in line.values():
                if isinstance(widget, ttk.Entry) or isinstance(widget, ttk.Button):
                    widget.destroy()

        self.lines = []
        self.add_item_row()
