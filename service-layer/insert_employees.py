import csv
import psycopg2
from psycopg2 import sql

# Database connection parameters (for local Docker Postgres)
DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'

# CSV file path (update as needed)
CSV_FILE = 'employees.csv'

def insert_employees_from_csv():
    """Read CSV and insert employees into database, committing one at a time."""
    conn = None
    try:
        # Connect to database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()
        
        # Insert query
        insert_query = sql.SQL("""
            INSERT INTO test_schema.employee (firstname, lastname, email, age, salary)
            VALUES (%s, %s, %s, %s, %s)
        """)
        
        inserted_count = 0
        skipped_count = 0
        with open(CSV_FILE, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)  # Assumes header row: firstname,lastname,email,age,salary
            for row in reader:
                try:
                    cur.execute(insert_query, (
                        row['firstname'],
                        row['lastname'],
                        row['email'],
                        int(row['age']),  # Ensure int
                        float(row['salary'])  # Ensure float
                    ))
                    conn.commit()  # Commit after each insert
                    inserted_count += 1
                    print(f"Inserted: {row['firstname']} {row['lastname']}")
                except Exception as row_error:
                    print(f"Error inserting row {row}: {row_error}")
                    if conn:
                        conn.rollback()  # Rollback this row only
                    skipped_count += 1
        
        print(f"Successfully inserted {inserted_count} employees from {CSV_FILE}. Skipped {skipped_count} due to errors.")
        
    except FileNotFoundError:
        print(f"Error: CSV file '{CSV_FILE}' not found. Create it with headers: firstname,lastname,email,age,salary")
    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    insert_employees_from_csv()