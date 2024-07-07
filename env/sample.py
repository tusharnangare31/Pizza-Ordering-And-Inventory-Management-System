import mysql.connector

# MySQL connection configuration
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 't1121tdn',
    'database': 'college',
}

# Establishing connection
conn = mysql.connector.connect(**mysql_config)

# Creating a cursor object to execute SQL queries
cursor = conn.cursor()

# Example query: fetching all records from a table
query = "SELECT * FROM student"

# Executing the query
cursor.execute(query)

# Fetching all the results
results = cursor.fetchall()

# Printing the results
for row in results:
    print(row)

# Closing cursor and connection
cursor.close()
conn.close()
