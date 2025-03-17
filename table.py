import mysql.connector as mc

conn = mc.connect(user='root', password='ayush@#11', host='localhost', database='credit_p')

if conn.is_connected():
    print("You are connected.")
else:
    print('Unable to connect.')

mycursor = conn.cursor()

query = """CREATE TABLE data(
    income DECIMAL(10, 2),
    credit_limit DECIMAL(10, 2),  
    cards INT,
    age INT,
    education VARCHAR(50),
    gender VARCHAR(10),
    student BOOLEAN,
    married BOOLEAN,
    ethnicity VARCHAR(50),
    predicted INT
)
"""


mycursor.execute(query)
print('Your table is created.')

mycursor.close()
conn.close()
