from flask import Blueprint, jsonify, request

from services.claim_service import (
    create_claim,
    get_all_claims,
    update_claim_status,
    get_customer_claims
)
from middleware.auth_middleware import token_required, role_required


claim_bp = Blueprint("claim", __name__)


@claim_bp.route("/claims", methods=["POST"])
@token_required
@role_required("Admin", "Agent", "Customer")
def add_claim():
    try:
        data = request.get_json()

        required_fields = [
            "PolicyId",
            "CustomerId",
            "ClaimAmount",
            "ClaimReason"
        ]

        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": f"{field} is required"
                }), 400

        claim_id, error = create_claim(
            data["PolicyId"],
            data["CustomerId"],
            data["ClaimAmount"],
            data["ClaimReason"]
        )

        if error:
            return jsonify({
                "error": error
            }), 404

        return jsonify({
            "message": "Claim submitted successfully",
            "ClaimId": claim_id
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@claim_bp.route("/claims", methods=["GET"])
@token_required
@role_required("Admin", "Agent")
def get_claims():
    try:
        claims = get_all_claims()

        return jsonify(claims)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@claim_bp.route("/claims/<int:claim_id>/status", methods=["PUT"])
@token_required
@role_required("Admin", "Agent")
def update_status(claim_id):
    try:
        data = request.get_json()

        status = data.get("Status")

        if not status:
            return jsonify({
                "error": "Status is required"
            }), 400

        success, error = update_claim_status(
            claim_id,
            status
        )

        if not success:
            return jsonify({
                "error": error
            }), 400

        return jsonify({
            "message": f"Claim {status.lower()} successfully",
            "ClaimId": claim_id,
            "Status": status
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@claim_bp.route("/my-claims", methods=["GET"])
@token_required
@role_required("Customer")
def my_claims():
    try:
        customer_id = request.user.get("user_id")

        if not customer_id:
            return jsonify({
                "error": "Customer information not found"
            }), 400

        claims = get_customer_claims(customer_id)

        return jsonify(claims), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500