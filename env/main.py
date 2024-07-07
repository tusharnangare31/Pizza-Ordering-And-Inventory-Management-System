import customtkinter 
from customtkinter import *
from tkinter import *
import mysql.connector
from PIL import Image
from tkinter import messagebox

# MySQL connection configuration
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 't1121tdn',
    'database': 'Pizza'
}

def get_pizza():
    conn = mysql.connector.connect(**mysql_config)
    c = conn.cursor()
    c.execute('SELECT pizza_name , price FROM pizza')
    results = c.fetchall()
    print(results)

    global pizza1_details
    global pizza2_details
    global pizza3_details

    pizza1_details = results[0]
    pizza2_details = results[1]
    pizza3_details = results[2]

    p1_text.configure(text='{}\nPrice: ₹{}'.format(pizza1_details[0],pizza1_details[1]))
    p2_text.configure(text='{}\nPrice: ₹{}'.format(pizza2_details[0],pizza2_details[1]))
    p3_text.configure(text='{}\nPrice: ₹{}'.format(pizza3_details[0],pizza3_details[1]))

def get_quantity():
    conn = mysql.connector.connect(**mysql_config)
    c = conn.cursor()
    c.execute('SELECT quantity FROM pizza')
    results = c.fetchall()
    print(results)
    global pizza1_quantity
    global pizza2_quantity
    global pizza3_quantity

    pizza1_quantity = results[0][0]
    pizza2_quantity = results[1][0]
    pizza3_quantity = results[2][0]

    if pizza1_quantity == 0:
        variable1.set('0')
        p1_quantity.destroy()
        p1_state_label = CTkLabel(p1_frame, font=font1, text='Sold Out', text_color='#f00', bg_color='#000', width=100)
        p1_state_label.place(x=40, y=270)
    else:
        list1 = [str(i) for i in range(pizza1_quantity + 1)]
        p1_quantity.configure(values=list1)
        p1_quantity.set('0')

    if pizza2_quantity == 0:
        variable2.set('0')
        p2_quantity.destroy()
        p2_state_label = CTkLabel(p2_frame, font=font1, text='Sold Out', text_color='#f00', bg_color='#000', width=100)
        p2_state_label.place(x=40, y=270)
    else:
        list2 = [str(i) for i in range(pizza2_quantity + 1)]
        p2_quantity.configure(values=list2)
        p2_quantity.set('0')

    if pizza3_quantity == 0:
        variable3.set('0')
        p3_quantity.destroy()
        p3_state_label = CTkLabel(p3_frame, font=font1, text='Sold Out', text_color='#f00', bg_color='#000', width=100)
        p3_state_label.place(x=40, y=270)
    else:
        list3 = [str(i) for i in range(pizza3_quantity + 1)]
        p3_quantity.configure(values=list3)
        p3_quantity.set('0')

def checkout():
    if pizza1_quantity == 0 and pizza2_quantity == 0 and pizza3_quantity == 0:
        messagebox.showerror("Error", "Cannot serve you now.")
    else:
        if customer_entry.get():
            conn = mysql.connector.connect(**mysql_config)
            c = conn.cursor()
            quantity1 = int(variable1.get())
            quantity2 = int(variable2.get())
            quantity3 = int(variable3.get())
            c.execute('UPDATE pizza SET quantity = %s WHERE pizza_name = %s', (pizza1_quantity - quantity1, 'Margherita Pizza'))
            c.execute('UPDATE pizza SET quantity = %s WHERE pizza_name = %s', (pizza2_quantity - quantity2, 'BBQ Pizza'))
            c.execute('UPDATE pizza SET quantity = %s WHERE pizza_name = %s', (pizza3_quantity - quantity3, 'SeaFood Pizza'))  
            conn.commit()
            conn.close()
            total_price = quantity1 * pizza1_details[1] + quantity2 * pizza2_details[1] + quantity3 * pizza3_details[1]
            if total_price == 0:
                messagebox.showerror('Error', 'Choose a pizza.')
            else:
                price_label.configure(text=f'Price: ₹{total_price}')
                get_quantity()
                # Record order details in the database
                conn = mysql.connector.connect(**mysql_config)
                c = conn.cursor()
                c.execute('INSERT INTO orders ( id,customer_name, Margherita_Pizza, BBQ_Pizza, SeaFood_Pizza, total_price) VALUES (%s,%s, %s, %s, %s, %s)',
                          (get_last_id()+1,customer_entry.get(), quantity1, quantity2, quantity3, total_price))
                conn.commit()
                conn.close()
                with open('order.txt', 'a') as f:
                    f.write(f'Name: {customer_entry.get()}\n')
                    f.write(f'Total Price: {total_price}\n')
                    f.write('--------------------------\n')
        else:
            messagebox.showerror('Error', 'Enter Customer Name.')
        
