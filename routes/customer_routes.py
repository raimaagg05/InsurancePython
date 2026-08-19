from flask import Blueprint, jsonify, request
from services.customer_service import (
    get_all_customers,
    create_customer,
    get_customer_by_id,
    update_customer,
    delete_customer
)
from middleware.auth_middleware import token_required, role_required

customer_bp = Blueprint("customer", __name__)


@customer_bp.route("/customers", methods=["GET"])
@token_required
@role_required("Admin", "Agent")
def get_customers():
    try:
        customers = get_all_customers()
        return jsonify(customers)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@customer_bp.route("/customers", methods=["POST"])
@token_required
@role_required("Admin", "Agent")
def add_customer():
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

        customer_id = create_customer(
            customer_name,
            email,
            phone,
            address
        )

        return jsonify({
            "message": "Customer added successfully",
            "CustomerId": customer_id
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@customer_bp.route("/customers/<int:customer_id>", methods=["GET"])
@token_required
@role_required("Admin", "Agent")
def get_customer(customer_id):
    try:
        customer = get_customer_by_id(customer_id)

        if not customer:
            return jsonify({
                "error": "Customer not found"
            }), 404

        return jsonify(customer)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@customer_bp.route("/customers/<int:customer_id>", methods=["PUT"])
@token_required
@role_required("Admin", "Agent")
def update_customer_route(customer_id):
    try:
        data = request.get_json()

        required_fields = [
            "CustomerName",
            "Email",
            "Phone",
            "Address"
        ]

        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": f"{field} is required"
                }), 400

        result = update_customer(
            customer_id,
            data["CustomerName"],
            data["Email"],
            data["Phone"],
            data["Address"]
        )

        if not result:
            return jsonify({
                "error": "Customer not found"
            }), 404

        return jsonify({
            "message": "Customer updated successfully"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@customer_bp.route("/customers/<int:customer_id>", methods=["DELETE"])
@token_required
@role_required("Admin")
def delete_customer_route(customer_id):
    try:
        result = delete_customer(customer_id)

        if not result:
            return jsonify({
                "error": "Customer not found"
            }), 404

        return jsonify({
            "message": "Customer deleted successfully",
            "CustomerId": customer_id
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
