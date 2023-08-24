import random
from mimesis import Generic
import mysql.connector

# Create a Generic instance
fake = Generic()

# Establish a connection to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="orangehrm_mysql01"  
)

# Create a cursor
cursor = db.cursor()

# Generate and insert multiple rows of fake data
num_rows = 20  # Change this to the number of rows you want to generate
generated_names = set()  # To keep track of generated names

for _ in range(num_rows):
    name = None
    while name is None or name in generated_names:
        name = fake.text.word() + " Department"
    generated_names.add(name)

    unit_id = fake.random.randint(1000, 9999)
    description = fake.text.sentence()  # Use sentence method for random phrases
    lft = fake.random.randint(1, 100)
    rgt = lft + 1
    level = fake.random.randint(1, 5)

    try:
        # Define the SQL query
        sql = """
        INSERT INTO ohrm_subunit (name, unit_id, description, lft, rgt, level)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        # Execute the query
        values = (name, unit_id, description, lft, rgt, level)
        cursor.execute(sql, values)
        db.commit()

        print("Insert successful for subunit:", name)
    except mysql.connector.Error as err:
        db.rollback()  # Rollback the transaction in case of error
        print("Insert failed for subunit:", name)
        print("Error:", err)

# Close the cursor and connection
cursor.close()
db.close()
