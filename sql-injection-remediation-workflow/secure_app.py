from flask import Flask, request, jsonify
import sqlite3
import hashlib
import re

app = Flask(__name__)
DATABASE = "users_secure.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_input(username, password):
    if not isinstance(username, str) or not isinstance(password, str):
        return False, "username and password must be strings"

    if len(username) < 3 or len(username) > 50:
        return False, "username must be between 3 and 50 characters"

    if len(password) < 6:
        return False, "password must be at least 6 characters"

    if not re.match(r"^[A-Za-z0-9_.-]+$", username):
        return False, "username contains invalid characters"

    return True, None

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)

    admin_hash = hash_password("admin123")
    user_hash = hash_password("user123")

    cursor.execute(
        "INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)",
        (1, "admin", admin_hash, "admin")
    )

    cursor.execute(
        "INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)",
        (2, "user", user_hash, "user")
    )

    conn.commit()
    conn.close()

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    username = data.get("username", "")
    password = data.get("password", "")

    is_valid, error_message = validate_input(username, password)

    if not is_valid:
        return jsonify({
            "status": "failed",
            "error": error_message
        }), 400

    password_hash = hash_password(password)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, role FROM users WHERE username=? AND password=?",
        (username, password_hash)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({
            "status": "success",
            "user": user[1],
            "role": user[2]
        })

    return jsonify({"status": "failed"}), 401

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "secure-app-running"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5001, debug=False)
