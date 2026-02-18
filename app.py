import sqlite3
from flask import Flask, render_template, redirect, session, request

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.secret_key = "dev-key"

@app.route("/") #This is the login page
def home():
    return render_template("login.html")

@app.route("/login/coach", methods = ["POST"]) #This is the coach login button
def login_coach():
    session["role"] = "Coach"
    return redirect("/dashboard")

@app.route("/login/player", methods = ["POST"]) #This is the player login button
def login_player():
    session["role"] = "Player"   
    return redirect("/dashboard")

@app.route("/dashboard") #This loads the dashboard for your role (if you have a role as coach/player)
def dashboard():
    role = session.get("role")
    if role is None:
        return redirect("/")
    return render_template("dashboard.html", role = role)

@app.route("/logout") #This "logs you out" and send you back to login
def logout():
    session.clear()
    return redirect("/")

@app.route("/announcements", methods = ["GET", "POST"]) #load announcements page
def announcements():
    role = session.get("role")
    if role is None:
        return redirect("/")
    
    if request.method == "POST":
        if role != "Coach":
            return redirect("/announcements")
        title = request.form["title"]
        content = request.form["content"]
        
        conn = get_db_connection()
        username = session.get("username")
        conn.execute(
            "INSERT INTO announcements (title, content, author) VALUES (?, ?, ?)",
            (title, content, username)
        )
        conn.commit()
        conn.close()
        
        return redirect("/announcements")
    
    conn = get_db_connection()
    announcements = conn.execute(
        "SELECT * FROM announcements ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    
    return render_template(
        "announcements.html", 
        announcements = announcements,
        role = role
    )
    
    
        
if __name__ == "__main__":
    app.run(debug = True)