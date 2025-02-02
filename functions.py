import sqlite3


def connect_db(my_db_name):
    """
    Connects to the SQLite database and returns the cursor and connection.
    :param my_db_name: The name of the database file.
    :return: A tuple containing the connection and cursor.
    """
    my_conn = sqlite3.connect('29_01_2025.db')
    my_conn.row_factory = sqlite3.Row  # To access columns by name
    my_cursor = my_conn.cursor()
    return my_conn, my_cursor


def execute_query(my_cursor, my_conn, query, params) -> None:
    """
    Executes a modify query (INSERT, UPDATE, DELETE).
    :param my_cursor: sqlite cursor
    :param my_conn:  sqlite connection
    :param query: SQL string query
    :param params: Parameters to be passed into the query
    :return: None
    """
    my_cursor.execute(query, params)
    my_conn.commit()


def print_color(message, color="red"):
    """
    Prints the message in the specified color (red or blue).
    :param message: The message to print.
    :param color: The color for printing. Default is "red".
    :return: None
    """
    match color:
        case "red":
            COLOR = '\033[31m'
            RESET = '\033[0m'
        case "blue":
            COLOR = '\033[34m'
            RESET = '\033[0m'
        case _:
            COLOR = '\033[31m'
            RESET = '\033[0m'
    print(f"{COLOR}{message}{RESET}")


def read_query(my_cursor, query):
    """
    Executes a SELECT query and returns the results in various formats (tuple, list, dictionary).
    :param my_cursor: sqlite cursor
    :param query: The SQL query to be executed (SELECT).
    :return: A list of tuples representing the result rows.
    """
    my_cursor.execute(query)
    rows = my_cursor.fetchall()
    result_list = [list(row) for row in rows]
    result_dict = [dict(row) for row in rows]
    result_tuple = [tuple(row) for row in rows]
    return result_tuple


def update_query(my_cursor, my_conn, query, param):
    """
    Executes an UPDATE query.
    :param my_cursor: sqlite cursor
    :param my_conn: sqlite connection
    :param query: SQL string query
    :param param: Parameters to be passed into the query
    :return: None
    """
    my_cursor.execute(query, param)
    my_conn.commit()


