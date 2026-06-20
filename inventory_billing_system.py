import json
import csv
import datetime

# --- Functions ---

def add_product():
    try:
        file = open("products.json", "r")
        products = json.load(file)
        file.close()
    except:
        products = []

    pid = input("Enter Product ID: ")
    
    for p in products:
        if p["id"] == pid:
            print("This ID already exists.")
            return
            
    name = input("Enter Product Name: ")
    price = float(input("Enter Price: "))
    qty = int(input("Enter Quantity: "))
    
    new_product = {}
    new_product["id"] = pid
    new_product["name"] = name
    new_product["price"] = price
    new_product["quantity"] = qty
    
    products.append(new_product)
    
    file = open("products.json", "w")
    json.dump(products, file)
    file.close()
    
    print("Product added.")

def view_products():
    try:
        file = open("products.json", "r")
        products = json.load(file)
        file.close()
    except:
        products = []
    
    print("All Products:")
    for p in products:
        print(p["id"], "-", p["name"], "-", p["price"], "-", p["quantity"])

def update_qty():
    try:
        file = open("products.json", "r")
        products = json.load(file)
        file.close()
    except:
        products = []
    
    pid = input("Enter Product ID to update: ")
    found = False
    
    for p in products:
        if p["id"] == pid:
            new_qty = int(input("Enter new quantity: "))
            p["quantity"] = new_qty
            found = True
            print("Quantity updated.")
            
    if found == False:
        print("Product not found.")
        
    file = open("products.json", "w")
    json.dump(products, file)
    file.close()

def delete_product():
    try:
        file = open("products.json", "r")
        products = json.load(file)
        file.close()
    except:
        products = []
    
    pid = input("Enter Product ID to delete: ")
    found = False
    
    new_list = []
    for p in products:
        if p["id"] == pid:
            found = True
            print("Product deleted.")
        else:
            new_list.append(p)
            
    if found == False:
        print("Product not found.")
        
    file = open("products.json", "w")
    json.dump(new_list, file)
    file.close()

def generate_bill():
    try:
        file = open("products.json", "r")
        products = json.load(file)
        file.close()
    except:
        products = []
    
    customer = input("Enter Customer Name: ")
    cart = []
    
    while True:
        pid = input("Enter Product ID (or 'done' to stop): ")
        if pid == "done":
            break
            
        found = False
        for p in products:
            if p["id"] == pid:
                found = True
                qty_to_buy = int(input("Enter quantity: "))
                
                if qty_to_buy <= p["quantity"]:
                    p["quantity"] = p["quantity"] - qty_to_buy
                    
                    item = {}
                    item["name"] = p["name"]
                    item["price"] = p["price"]
                    item["qty"] = qty_to_buy
                    item["total"] = p["price"] * qty_to_buy
                    cart.append(item)
                    print("Added to cart.")
                else:
                    print("Not enough stock.")
                    
        if found == False:
            print("Product not found.")
            
    if len(cart) == 0:
        print("Cart is empty.")
        return
        
    subtotal = 0
    for item in cart:
        subtotal = subtotal + item["total"]
        
    discount_percent = float(input("Enter discount percentage: "))
    discount_amount = (subtotal * discount_percent) / 100
    after_discount = subtotal - discount_amount
    
    gst_amount = (after_discount * 18) / 100
    net_amount = after_discount + gst_amount
    
    now = datetime.datetime.now()
    invoice_num = "INV-" + str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second)
    date_str = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
    
    invoice = {}
    invoice["invoice_num"] = invoice_num
    invoice["date"] = date_str
    invoice["customer"] = customer
    invoice["items"] = cart
    invoice["subtotal"] = subtotal
    invoice["discount"] = discount_amount
    invoice["gst"] = gst_amount
    invoice["net_amount"] = net_amount
    
    try:
        s_file = open("sales.json", "r")
        sales = json.load(s_file)
        s_file.close()
    except:
        sales = []
        
    sales.append(invoice)
    
    s_file = open("sales.json", "w")
    json.dump(sales, s_file)
    s_file.close()
    
    p_file = open("products.json", "w")
    json.dump(products, p_file)
    p_file.close()
    
    print("----- BILL -----")
    print("Invoice:", invoice_num)
    print("Date:", date_str)
    print("Customer:", customer)
    print("Items:")
    for i in cart:
        print(" -", i["name"], "x", i["qty"], "=", i["total"])
    print("Subtotal:", subtotal)
    print("Discount:", discount_amount)
    print("GST (18%):", gst_amount)
    print("Net Amount:", net_amount)
    print("----------------")
    
    export = input("Export to txt or csv? (txt/csv/no): ")
    if export == "txt":
        txt_file = open(invoice_num + ".txt", "w")
        txt_file.write("----- BILL -----\n")
        txt_file.write("Invoice: " + invoice_num + "\n")
        txt_file.write("Date: " + date_str + "\n")
        txt_file.write("Customer: " + customer + "\n")
        txt_file.write("Items:\n")
        for i in cart:
            txt_file.write(" - " + i["name"] + " x " + str(i["qty"]) + " = " + str(i["total"]) + "\n")
        txt_file.write("Subtotal: " + str(subtotal) + "\n")
        txt_file.write("Discount: " + str(discount_amount) + "\n")
        txt_file.write("GST (18%): " + str(gst_amount) + "\n")
        txt_file.write("Net Amount: " + str(net_amount) + "\n")
        txt_file.write("----------------\n")
        txt_file.close()
        print("Exported to txt file.")
    elif export == "csv":
        csv_file = open(invoice_num + ".csv", "w", newline='')
        writer = csv.writer(csv_file)
        writer.writerow(["Invoice Num", "Date", "Customer", "Item", "Qty", "Price", "Total"])
        for i in cart:
            writer.writerow([invoice_num, date_str, customer, i["name"], i["qty"], i["price"], i["total"]])
        writer.writerow([])
        writer.writerow(["", "", "", "", "", "Subtotal", subtotal])
        writer.writerow(["", "", "", "", "", "Discount", discount_amount])
        writer.writerow(["", "", "", "", "", "GST (18%)", gst_amount])
        writer.writerow(["", "", "", "", "", "Net Amount", net_amount])
        csv_file.close()
        print("Exported to csv file.")

def daily_sales():
    try:
        file = open("sales.json", "r")
        sales = json.load(file)
        file.close()
    except:
        print("No sales data.")
        return
        
    now = datetime.datetime.now()
    today = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
    
    print("Sales for today (" + today + "):")
    
    total_revenue = 0
    for s in sales:
        if s["date"] == today:
            print(s["invoice_num"], "-", s["customer"], "-", s["net_amount"])
            total_revenue = total_revenue + s["net_amount"]
            
    print("Total Revenue:", total_revenue)

# --- Menu ---

while True:
    print("\n1. Add Product")
    print("2. View Products")
    print("3. Update Quantity")
    print("4. Delete Product")
    print("5. Generate Bill")
    print("6. Daily Sales Report")
    print("7. Exit")
    
    choice = input("Enter choice: ")
    
    if choice == "1":
        add_product()
    elif choice == "2":
        view_products()
    elif choice == "3":
        update_qty()
    elif choice == "4":
        delete_product()
    elif choice == "5":
        generate_bill()
    elif choice == "6":
        daily_sales()
    elif choice == "7":
        print("Bye!")
        break
    else:
        print("Wrong choice.")
