from database import get_connection


def get_all_customers():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Customer")

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def create_customer(customer_name, email, phone, address):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO Customer
            (CustomerName, Email, Phone, Address)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (customer_name, email, phone, address)
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

def get_customer_by_id(customer_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM Customer WHERE CustomerId = %s",
            (customer_id,)
        )

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def update_customer(
    customer_id,
    customer_name,
    email,
    phone,
    address
):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT CustomerId FROM Customer WHERE CustomerId = %s",
            (customer_id,)
        )

        if not cursor.fetchone():
            return False

        query = """
            UPDATE Customer
            SET
                CustomerName = %s,
                Email = %s,
                Phone = %s,
                Address = %s
            WHERE CustomerId = %s
        """

        cursor.execute(
            query,
            (
                customer_name,
                email,
                phone,
                address,
                customer_id
            )
        )

        connection.commit()

        return True

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def delete_customer(customer_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT CustomerId FROM Customer WHERE CustomerId = %s",
            (customer_id,)
        )

        if not cursor.fetchone():
            return False

        cursor.execute(
            "DELETE FROM Customer WHERE CustomerId = %s",
            (customer_id,)
        )

        connection.commit()

        return True

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()