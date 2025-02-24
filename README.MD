# 🍕 Inventory Management System

Welcome to the Inventory Management System for managing pizza inventory and orders efficiently.

## 📑 Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Database Setup](#database-setup)
- [Running the Project](#running-the-project)
- [Usage](#usage)
  - [Adding a New Pizza](#adding-a-new-pizza)
  - [Placing an Order](#placing-an-order)
  - [Viewing Inventory](#viewing-inventory)
  - [Viewing Orders](#viewing-orders)
- [License](#license)

## 📖 Project Overview

This project is an Inventory Management System designed to help manage pizza inventory and customer orders. It includes features for adding new pizzas, placing orders, and viewing current inventory and orders.

## 📁 Project Structure

```
.
├── .gitignore
├── 1.jpg
├── 2.jpg
├── 3.jpg
├── dashboard.ico
├── dashboard.png
├── env/
│   ├── bin/
│   ├── include/
│   ├── lib/
│   └── pyvenv.cfg
├── graph.py
├── main.py
├── order.txt
├── Pizza.sql
├── README.md
├── requirements.txt
├── sample.py
├── share/
│   └── man/
│       └── man1/
├── tempCodeRunnerFile.py
└── title.jpg
```

## 📋 Requirements

To install the required dependencies, run:

```sh
pip install -r requirements.txt
```

## 🗄️ Database Setup

To set up the database, run the SQL script in Pizza.sql:

```sql
CREATE DATABASE Pizza;

USE Pizza;

CREATE TABLE pizza(
    id INT PRIMARY KEY,
    pizza_name VARCHAR(20),
    price INT,
    quantity INT
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(20),
    Margherita_Pizza INT,
    BBQ_Pizza INT,
    SeaFood_Pizza INT,
    total_price INT
);

INSERT INTO pizza (id, pizza_name, price, quantity) VALUES
(1, 'Margherita Pizza', 200, 5),
(2, 'BBQ Pizza', 250, 4),
(3, 'SeaFood Pizza', 300, 6);

INSERT INTO orders (id, customer_name, Margherita_Pizza, BBQ_Pizza, SeaFood_Pizza, total_price) VALUES
(1, 'John', 2, 3, 1, (2 * 200) + (3 * 250) + (1 * 300)),
(2, 'Alice', 1, 2, 2, (1 * 200) + (2 * 250) + (2 * 300)),
(3, 'Bob', 3, 1, 1, (3 * 200) + (1 * 250) + (1 * 300));
```

## 🚀 Running the Project

To run the project, execute the `main.py` file:

```sh
python main.py
```

## 🛠️ Usage

### ➕ Adding a New Pizza

To add a new pizza to the inventory, modify the Pizza.sql file and insert a new row into the `pizza` table:

```sql
INSERT INTO pizza (id, pizza_name, price, quantity) VALUES
(4, 'New Pizza', 350, 10);
```

### 🛒 Placing an Order

To place an order, modify the `orders` table in the Pizza.sql file and insert a new row with the customer's order details:

```sql
INSERT INTO orders (customer_name, Margherita_Pizza, BBQ_Pizza, SeaFood_Pizza, total_price) VALUES
('Customer Name', 1, 2, 1, (1 * 200) + (2 * 250) + (1 * 300));
```

### 📦 Viewing Inventory

To view the current inventory, query the `pizza` table:

```sql
SELECT * FROM pizza;
```

### 📋 Viewing Orders

To view all orders, query the `orders` table:

```sql
SELECT * FROM orders;
```

## 📜 License

This project is licensed under the MIT License.
```

This version includes emojis for better visual appeal and a more structured layout. You can further customize it based on your project's specific details and requirements.
This version includes emojis for better visual appeal and a more structured layout. You can further customize it based on your project's specific details and requirements.
