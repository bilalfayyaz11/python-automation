from flask import Flask, jsonify
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)
auth = HTTPTokenAuth(scheme="Bearer")

users = [
    {"id": 1, "name": "Alice Johnson", "role": "DevOps Engineer"},
    {"id": 2, "name": "Bob Smith", "role": "SRE"},
    {"id": 3, "name": "Carol White", "role": "Platform Engineer"},
]

VALID_TOKEN = "dev-token-12345"

@auth.verify_token
def verify_token(token):
    return token == VALID_TOKEN

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "User API"})

@app.route("/api/users", methods=["GET"])
@auth.login_required
def get_users():
    return jsonify({"users": users, "count": len(users)})

@app.route("/api/users/<int:user_id>", methods=["GET"])
@auth.login_required
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
