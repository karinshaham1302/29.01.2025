import functions


def main():
    # Example calls to the functions:
    functions.setup_database()  # Set up the database, create table, and insert data
    functions.add_car_to_garage('your_db_name.db')  # Add car to the garage
    functions.update_car_status('your_db_name.db')  # Update car repair status
    functions.delete_car_from_garage('your_db_name.db')  # Delete car from the garage
    functions.show_cars_waiting_for_repair('your_db_name.db')  # Display cars waiting for
    # repair


if __name__ == "__main__":
    main()
