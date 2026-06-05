from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = "users.db"

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

    cursor.execute(
        "INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123', 'admin')"
    )

    cursor.execute(
        "INSERT OR IGNORE INTO users VALUES (2, 'user', 'user123', 'user')"
    )

    conn.commit()
    conn.close()

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    username = data.get("username", "")
    password = data.get("password", "")

    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({
            "status": "success",
            "user": user[1],
            "role": user[3],
            "query_executed": query
        })

    return jsonify({"status": "failed", "query_executed": query}), 401

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "vulnerable-app-running"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