def setup_database():
    # Connect to the database
    conn, cursor = connect_db('29_01_2025.db')  # Replace 'garage.db' with your actual DB file name

    # Create the table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS garage (
        fix_id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_number TEXT UNIQUE NOT NULL,
        car_problem TEXT NOT NULL,
        fixed BOOLEAN DEFAULT FALSE,
        owner_ph TEXT NOT NULL
    );
    """
    execute_query(cursor, conn, create_table_query, ())
    conn.commit()

    # Remove all existing records from the table (optional)
    execute_query(cursor, conn, "DELETE FROM garage", ())

    # Insert the data into the garage table
    insert_queries = [
        ("23", "Engine overheating after long drives", True, "555-1023"),
        ("34", "Brake pads worn out, needs replacement", True, "555-1034"),
        ("30", "Check engine light on, possible sensor issue", True, "555-1030"),
        ("24", "Battery drains overnight, needs diagnosis", False, "555-1024"),
        ("3", "Strange noise from suspension when turning", False, "555-1003")
    ]

    for car in insert_queries:
        insert_query = """
        INSERT INTO garage (car_number, car_problem, fixed, owner_ph)
        VALUES (?, ?, ?, ?)
        """
        try:
            execute_query(cursor, conn, insert_query, car)
        except sqlite3.IntegrityError:
            print(f"Car with number {car[0]} already exists.")

    print_color("Table and data setup complete.", "blue")
    conn.commit()


def add_car_to_garage(my_db_name):
    """
    Adds a car to the garage table in the database.
    :param my_db_name: The name of the SQLite database file.
    :return: None
    """
    car_number = input("Enter car license plate number: ")
    car_problem = input("Enter car problem: ")
    owner_ph = input("Enter car owner's phone number: ")

    # INSERT query to add the car to the garage table
    query = """
    INSERT INTO garage (car_number, car_problem, fixed, owner_ph)
    VALUES (?, ?, 0, ?)
    """
    params = (car_number, car_problem, owner_ph)

    # Connect to the database
    conn, cursor = connect_db(my_db_name)

    try:
        # Execute the query
        execute_query(cursor, conn, query, params)
        print_color("The car has been successfully added to the garage.", color="blue")
    except Exception as e:
        print_color(f"Error adding the car: {e}", color="red")
    finally:
        # Close the database connection
        conn.close()


def update_car_status(my_db_name):
    """
    Checks the repair status of a car and updates it if the repair is complete.
    :param my_db_name: The name of the SQLite database file.
    :return: None
    """
    car_number = input("Enter car license plate number: ")

    # SELECT query to check if the car exists and get its status
    query_select = "SELECT fixed, owner_ph FROM garage WHERE car_number = ?"
    params_select = (car_number,)

    # Connect to the database
    conn, cursor = connect_db(my_db_name)

    try:
        # Check if the car exists
        cursor.execute(query_select, params_select)
        result = cursor.fetchone()

        if result is None:
            print_color("The car is not in the garage.", color="red")
        else:
            if result['fixed'] == 0:
                print_color("The repair for this car is not yet completed.", color="red")
            else:
                print_color(f"Please contact the car owner at: {result['owner_ph']}", color="blue")
                # UPDATE query to change the fixed status to 1 (repair completed)
                query_update = "UPDATE garage SET fixed = 1 WHERE car_number = ?"
                execute_query(cursor, conn, query_update, params_select)
                print_color("The car repair status has been updated.", color="blue")
    except Exception as e:
        print_color(f"Error: {e}", color="red")
    finally:
        # Close the database connection
        conn.close()


def delete_car_from_garage(my_db_name):
    """
    Deletes a car record from the garage table after verifying its status.
    :param my_db_name: The name of the SQLite database file.
    :return: None
    """
    car_number = input("Enter car license plate number: ")

    # SELECT query to check if the car exists and get its status
    query_select = "SELECT fixed, owner_ph FROM garage WHERE car_number = ?"
    params_select = (car_number,)

    # Connect to the database
    conn, cursor = connect_db(my_db_name)

    try:
        # Check if the car exists
        cursor.execute(query_select, params_select)
        result = cursor.fetchone()

        if result is None:
            print_color("The car is not in the garage.", color="red")
        else:
            if result['fixed'] == 0:
                print_color("The repair for this car is not yet completed.", color="red")
            else:
                print_color(f"Please contact the car owner at: {result['owner_ph']}", color="blue")
                # DELETE query to remove the car record
                query_delete = "DELETE FROM garage WHERE car_number = ?"
                execute_query(cursor, conn, query_delete, params_select)
                print_color("The car has been successfully removed from the garage.", color="blue")

    except Exception as e:
        print_color(f"Error: {e}", color="red")
    finally:
        # Close the database connection
        conn.close()


def show_cars_waiting_for_repair(my_db_name):
    """
    This function queries the garage database to find cars that are waiting for repair
    (those with a fixed status of 0) and displays their car numbers and problems.
    It also handles any exceptions and displays messages in color.

    :param my_db_name: The name of the SQLite database file.
    :return: None
    """

    # Define the SELECT query to get cars that are waiting for repair (fixed = 0)
    query = "SELECT car_number, car_problem FROM garage WHERE fixed = 0"

    # Connect to the database
    conn, cursor = connect_db(my_db_name)

    try:
        # Execute the SELECT query
        result = read_query(cursor, query)

        if result:  # If there are cars waiting for repair
            print_color(f"There are {len(result)} cars waiting for repair:", color="blue")
            for car in result:
                print(f"Car Number: {car[0]}, Problem: {car[1]}")
        else:  # No cars waiting for repair
            print_color("No cars are currently waiting for repair.", color="blue")

    except Exception as e:
        # In case of any error, print the error message in red
        print_color(f"Error: {e}", color="red")
    finally:
        # Close the database connection
        conn.close()