def get_last_id():
    conn = mysql.connector.connect(**mysql_config)
    c = conn.cursor()
    c.execute('SELECT max(id) FROM orders')
    last_id = c.fetchone()[0]
    conn.close()
    return last_id if last_id is not None else 0

app = CTk()
app.title('Pizza Shop')
app.geometry('700x700')
app.resizable(0,0)
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")
app.config(bg='#000')
font1 = ('Arial',22,'bold')

variable1 = StringVar()
variable2 = StringVar()
variable3 = StringVar()

frame1 = CTkFrame(app,bg_color='#000',fg_color='#0E0F0F',width =700,height=265)
frame1.place(x=0,y=0)

frame2 = CTkFrame(app,bg_color='#000',fg_color='#0E0F0F',width=700,height=440)
frame2.place(x=0,y=265)

img1 = CTkImage(light_image=Image.open('title.jpg'),dark_image=Image.open('title.jpg'),size=(700,265))
Lab_img_1 = CTkLabel(frame1,image=img1,text="")
Lab_img_1.pack() 

p1_frame = CTkFrame(frame2,bg_color='#fff',corner_radius=0,width=196,height=320)
p1_frame.place(x=20,y=20)

p1_img = CTkImage(light_image=Image.open('1.jpg'),dark_image=Image.open('1.jpg'),size=(196,196))
p1_lable = CTkLabel(p1_frame,image=p1_img,text="")
p1_lable.place(x = 0, y = 0)

p1_text = CTkLabel(p1_frame,text="Margherita Pizza\nPrice ₹20",font=font1)
p1_text.place(x=10,y = 200)

p1_quantity = CTkComboBox(p1_frame,text_color='#000',fg_color='#fff',dropdown_hover_color='#06911f',button_color='#F67A0D',button_hover_color='#be4d25',variable=variable1,width=120)
p1_quantity.set('0')
p1_quantity.place(x=40, y=270)

p2_frame = CTkFrame(frame2,bg_color='#fff',corner_radius=0,width=196,height=320)
p2_frame.place(x=250,y=20)

p2_img = CTkImage(light_image=Image.open('2.jpg'),dark_image=Image.open('2.jpg'),size=(196,196))
p2_lable = CTkLabel(p2_frame,image=p2_img,text="")
p2_lable.place(x = 0, y = 0)

p2_text = CTkLabel(p2_frame,text="BBQ Pizza\nPrice ₹25",font=font1)
p2_text.place(x=40,y = 200)

p2_quantity = CTkComboBox(p2_frame,text_color='#000',fg_color='#fff',dropdown_hover_color='#06911f',button_color='#F67A0D',button_hover_color='#be4d25',variable=variable2,width=120)
p2_quantity.set('0')
p2_quantity.place(x=40, y=270)

p3_frame = CTkFrame(frame2,bg_color='#fff',corner_radius=0,width=196,height=320)
p3_frame.place(x=480,y=20)

p3_img = CTkImage(light_image=Image.open('3.jpg'),dark_image=Image.open('3.jpg'),size=(196,196))
p3_lable = CTkLabel(p3_frame,image=p3_img,text="")
p3_lable.place(x = 0, y = 0)

p3_text = CTkLabel(p3_frame,text="Seafood Pizza\nPrice ₹35",font=font1)
p3_text.place(x=20,y = 200)

p3_quantity = CTkComboBox(p3_frame,text_color='#000',fg_color='#fff',dropdown_hover_color='#06911f',button_color='#F67A0D',button_hover_color='#be4d25',variable=variable3,width=120)
p3_quantity.set('0')
p3_quantity.place(x=40, y=270)

customer_lable = CTkLabel(frame2,text='Customer :',font=font1,bg_color='#000',fg_color='#000',text_color='#fff')
customer_lable.place(x=50,y=370)

customer_entry = CTkEntry(frame2,font=font1,text_color='#000',fg_color='#fff')
customer_entry.place(x=170,y=370)

checkout_button = CTkButton(frame2,font=font1,text_color='#fff',command=checkout,text='checkout',fg_color='#410AE3',hover_color='#3303C0',bg_color='#000',cursor='hand2',corner_radius=30,width=160,height=40)
checkout_button.place(x=350,y=365)

price_label = CTkLabel(frame2,text='',text_color='#0f0',bg_color='#0E0F0F',font=font1)
price_label.place(x=550,y=370)

get_pizza()
get_quantity()
app.mainloop()
