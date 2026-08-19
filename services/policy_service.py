from database import get_connection


def get_all_policies():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                p.*,
                c.CustomerName
            FROM Policy p
            JOIN Customer c
                ON p.CustomerId = c.CustomerId
        """

        cursor.execute(query)

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def create_policy(
    policy_number,
    customer_id,
    policy_type,
    premium_amount,
    coverage_amount,
    effective_date,
    expiry_date,
    status
):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Check customer exists
        cursor.execute(
            "SELECT CustomerId FROM Customer WHERE CustomerId = %s",
            (customer_id,)
        )

        if not cursor.fetchone():
            return None

        query = """
            INSERT INTO Policy
            (
                PolicyNumber,
                CustomerId,
                PolicyType,
                PremiumAmount,
                CoverageAmount,
                EffectiveDate,
                ExpiryDate,
                Status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                policy_number,
                customer_id,
                policy_type,
                premium_amount,
                coverage_amount,
                effective_date,
                expiry_date,
                status
            )
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

def get_policy_by_id(policy_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                p.*,
                c.CustomerName
            FROM Policy p
            JOIN Customer c
                ON p.CustomerId = c.CustomerId
            WHERE p.PolicyId = %s
        """

        cursor.execute(query, (policy_id,))

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def update_policy(
    policy_id,
    policy_number,
    customer_id,
    policy_type,
    premium_amount,
    coverage_amount,
    effective_date,
    expiry_date,
    status
):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT PolicyId FROM Policy WHERE PolicyId = %s",
            (policy_id,)
        )

        if not cursor.fetchone():
            return False

        cursor.execute(
            "SELECT CustomerId FROM Customer WHERE CustomerId = %s",
            (customer_id,)
        )

        if not cursor.fetchone():
            return None

        query = """
            UPDATE Policy
            SET
                PolicyNumber = %s,
                CustomerId = %s,
                PolicyType = %s,
                PremiumAmount = %s,
                CoverageAmount = %s,
                EffectiveDate = %s,
                ExpiryDate = %s,
                Status = %s
            WHERE PolicyId = %s
        """

        cursor.execute(
            query,
            (
                policy_number,
                customer_id,
                policy_type,
                premium_amount,
                coverage_amount,
                effective_date,
                expiry_date,
                status,
                policy_id
            )
        )

        connection.commit()

        return True

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def delete_policy(policy_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT PolicyId FROM Policy WHERE PolicyId = %s",
            (policy_id,)
        )

        if not cursor.fetchone():
            return False

        cursor.execute(
            "DELETE FROM Policy WHERE PolicyId = %s",
            (policy_id,)
        )

        connection.commit()

        return True

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()