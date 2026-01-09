from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = "expense-tracker-2k26-secret-key"

# ✅ MySQL configuration (mysql-connector)
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Sim@12345678",   # your MySQL password
    "database": "expense_tracker_2k26"
}

def get_db_connection():
    return mysql.connector.connect(**db_config, buffered=True)


# 🔍 Test route
@app.route("/test-db")
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()  # ✅ consume result
        cursor.close()
        conn.close()
        return "✅ Database connected successfully!"
    except Exception as e:
        return f"❌ Database connection failed: {e}"

@app.route("/")
def home():
    return "Expense Tracker 2k26 is running 🚀"

# 📝 Register
@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if not username or not email or not password:
            error = "All fields are required"
        else:
            hashed_password = generate_password_hash(password)

            try:
                conn = get_db_connection()
                cursor = conn.cursor()

                cursor.execute(
                    "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                    (username, email, hashed_password)
                )

                conn.commit()
                cursor.close()
                conn.close()

                return redirect(url_for("login"))

            except Exception:
                error = "User already exists or database error"

    return render_template("register.html", error=error)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid email or password"

    return render_template("login.html", error=error)
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM expenses WHERE user_id = %s ORDER BY expense_date DESC",
        (session["user_id"],)
    )
    expenses = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("dashboard.html", expenses=expenses)
@app.route("/add-expense", methods=["POST"])
def add_expense():
    if "user_id" not in session:
        return redirect(url_for("login"))

    amount = request.form["amount"]
    category = request.form["category"]
    expense_date = request.form["expense_date"]
    description = request.form["description"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO expenses (user_id, amount, category, expense_date, description)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (session["user_id"], amount, category, expense_date, description)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("dashboard"))


@app.route("/delete-expense/<int:id>")
def delete_expense(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = %s AND user_id = %s",
        (id, session["user_id"])
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("dashboard"))

@app.route("/edit-expense/<int:id>", methods=["GET", "POST"])
def edit_expense(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        amount = request.form["amount"]
        category = request.form["category"]
        expense_date = request.form["expense_date"]
        description = request.form["description"]

        cursor.execute(
            """
            UPDATE expenses
            SET amount = %s, category = %s, expense_date = %s, description = %s
            WHERE id = %s AND user_id = %s
            """,
            (amount, category, expense_date, description, id, session["user_id"])
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("dashboard"))

    # GET request → fetch existing expense
    cursor.execute(
        "SELECT * FROM expenses WHERE id = %s AND user_id = %s",
        (id, session["user_id"])
    )
    expense = cursor.fetchone()

    cursor.close()
    conn.close()

    if not expense:
        return redirect(url_for("dashboard"))

    return render_template("edit_expense.html", expense=expense)

if __name__ == "__main__":
    app.run(debug=True)
