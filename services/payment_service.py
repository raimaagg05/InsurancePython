import razorpay

from config import Config
from database import get_connection


client = razorpay.Client(
    auth=(
        Config.RAZORPAY_KEY_ID,
        Config.RAZORPAY_KEY_SECRET
    )
)


def create_payment_order(
    policy_id,
    customer_id,
    amount
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

        # Razorpay expects amount in paise
        amount_paise = int(float(amount) * 100)

        razorpay_order = client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "receipt": f"policy_{policy_id}",
            "notes": {
                "policy_id": str(policy_id),
                "customer_id": str(customer_id)
            }
        })

        query = """
            INSERT INTO Payment
            (
                PolicyId,
                CustomerId,
                Amount,
                RazorpayOrderId,
                Status
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                policy_id,
                customer_id,
                amount,
                razorpay_order["id"],
                "Created"
            )
        )

        connection.commit()

        return {
            "payment_id": cursor.lastrowid,
            "order_id": razorpay_order["id"],
            "amount": amount,
            "currency": "INR"
        }, None

    except Exception:
        if connection:
            connection.rollback()

        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

def verify_payment(
    razorpay_order_id,
    razorpay_payment_id,
    razorpay_signature
):
    connection = None
    cursor = None

    try:
        # Verify Razorpay signature
        client.utility.verify_payment_signature({
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
        })

        connection = get_connection()
        cursor = connection.cursor()

        # Find payment record
        cursor.execute(
            """
            SELECT PaymentId
            FROM Payment
            WHERE RazorpayOrderId = %s
            """,
            (razorpay_order_id,)
        )

        payment = cursor.fetchone()

        if not payment:
            return False, "Payment order not found"

        # Mark payment as paid
        cursor.execute(
            """
            UPDATE Payment
            SET
                RazorpayPaymentId = %s,
                Status = 'Paid'
            WHERE RazorpayOrderId = %s
            """,
            (
                razorpay_payment_id,
                razorpay_order_id
            )
        )

        connection.commit()

        return True, None

    except razorpay.errors.SignatureVerificationError:
        return False, "Payment signature verification failed"

    except Exception:
        if connection:
            connection.rollback()

        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()