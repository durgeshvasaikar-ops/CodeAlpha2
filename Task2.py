# TASK 2: Stock Portfolio Tracker 

import tkinter as tk
from tkinter import messagebox
import yfinance as yf
import matplotlib.pyplot as plt

portfolio = {}

# -------- Get Live Price --------
def get_live_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        return round(data["Close"].iloc[-1], 2)
    except:
        return None

# -------- Add Stock --------
def add_stock():
    stock = stock_entry.get().upper().strip()
    qty = qty_entry.get()

    if not qty.isdigit():
        messagebox.showerror("Error", "Enter valid quantity!")
        return

    price = get_live_price(stock)

    if price is None:
        messagebox.showerror("Error", "Stock not found!")
        return

    qty = int(qty)
    portfolio[stock] = portfolio.get(stock, 0) + qty

    result_box.insert(tk.END,
        f"✅ Added {stock} - {qty} shares @ {price}\n")

# -------- Calculate Total --------
def calculate_total():
    total = 0
    result_box.insert(tk.END, "\n📊 Investment Summary:\n")

    for stock, qty in portfolio.items():
        price = get_live_price(stock)
        investment = price * qty
        total += investment
        result_box.insert(tk.END,
            f"{stock}: {qty} × {price} = {round(investment,2)}\n")

    result_box.insert(tk.END,
        f"\n💰 Total Investment = {round(total,2)}\n\n")

# -------- Show Graph --------
def show_chart():
    stock = stock_entry.get().upper().strip()

    if stock == "":
        messagebox.showerror("Error", "Enter stock symbol!")
        return

    try:
        data = yf.Ticker(stock).history(period="1mo")

        if data.empty:
            messagebox.showerror("Error", "No data found!")
            return

        plt.figure()
        plt.plot(data.index, data["Close"])
        plt.title(f"{stock} Price Chart (1 Month)")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.show()

    except:
        messagebox.showerror("Error", "Failed to load chart!")

# -------- GUI --------
root = tk.Tk()
root.title("Live Stock Tracker + Chart")
root.geometry("420x520")
root.configure(bg="#1e1e2f")

title = tk.Label(root,
    text="📈 Stock Tracker with Graph",
    font=("Arial",16,"bold"),
    bg="#1e1e2f",
    fg="#00ffcc")
title.pack(pady=10)

frame = tk.Frame(root,bg="#2a2a40",padx=15,pady=15)
frame.pack(pady=10)

tk.Label(frame,text="Stock Name",
         bg="#2a2a40",fg="white").pack()

stock_entry = tk.Entry(frame,font=("Arial",11))
stock_entry.pack(pady=5)

tk.Label(frame,text="Quantity",
         bg="#2a2a40",fg="white").pack()

qty_entry = tk.Entry(frame,font=("Arial",11))
qty_entry.pack(pady=5)

btn_frame = tk.Frame(root,bg="#1e1e2f")
btn_frame.pack()

tk.Button(btn_frame,text="Add Stock",
          command=add_stock,
          bg="#4CAF50",fg="white",
          width=15).grid(row=0,column=0,padx=5,pady=10)

tk.Button(btn_frame,text="Calculate Total",
          command=calculate_total,
          bg="#2196F3",fg="white",
          width=15).grid(row=0,column=1,padx=5,pady=10)

tk.Button(root,text="📈 Show Chart",
          command=show_chart,
          bg="#ff9800",
          fg="white",
          width=20).pack(pady=5)

result_box = tk.Text(root,height=15,
                     bg="#111122",
                     fg="#00ffcc",
                     font=("Consolas",10))
result_box.pack(padx=10,pady=10,fill="both",expand=True)

root.mainloop()
