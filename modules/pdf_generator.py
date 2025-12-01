from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors

def generate_invoice_pdf(invoice, items, dealer, customer, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # ---------------- LOGO (top-left) ----------------
    try:
        logo = ImageReader("assets/logo.png")
        c.drawImage(logo, 40, height - 110, width=70, height=70, mask='auto')
    except:
        c.setFont("Helvetica", 10)
        c.drawString(40, height - 40, "Logo Not Found")

    # ---------------- INVOICE TITLE (center header) ----------------
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(width / 2, height - 70, "INVOICE")

    # ================================================================
    #                DEALER INFORMATION BOX
    # ================================================================
    dealer_box_x = 40
    dealer_box_y = height - 260
    dealer_box_w = 250
    dealer_box_h = 120

    c.rect(dealer_box_x, dealer_box_y, dealer_box_w, dealer_box_h)

    # Title inside the box
    c.setFont("Helvetica-Bold", 12)
    c.drawString(dealer_box_x + 10, dealer_box_y + dealer_box_h - 20, "Dealer Information")

    # Dealer content
    c.setFont("Helvetica", 11)
    y = dealer_box_y + dealer_box_h - 40
    line_gap = 15

    c.drawString(dealer_box_x + 10, y, f"Name: {dealer['first_name']} {dealer['last_name']}")
    y -= line_gap
    c.drawString(dealer_box_x + 10, y, f"Address 1: {dealer['address']}")
    y -= line_gap
    c.drawString(dealer_box_x + 10, y, f"Address 2: {dealer['city']}, {dealer['state']} {dealer['zipcode']}")
    y -= line_gap
    c.drawString(dealer_box_x + 10, y, f"Country: {dealer['country']}")
    y -= line_gap
    c.drawString(dealer_box_x + 10, y, f"Phone: {dealer['phone']}")

    # ================================================================
    #                CUSTOMER INFORMATION BOX
    # ================================================================
    customer_box_x = 330
    customer_box_y = height - 280
    customer_box_w = 250
    customer_box_h = 140

    c.rect(customer_box_x, customer_box_y, customer_box_w, customer_box_h)

    # Title inside box
    c.setFont("Helvetica-Bold", 12)
    c.drawString(customer_box_x + 10, customer_box_y + customer_box_h - 20, "Customer Information")

    # Customer content
    c.setFont("Helvetica", 11)
    y = customer_box_y + customer_box_h - 40

    c.drawString(customer_box_x + 10, y, f"Name: {customer['first_name']} {customer['last_name']}")
    y -= line_gap
    c.drawString(customer_box_x + 10, y, f"Address 1: {customer['address']}")
    y -= line_gap
    c.drawString(customer_box_x + 10, y, f"Address 2: {customer['city']}, {customer['state']} {customer['zipcode']}")
    y -= line_gap
    c.drawString(customer_box_x + 10, y, f"Country: {customer['country']}")
    y -= line_gap
    c.drawString(customer_box_x + 10, y, f"Phone: {customer['phone']}")

    # ================================================================
    #                INVOICE DETAILS (Invoice ID + Date)
    # ================================================================
    c.setFont("Helvetica-Bold", 12)
    y_invoice = customer_box_y - 20
    c.drawString(40, y_invoice, f"Invoice ID: {invoice['invoice_id']}")
    c.drawRightString(width - 40, y_invoice, f"Date: {invoice['date']}")

    # ------------------------------------------------
    #                    TABLE HEADER
    # ------------------------------------------------
    y = y_invoice - 30
    headers = ["Description", "Qty", "Rate", "Tax %", "Discount", "Total"]
    x_positions = [40, 250, 310, 380, 450, 520]
    col_widths = [210, 60, 70, 70, 70, 70]
    row_height = 25

    c.setFillColor(colors.lightgrey)
    c.rect(40, y, sum(col_widths), row_height, fill=True)
    c.setFillColor(colors.black)

    c.setFont("Helvetica-Bold", 12)
    for header, x in zip(headers, x_positions):
        c.drawString(x + 5, y + 7, header)

    y -= row_height

    # ------------------------------------------------
    #                    TABLE ITEMS
    # ------------------------------------------------
    c.setFont("Helvetica", 11)
    for item in items:
        item_total = item["qty"] * item["rate"]
        item_tax = item_total * (item["tax_percent"] / 100)
        item_discount = item_total * (item["discount_percent"] / 100)
        final_total = item_total + item_tax - item_discount

        c.rect(40, y, sum(col_widths), row_height)

        c.drawString(x_positions[0] + 5, y + 7, item["description"])
        c.drawRightString(x_positions[1] + col_widths[1] - 5, y + 7, str(item["qty"]))
        c.drawRightString(x_positions[2] + col_widths[2] - 5, y + 7, f"${item['rate']:.2f}")
        c.drawRightString(x_positions[3] + col_widths[3] - 5, y + 7, f"{item['tax_percent']}%")
        c.drawRightString(x_positions[4] + col_widths[4] - 5, y + 7, f"{item['discount_percent']}%")
        c.drawRightString(x_positions[5] + col_widths[5] - 5, y + 7, f"${final_total:.2f}")

        y -= row_height

    # ------------------------------------------------
    #                    SUMMARY
    # ------------------------------------------------
    y -= 20
    c.setFont("Helvetica-Bold", 12)

    c.drawRightString(width - 40, y, f"Subtotal: ${invoice['subtotal']:.2f}")
    c.drawRightString(width - 40, y - 20, f"Total Tax: ${invoice['tax']:.2f}")
    c.drawRightString(width - 40, y - 40, f"Total Discount: ${invoice['discount']:.2f}")
    c.drawRightString(width - 40, y - 60, f"Grand Total: ${invoice['total']:.2f}")

    # ------------------------------------------------
    #                    FOOTER
    # ------------------------------------------------
    c.setFont("Helvetica-Oblique", 12)
    c.drawCentredString(width / 2, 60, "Thank you for your business!")
    c.drawCentredString(width / 2, 42, "Please contact us for any questions regarding this invoice.")

    c.save()
