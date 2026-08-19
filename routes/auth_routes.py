from flask import Blueprint, jsonify, request

from middleware.auth_middleware import token_required, role_required

from services.auth_service import register_user, login_user


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        full_name = data.get("FullName")
        email = data.get("Email")
        password = data.get("Password")
        role = data.get("Role", "Customer")

        if not full_name or not email or not password:
            return jsonify({
                "error": "FullName, Email and Password are required"
            }), 400

        if role not in ["Admin", "Agent", "Customer"]:
            return jsonify({
                "error": "Invalid role"
            }), 400

        user_id, error = register_user(
            full_name,
            email,
            password,
            role
        )

        if error:
            return jsonify({
                "error": error
            }), 409

        return jsonify({
            "message": "User registered successfully",
            "UserId": user_id
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@auth_bp.route("/auth/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        email = data.get("Email")
        password = data.get("Password")

        if not email or not password:
            return jsonify({
                "error": "Email and Password are required"
            }), 400

        user, error = login_user(
            email,
            password
        )

        if error:
            return jsonify({
                "error": error
            }), 401

        return jsonify({
    "message": "Login successful",
    "user": user["user"],
    "token": user["token"]
}), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@auth_bp.route("/auth/admin-test", methods=["GET"])
@token_required
@role_required("Admin")
def admin_test():
    return jsonify({
        "message": "Admin access granted"
    })