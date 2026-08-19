from flask import Blueprint, jsonify, request, render_template

from services.payment_service import (
    create_payment_order,
    verify_payment
)

from middleware.auth_middleware import (
    token_required,
    role_required
)


payment_bp = Blueprint("payment", __name__)


@payment_bp.route("/payments/create", methods=["POST"])
@token_required
@role_required("Admin", "Agent", "Customer")
def create_payment():
    try:
        data = request.get_json()

        required_fields = [
            "PolicyId",
            "CustomerId",
            "Amount"
        ]

        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": f"{field} is required"
                }), 400

        payment, error = create_payment_order(
            data["PolicyId"],
            data["CustomerId"],
            data["Amount"]
        )

        if error:
            return jsonify({
                "error": error
            }), 404

        return jsonify({
            "message": "Payment order created successfully",
            "payment": payment
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@payment_bp.route("/payments/verify", methods=["POST"])
@token_required
@role_required("Admin", "Agent", "Customer")
def verify_payment_route():
    try:
        data = request.get_json()

        required_fields = [
            "razorpay_order_id",
            "razorpay_payment_id",
            "razorpay_signature"
        ]

        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": f"{field} is required"
                }), 400

        success, error = verify_payment(
            data["razorpay_order_id"],
            data["razorpay_payment_id"],
            data["razorpay_signature"]
        )

        if not success:
            return jsonify({
                "error": error
            }), 400

        return jsonify({
            "message": "Payment verified successfully",
            "status": "Paid"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@payment_bp.route("/payment", methods=["GET"])
def payment_page():
    return render_template("payment.html")
