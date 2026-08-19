from flask import Blueprint, jsonify, request
from services.policy_service import (
    get_all_policies,
    create_policy,
    get_policy_by_id,
    update_policy,
    delete_policy
)
from middleware.auth_middleware import token_required, role_required

policy_bp = Blueprint("policy", __name__)


@policy_bp.route("/policies", methods=["GET"])
@token_required
@role_required("Admin", "Agent", "Customer")
def get_policies():
    try:
        policies = get_all_policies()

        return jsonify(policies)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@policy_bp.route("/policies", methods=["POST"])
@token_required
@role_required("Admin", "Agent")
def add_policy():
    try:
        data = request.get_json()

        required_fields = [
            "PolicyNumber",
            "CustomerId",
            "PolicyType",
            "PremiumAmount",
            "CoverageAmount",
            "EffectiveDate",
            "ExpiryDate",
            "Status"
        ]

        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": f"{field} is required"
                }), 400

        policy_id = create_policy(
            data["PolicyNumber"],
            data["CustomerId"],
            data["PolicyType"],
            data["PremiumAmount"],
            data["CoverageAmount"],
            data["EffectiveDate"],
            data["ExpiryDate"],
            data["Status"]
        )

        if policy_id is None:
            return jsonify({
                "error": "Customer not found"
            }), 404

        return jsonify({
            "message": "Policy added successfully",
            "PolicyId": policy_id
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@policy_bp.route("/policies/<int:policy_id>", methods=["GET"])
@token_required
@role_required("Admin", "Agent", "Customer")
def get_policy(policy_id):
    try:
        policy = get_policy_by_id(policy_id)

        if not policy:
            return jsonify({
                "error": "Policy not found"
            }), 404

        return jsonify(policy)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@policy_bp.route("/policies/<int:policy_id>", methods=["PUT"])
@token_required
@role_required("Admin", "Agent")
def update_policy_route(policy_id):
    try:
        data = request.get_json()

        required_fields = [
            "PolicyNumber",
            "CustomerId",
            "PolicyType",
            "PremiumAmount",
            "CoverageAmount",
            "EffectiveDate",
            "ExpiryDate",
            "Status"
        ]

        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": f"{field} is required"
                }), 400

        result = update_policy(
            policy_id,
            data["PolicyNumber"],
            data["CustomerId"],
            data["PolicyType"],
            data["PremiumAmount"],
            data["CoverageAmount"],
            data["EffectiveDate"],
            data["ExpiryDate"],
            data["Status"]
        )

        if result is False:
            return jsonify({
                "error": "Policy not found"
            }), 404

        if result is None:
            return jsonify({
                "error": "Customer not found"
            }), 404

        return jsonify({
            "message": "Policy updated successfully"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@policy_bp.route("/policies/<int:policy_id>", methods=["DELETE"])
@token_required
@role_required("Admin")
def delete_policy_route(policy_id):
    try:
        result = delete_policy(policy_id)

        if not result:
            return jsonify({
                "error": "Policy not found"
            }), 404

        return jsonify({
            "message": "Policy deleted successfully",
            "PolicyId": policy_id
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
