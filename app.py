from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "campus-reuse-demo-key"


def create_database():

    connection = sqlite3.connect("campus_reuse.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            price INTEGER NOT NULL,
            owner_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            dorm TEXT NOT NULL,
            availability TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            requester_name TEXT NOT NULL,
            requester_phone TEXT NOT NULL,
            message TEXT,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY (item_id) REFERENCES items(id)
        )
    """)

    connection.commit()
    connection.close()


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "student01" and password == "campus123":

            session["logged_in"] = True

            return redirect("/")

        return """
        <h2>Invalid Student ID or Password</h2>
        <a href="/login">Try Again</a>
        """

    return render_template("login.html")


# ---------------- HOME ----------------

@app.route("/")
def home():

    if not session.get("logged_in"):
        return redirect("/login")

    connection = sqlite3.connect("campus_reuse.db")

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM items
        ORDER BY id DESC
    """)

    items = cursor.fetchall()

    cursor.execute("""
        SELECT
            requests.id,
            requests.requester_name,
            requests.message,
            requests.status,
            items.item_name
        FROM requests
        JOIN items
        ON requests.item_id = items.id
        ORDER BY requests.id DESC
    """)

    requests_list = cursor.fetchall()

    connection.close()

    return render_template(
        "index.html",
        items=items,
        requests=requests_list
    )


# ---------------- POST ITEM ----------------

@app.route("/post", methods=["POST"])
def post_item():

    if not session.get("logged_in"):
        return redirect("/login")

    item_name = request.form["item_name"]
    category = request.form["category"]
    description = request.form["description"]
    price = request.form["price"]
    owner_name = request.form["owner_name"]
    phone = request.form["phone"]
    dorm = request.form["dorm"]
    availability = request.form["availability"]

    connection = sqlite3.connect("campus_reuse.db")

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO items
        (
            item_name,
            category,
            description,
            price,
            owner_name,
            phone,
            dorm,
            availability
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        item_name,
        category,
        description,
        price,
        owner_name,
        phone,
        dorm,
        availability
    ))

    connection.commit()

    connection.close()

    return redirect("/#browse")


# ---------------- REQUEST ITEM ----------------

@app.route("/request/<int:item_id>", methods=["POST"])
def request_item(item_id):

    if not session.get("logged_in"):
        return redirect("/login")

    requester_name = request.form["requester_name"]
    requester_phone = request.form["requester_phone"]
    message = request.form["message"]

    connection = sqlite3.connect("campus_reuse.db")

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO requests
        (
            item_id,
            requester_name,
            requester_phone,
            message,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        item_id,
        requester_name,
        requester_phone,
        message,
        "Pending"
    ))

    connection.commit()

    connection.close()

    return redirect("/#browse")


# ---------------- APPROVE / REJECT REQUEST ----------------

@app.route("/request/<int:request_id>/<status>", methods=["POST"])
def update_request_status(request_id, status):

    if not session.get("logged_in"):
        return redirect("/login")

    if status not in ["Approved", "Rejected"]:
        return redirect("/#requests")

    connection = sqlite3.connect("campus_reuse.db")

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE requests
        SET status = ?
        WHERE id = ?
    """, (
        status,
        request_id
    ))

    connection.commit()

    connection.close()

    return redirect("/#requests")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# ---------------- OLD ROUTES ----------------

@app.route("/items")
def old_items():

    return redirect("/#browse")


@app.route("/requests")
def old_requests():

    return redirect("/#requests")


# ---------------- RUN APP ----------------

if __name__ == "__main__":

    create_database()

    app.run(debug=True)