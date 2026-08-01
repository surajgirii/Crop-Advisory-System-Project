from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecretkey"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Batman@12",
    database="srmproject"
)

cursor = db.cursor()

# Home Redirect
@app.route("/")
def home():
    return render_template("index.html")
# Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute("INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",
                       (name,email,password))
        db.commit()

        return redirect("/login")

    return render_template("register.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s",
                       (email,password))
        user = cursor.fetchone()

        if user:
            session["user"] = user[1]
            return redirect("/dashboard")

    return render_template("login.html")

# Dashboard + Advanced Filter
@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    if "user" not in session:
        return redirect("/login")

    results = None

    if request.method == "POST":
        season = request.form["season"]
        soil = request.form["soil"]
        water = request.form["water"]

        query = """
        SELECT crop_name, water_need, fertilizer, msp_price
        FROM crops
        WHERE season=%s AND soil_type=%s AND water_need=%s
        """

        cursor.execute(query,(season,soil,water))
        results = cursor.fetchall()

    return render_template("dashboard.html", data=results, user=session["user"])

# Logout
@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)