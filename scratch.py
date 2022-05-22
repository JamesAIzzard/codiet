import sqlite3

con = None
try:
    # Connect to the database
    con = sqlite3.connect('test_database.db')
    cur = con.cursor()
    # Execute a query that will pass
    cur.execute("""INSERT INTO contacts (
        first_name, last_name, email, phone
    ) VALUES (
        'Barry', 'Bobson', 'bb@gmail.com', '987654321'
    );
    """)
    # Execute a query that will fail (email unique field collision)
    cur.execute("""INSERT INTO contacts (
        first_name, last_name, email, phone
    ) VALUES (
        'Jane', 'Johnson', 'jane@doe.com', '12345678910'
    );
    """)
    con.commit()

except sqlite3.Error as e:
    if con is not None:
        con.rollback()
    
    print(e)

finally:
    if con is not None:
        con.close()