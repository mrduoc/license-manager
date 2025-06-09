from flask import Flask, render_template, request, redirect, session
from dao import load_all, add_license, toggle_license, delete_license
import uuid

app = Flask(__name__)
app.secret_key = "duoc@secretkey123"

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "123456":
            session["logged_in"] = True
            return redirect("/")
        return render_template("login.html", error="Sai tài khoản hoặc mật khẩu")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login")

@app.route("/")
def index():
    if not session.get("logged_in"):
        return redirect("/login")
    data = load_all()
    return render_template("index.html", licenses=data)

@app.route("/add", methods=["POST"])
def add():
    pc_id = request.form["pc_id"]
    expires = request.form["expires"]
    key = str(uuid.uuid4()).replace("-", "")[:16]
    add_license(pc_id, key, expires)
    return redirect("/")

@app.route("/toggle/<pc_id>")
def toggle(pc_id):
    toggle_license(pc_id)
    return redirect("/")

@app.route("/delete/<pc_id>")
def delete(pc_id):
    delete_license(pc_id)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
