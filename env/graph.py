# import tkinter as tk
from tkinter import ttk
import mysql.connector
import customtkinter
from customtkinter import *
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 't1121tdn',
    'database': 'Pizza'
}

def update_graph():
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    cursor.execute('SELECT pizza_name, quantity FROM pizza')
    results = cursor.fetchall()
    conn.close()

    pizzas = [result[0] for result in results]
    quantities = [result[1] for result in results]

    fig = plt.figure(figsize=(4, 4), dpi=50)
    sns.barplot(x=pizzas, y=quantities, palette='viridis', hue=pizzas, legend=False)
    plt.xlabel('Pizza Name')
    plt.ylabel('Quantity')
    plt.title('Pizza Quantity Statistics')

    canvas = FigureCanvasTkAgg(fig, master=frame2)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

def update_graph_sale():
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(Margherita_Pizza), SUM(BBQ_Pizza), SUM(SeaFood_Pizza), SUM(total_price) AS total_profit FROM orders')
    sales_results = cursor.fetchone()

    pizzas = ['Margherita\nPizza', 'BBQ\nPizza', 'SeaFood\nPizza']
    quantities_sold = [sales_results[0], sales_results[1], sales_results[2]]
    total_profit = sales_results[3]

    cursor.execute('SELECT SUM(Margherita_Pizza*200), SUM(BBQ_Pizza*250), SUM(SeaFood_Pizza*300) FROM orders')
    profits = cursor.fetchone()
    individual_profits = [profits[0], profits[1], profits[2]]

    fig = plt.figure(figsize=(6, 4), dpi=50)

    plt.subplot(1, 3, 1)
    sns.barplot(x=pizzas, y=quantities_sold, hue=pizzas, dodge=False)
    plt.xlabel('Pizza Name')
    plt.ylabel('Quantity Sold')
    plt.title('Pizza Sales Quantity')
    plt.xticks(fontsize=8) 

    plt.subplot(1, 3, 2)
    sns.barplot(x=pizzas, y=individual_profits, hue=pizzas, dodge=False)
    plt.xlabel('Pizza Name')
    plt.ylabel('Profit (₹)')
    plt.title('Individual Pizza Profits')
    plt.xticks(fontsize=8) 
    
    plt.subplot(1, 3, 3)
    sns.barplot(x=['Total Profit'], y=[total_profit], hue=['Total Profit'], palette='muted', legend=True)
    plt.xlabel('Total Profit (₹)')
    plt.title('Total Profit')
    plt.legend().remove() 

    plt.tight_layout()
    conn.close()

    canvas = FigureCanvasTkAgg(fig, master=frame2)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=3, column=3, columnspan=3, padx=5, pady=5, sticky='nsew')


def update_quantity_and_price():
    selected_item = tree.focus()
    if selected_item:
        pizza_id = tree.item(selected_item)['values'][0]
        new_quantity = quantity_entry.get().strip()
        new_price = price_entry.get().strip()
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        if new_quantity:
            cursor.execute('UPDATE pizza SET quantity = %s WHERE id = %s', (new_quantity, pizza_id))
        if new_price:
            cursor.execute('UPDATE pizza SET price = %s WHERE id = %s', (new_price, pizza_id))
        conn.commit()
        conn.close()
        display_table()
        update_graph()


def display_table():
    for row in tree.get_children():
        tree.delete(row)
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    cursor.execute('SELECT id, pizza_name, price, quantity FROM pizza')
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)
    conn.close()


def display_orders():
    for row in orders_tree.get_children():
        orders_tree.delete(row)
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders')
    for row in cursor.fetchall():
        orders_tree.insert('', 'end', values=row)
    conn.close()


