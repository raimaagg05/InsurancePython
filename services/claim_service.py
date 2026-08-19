from database import get_connection


def create_claim(
    policy_id,
    customer_id,
    claim_amount,
    claim_reason
):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Check policy
        cursor.execute(
            """
            SELECT PolicyId
            FROM Policy
            WHERE PolicyId = %s
            """,
            (policy_id,)
        )

        if not cursor.fetchone():
            return None, "Policy not found"

        # Check customer
        cursor.execute(
            """
            SELECT CustomerId
            FROM Customer
            WHERE CustomerId = %s
            """,
            (customer_id,)
        )

        if not cursor.fetchone():
            return None, "Customer not found"

        query = """
            INSERT INTO Claim
            (PolicyId, CustomerId, ClaimAmount, ClaimReason)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                policy_id,
                customer_id,
                claim_amount,
                claim_reason
            )
        )

        connection.commit()

        return cursor.lastrowid, None

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

def get_all_claims():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                cl.ClaimId,
                cl.PolicyId,
                cl.CustomerId,
                c.CustomerName,
                cl.ClaimAmount,
                cl.ClaimReason,
                cl.ClaimDate,
                cl.Status
            FROM Claim cl
            JOIN Customer c
                ON cl.CustomerId = c.CustomerId
            ORDER BY cl.ClaimDate DESC
        """

        cursor.execute(query)

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

def update_claim_status(claim_id, status):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT ClaimId, Status
            FROM Claim
            WHERE ClaimId = %s
            """,
            (claim_id,)
        )

        claim = cursor.fetchone()

        if not claim:
            return False, "Claim not found"

        if status not in ["Approved", "Rejected"]:
            return False, "Invalid claim status"

        if claim[1] != "Pending":
            return False, "Only pending claims can be approved or rejected"

        cursor.execute(
            """
            UPDATE Claim
            SET Status = %s
            WHERE ClaimId = %s
            """,
            (status, claim_id)
        )

        connection.commit()

        return True, None

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

def get_customer_claims(customer_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                cl.ClaimId,
                cl.PolicyId,
                cl.CustomerId,
                c.CustomerName,
                cl.ClaimAmount,
                cl.ClaimReason,
                cl.ClaimDate,
                cl.Status
            FROM Claim cl
            JOIN Customer c
                ON cl.CustomerId = c.CustomerId
            WHERE cl.CustomerId = %s
            ORDER BY cl.ClaimDate DESC
        """

        cursor.execute(query, (customer_id,))

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()