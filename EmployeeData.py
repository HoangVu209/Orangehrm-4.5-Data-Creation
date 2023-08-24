from faker import Faker
import mysql.connector
import csv 
# Create a Faker instance
fake = Faker()

# Establish a connection to your MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="orangehrm_mysql01"
)

# Create a cursor
cursor = db.cursor()

# Generate and insert multiple rows of fake data
num_rows = 2000  # Change this to the number of rows you want to generate
csv_data = []  # List to store CSV data
for _ in range(num_rows):
    employee_id = "E" + format(fake.unique.random_number(digits=4), '04d')
    emp_lastname = fake.last_name()
    emp_firstname = fake.first_name()
    emp_middle_name = fake.first_name_male()
    emp_nick_name = fake.first_name()
    emp_marital_status = fake.random_element(elements=("Single", "Married", "Divorced"))
    # ... continue generating values for other columns

    # Define the SQL query
    sql = """
    INSERT INTO hs_hr_employee (
    employee_id, emp_lastname, emp_firstname, emp_middle_name, emp_nick_name, emp_marital_status
    ) VALUES (
        %s, %s, %s, %s, %s, %s
    )
    """
    # Execute the query
    values = (
        employee_id, emp_lastname, emp_firstname, emp_middle_name, emp_nick_name, emp_marital_status
    )
    try:
        cursor.execute(sql, values)
        db.commit()  # Commit the changes
        # Append data to CSV list
        csv_data.append([emp_firstname + ' ' + emp_lastname, employee_id])

    except mysql.connector.Error as err:
        db.rollback()  # Rollback the transaction in case of error
        print("Insert failed for employee_id:", employee_id)
        print("Error:", err)

# Close the cursor and connection
cursor.close()
db.close()
# Save CSV data to a file
csv_filename = "search_list.csv"
with open(csv_filename, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['full_name', 'employee_id'])
    csv_writer.writerows(csv_data)

print("Insert successful " + num_rows + " employees")