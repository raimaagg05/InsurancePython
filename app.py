from flask import Flask, jsonify, request, render_template
from database import get_connection
from routes.customer_routes import customer_bp
from routes.policy_routes import policy_bp
from routes.auth_routes import auth_bp
from routes.claim_routes import claim_bp
from routes.payment_routes import payment_bp

app = Flask(__name__)

app.register_blueprint(customer_bp)
app.register_blueprint(policy_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(claim_bp)
app.register_blueprint(payment_bp)
@app.route("/")
def landing_page():
    return render_template("home.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/dashboard")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=False)