def delete_order():
    selected_item = orders_tree.focus()
    if selected_item:
        order_id = orders_tree.item(selected_item)['values'][0]
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()

        # Retrieve the quantities of each pizza in the deleted order
        cursor.execute('SELECT Margherita_Pizza, BBQ_Pizza, SeaFood_Pizza FROM orders WHERE id = %s', (order_id,))
        order_quantities = cursor.fetchone()

        # Unpack the order quantities
        margherita_quantity, bbq_quantity, seafood_quantity = order_quantities

        # Update the quantities in the pizza table separately for each pizza type
        cursor.execute('UPDATE pizza SET quantity = quantity + %s WHERE id = 1', (margherita_quantity,))
        cursor.execute('UPDATE pizza SET quantity = quantity + %s WHERE id = 2', (bbq_quantity,))
        cursor.execute('UPDATE pizza SET quantity = quantity + %s WHERE id = 3', (seafood_quantity,))


        cursor.execute('DELETE FROM orders WHERE id = %s', (order_id,))
        conn.commit()
        conn.close()
        display_table()
        update_graph()
        display_orders()
        update_graph_sale()
        configure_net_profit_label()


def configure_net_profit_label():
    net_profit_label.configure(text=f"Net Profit: ₹{calculate_net_profit()}")


def calculate_net_profit():
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(total_price) AS total_profit FROM orders')
    total_profit = cursor.fetchone()[0]
    conn.close()
    return total_profit


root = CTk()
root.title("Dashboard")
root.geometry()
font1 = ('Arial', 15, 'bold')
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

frame1 = CTkFrame(root, corner_radius=0, height=60, width=1300, fg_color='#002D62')
frame1.grid(row=0, column=0, sticky='nsew')
frame2 = CTkFrame(root, corner_radius=0, fg_color='#fff')
frame2.grid(row=1, column=0)

img = CTkImage(light_image=Image.open('dashboard.png'), dark_image=Image.open('dashboard.png'), size=(64, 64))
dashboard_img = CTkLabel(frame1, text='', image=img)
dashboard_img.place(x=20)
dasboard = CTkLabel(frame1, text='Dashboard', font=('Arial', 40, 'bold'), text_color='#fff')
dasboard.place(x=100, y=5)

quantity_label = CTkLabel(frame2, text="New Quantity:", font=font1)
quantity_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
quantity_entry = CTkEntry(frame2, width=200)
quantity_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

price_label = CTkLabel(frame2, text="New Price:", font=font1)
price_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
price_entry = CTkEntry(frame2, width=200)
price_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

update_button = CTkButton(frame2, text="Update Quantity and Price", command=update_quantity_and_price, fg_color='green', hover_color='#355E3B')
update_button.grid(row=0, column=2, rowspan=2, padx=5, pady=5)

style = ttk.Style(frame2)
style.theme_use('clam')
style.configure('Treeview.Heading', font=font1)

# Table of pizza quantity
tree = ttk.Treeview(frame2, columns=("ID", "Pizza Name", "Price", "Quantity"), show="headings", height=10)
for col in tree['columns']:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=150)

tree.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

delete_button = CTkButton(frame2, text="Delete Order", command=delete_order, fg_color='red', hover_color='#803333')
delete_button.grid(row=1, column=3, padx=5, pady=5)

Sales = CTkLabel(frame2, text='Sales', font=('Arial', 40, 'bold'))
Sales.grid(row=0, column=4, padx=5, pady=5)

net_profit_label = CTkLabel(frame2, text=f"Net Profit: ₹{calculate_net_profit()}", font=('Arial', 22, 'bold'))
net_profit_label.grid(row=1, column=5, padx=5, pady=5)

orders_tree = ttk.Treeview(frame2, columns=("ID", "Customer Name", "Margherita Pizza", "BBQ Pizza", "SeaFood Pizza", "Total Price"), show="headings")
for col in orders_tree['columns']:
    orders_tree.heading(col, text=col)
    orders_tree.column(col, anchor="center", width=120)

orders_tree.grid(row=2, column=3, columnspan=3, padx=5, pady=5, sticky='nsew')

display_table()
update_graph()
update_graph_sale()
display_orders()

root.mainloop()
