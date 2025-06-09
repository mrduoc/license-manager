from flask import Flask, render_template, request, redirect, session, jsonify
from dao import load_all, add_license, toggle_license, delete_license, update_license, load_by_service
import uuid

app = Flask(__name__)
app.secret_key = "duoc@secretkey123"

# ========== WEB UI ==========
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admduochamhoc" and request.form["password"] == "12052004Duoc@":
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
    name = request.form.get("name", "")
    service = request.form.get("service", "")
    key = str(uuid.uuid4()).replace("-", "")[:16]
    add_license(pc_id, key, expires, name, service)
    return redirect("/")

@app.route("/edit/<pc_id>", methods=["GET", "POST"])
def edit(pc_id):
    data = load_all()
    if request.method == "POST":
        name = request.form["name"]
        expires = request.form["expires"]
        update_license(pc_id, name, expires)
        return redirect("/")
    info = data.get(pc_id)
    return render_template("edit.html", pc_id=pc_id, info=info)

@app.route("/toggle/<pc_id>")
def toggle(pc_id):
    toggle_license(pc_id)
    return redirect("/")

@app.route("/delete/<pc_id>")
def delete(pc_id):
    delete_license(pc_id)
    return redirect("/")

# ========== API ==========
@app.route("/api/register", methods=["POST"])
def register_hwid():
    data = request.get_json()
    hwid = data.get("hwid")
    service = data.get("service", "LICENSE")  # <-- default fallback

    if not hwid:
        return jsonify({"status": "error", "message": "Missing HWID"}), 400

    db = load_all()
    if hwid in db:
        return jsonify({"status": "exists", "key": db[hwid]["key"]})

    new_key = str(uuid.uuid4()).replace("-", "")[:16]
    add_license(hwid, new_key, "2099-12-31", "", service)
    return jsonify({"status": "created", "key": new_key})


@app.route('/api/check', methods=['POST'])
def api_check():
    data = request.get_json()
    key = data.get("key")
    hwid = data.get("hwid")

    if not key or not hwid:
        return jsonify({"status": "error", "reason": "Thiếu key hoặc HWID"}), 400

    from dao import check_license
    valid = check_license(hwid, key)
    if valid:
        return jsonify({"status": "valid"})
    else:
        return jsonify({"status": "invalid", "reason": "Không khớp hoặc chưa được duyệt"})

@app.route("/api/licenses")
def api_all():
    return jsonify(load_all())

@app.route("/api/licenses/<service>")
def api_by_service(service):
    return jsonify(load_by_service(service.upper()))
@app.route("/edit_modal", methods=["POST"])
def edit_modal():
    pc_id = request.form["pc_id"]
    name = request.form["name"]
    expires = request.form["expires"]
    update_license(pc_id, name, expires)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
