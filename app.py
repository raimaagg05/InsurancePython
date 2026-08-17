from flask import Flask, jsonify, request, render_template
from database import get_connection

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/customers", methods=["GET"])
def get_customers():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Customer")

        customers = cursor.fetchall()

        return jsonify(customers)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM Customer WHERE CustomerId = %s"
        cursor.execute(query, (customer_id,))

        customer = cursor.fetchone()

        if not customer:
            return jsonify({
                "error": "Customer not found"
            }), 404

        return jsonify(customer)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@app.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    connection = None
    cursor = None

    try:
        data = request.get_json()

        customer_name = data.get("CustomerName")
        email = data.get("Email")
        phone = data.get("Phone")
        address = data.get("Address")

        if not customer_name or not email:
            return jsonify({
                "error": "CustomerName and Email are required"
            }), 400

        connection = get_connection()
        cursor = connection.cursor()

        # Check customer exists
        cursor.execute(
            "SELECT CustomerId FROM Customer WHERE CustomerId = %s",
            (customer_id,)
        )

        if not cursor.fetchone():
            return jsonify({
                "error": "Customer not found"
            }), 404

        query = """
            UPDATE Customer
            SET CustomerName = %s,
                Email = %s,
                Phone = %s,
                Address = %s
            WHERE CustomerId = %s
        """

        values = (
            customer_name,
            email,
            phone,
            address,
            customer_id
        )

        cursor.execute(query, values)
        connection.commit()

        return jsonify({
            "message": "Customer updated successfully",
            "CustomerId": customer_id
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

@app.route("/customers", methods=["POST"])
def add_customer():
    connection = None
    cursor = None

    try:
        data = request.get_json()

        customer_name = data.get("CustomerName")
        email = data.get("Email")
        phone = data.get("Phone")
        address = data.get("Address")

        if not customer_name or not email:
            return jsonify({
                "error": "CustomerName and Email are required"
            }), 400

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO Customer
            (CustomerName, Email, Phone, Address)
            VALUES (%s, %s, %s, %s)
        """

        values = (
            customer_name,
            email,
            phone,
            address
        )

        cursor.execute(query, values)
        connection.commit()

        return jsonify({
            "message": "Customer added successfully",
            "CustomerId": cursor.lastrowid
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
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
            return jsonify({
                "error": "Customer not found"
            }), 404

        # Delete customer
        cursor.execute(
            "DELETE FROM Customer WHERE CustomerId = %s",
            (customer_id,)
        )

        connection.commit()

        return jsonify({
            "message": "Customer deleted successfully",
            "CustomerId": customer_id
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()            


@app.route("/policies", methods=["GET"])
def get_policies():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                p.PolicyId,
                p.PolicyNumber,
                p.CustomerId,
                c.CustomerName,
                p.PolicyType,
                p.PremiumAmount,
                p.CoverageAmount,
                p.EffectiveDate,
                p.ExpiryDate,
                p.Status
            FROM Policy p
            JOIN Customer c
                ON p.CustomerId = c.CustomerId
        """

        cursor.execute(query)
        policies = cursor.fetchall()

        return jsonify(policies)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@app.route("/policies", methods=["POST"])
def add_policy():
    connection = None
    cursor = None

    try:
        data = request.get_json()

        policy_number = data.get("PolicyNumber")
        customer_id = data.get("CustomerId")
        policy_type = data.get("PolicyType")
        premium_amount = data.get("PremiumAmount")
        coverage_amount = data.get("CoverageAmount")
        effective_date = data.get("EffectiveDate")
        expiry_date = data.get("ExpiryDate")
        status = data.get("Status")

        if not policy_number or not customer_id or not policy_type:
            return jsonify({
                "error": "PolicyNumber, CustomerId and PolicyType are required"
            }), 400

        connection = get_connection()
        cursor = connection.cursor()

        # Check customer exists
        cursor.execute(
            "SELECT CustomerId FROM Customer WHERE CustomerId = %s",
            (customer_id,)
        )

        if not cursor.fetchone():
            return jsonify({
                "error": "Customer not found"
            }), 404

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

        values = (
            policy_number,
            customer_id,
            policy_type,
            premium_amount,
            coverage_amount,
            effective_date,
            expiry_date,
            status
        )

        cursor.execute(query, values)
        connection.commit()

        return jsonify({
            "message": "Policy added successfully",
            "PolicyId": cursor.lastrowid
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@app.route("/policies/<int:policy_id>", methods=["GET"])
def get_policy(policy_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                p.PolicyId,
                p.PolicyNumber,
                p.CustomerId,
                c.CustomerName,
                p.PolicyType,
                p.PremiumAmount,
                p.CoverageAmount,
                p.EffectiveDate,
                p.ExpiryDate,
                p.Status
            FROM Policy p
            JOIN Customer c
                ON p.CustomerId = c.CustomerId
            WHERE p.PolicyId = %s
        """

        cursor.execute(query, (policy_id,))
        policy = cursor.fetchone()

        if not policy:
            return jsonify({
                "error": "Policy not found"
            }), 404

        return jsonify(policy)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@app.route("/policies/<int:policy_id>", methods=["PUT"])
def update_policy(policy_id):
    connection = None
    cursor = None

    try:
        data = request.get_json()

        policy_type = data.get("PolicyType")
        premium_amount = data.get("PremiumAmount")
        coverage_amount = data.get("CoverageAmount")
        effective_date = data.get("EffectiveDate")
        expiry_date = data.get("ExpiryDate")
        status = data.get("Status")

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT PolicyId FROM Policy WHERE PolicyId = %s",
            (policy_id,)
        )

        if not cursor.fetchone():
            return jsonify({
                "error": "Policy not found"
            }), 404

        query = """
            UPDATE Policy
            SET PolicyType = %s,
                PremiumAmount = %s,
                CoverageAmount = %s,
                EffectiveDate = %s,
                ExpiryDate = %s,
                Status = %s
            WHERE PolicyId = %s
        """

        values = (
            policy_type,
            premium_amount,
            coverage_amount,
            effective_date,
            expiry_date,
            status,
            policy_id
        )

        cursor.execute(query, values)
        connection.commit()

        return jsonify({
            "message": "Policy updated successfully",
            "PolicyId": policy_id
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@app.route("/policies/<int:policy_id>", methods=["DELETE"])
def delete_policy(policy_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Check policy exists
        cursor.execute(
            "SELECT PolicyId FROM Policy WHERE PolicyId = %s",
            (policy_id,)
        )

        if not cursor.fetchone():
            return jsonify({
                "error": "Policy not found"
            }), 404

        # Delete policy
        cursor.execute(
            "DELETE FROM Policy WHERE PolicyId = %s",
            (policy_id,)
        )

        connection.commit()

        return jsonify({
            "message": "Policy deleted successfully",
            "PolicyId": policy_id
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

if __name__ == "__main__":
    app.run(debug=True)