# Day 08 – Inventory & Billing System

## Objective

Build an Inventory & Billing System in Python that manages product records (add, update, delete), generates customer bills with GST and discount calculations, stores data using JSON files, generates a daily sales report, and exports invoices as TXT or CSV files.

## Features Implemented

1. **Add Product:** Add a new product (id, name, price, qty).
2. **View Products:** See all current products.
3. **Update Quantity:** Change the stock for an existing product.
4. **Delete Product:** Remove a product.
5. **Generate Bill:**
   - Add items by Product ID.
   - Calculates Subtotal, Discount, GST (18%), and Net Amount.
   - Auto-updates the product stock.
6. **Sales Report:** Prints a summary of today's sales.
7. **Export:** Export generated invoice to `.txt` or `.csv`.
8. **Data Storage:** Uses `products.json` and `sales.json` to store data permanently.

## How to Run

```bash
python inventory_billing_system.py
```

## Files

- `inventory_billing_system.py`: The main program.
## Output Screenshots

<img width="1097" height="852" alt="Screenshot 2026-06-20 180841" src="https://github.com/user-attachments/assets/c4305bb7-82fd-44c6-a3c5-043002caddf2" />
<img width="1088" height="843" alt="Screenshot 2026-06-20 180859" src="https://github.com/user-attachments/assets/88e4b826-2ae2-4f6f-af2a-f62808552325" />
<img width="1103" height="855" alt="Screenshot 2026-06-20 180919" src="https://github.com/user-attachments/assets/9ef04c19-ea54-4ae3-8e5b-449f0c810582" />
<img width="921" height="806" alt="Screenshot 2026-06-20 180943" src="https://github.com/user-attachments/assets/73abd8e3-8276-4c56-9f02-865463da9cbb" />
<img width="912" height="800" alt="Screenshot 2026-06-20 180959" src="https://github.com/user-attachments/assets/eeb10ddc-0965-4a5a-9131-9e425083634a" />
<img width="607" height="485" alt="Screenshot 2026-06-20 182021" src="https://github.com/user-attachments/assets/469d78b2-e644-4ada-9ddc-c7a4f6f9dcf2" />

