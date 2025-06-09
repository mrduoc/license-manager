from flask import Flask, render_template, request, redirect, jsonify
import hashlib, json, os
from datetime import datetime

app = Flask(__name__)
LICENSE_FILE = 'license.json'
SECRET_KEY = 'duochamhoc_secret_'

def load_licenses():
    if not os.path.exists(LICENSE_FILE):
        return {}
    with open(LICENSE_FILE, 'r') as f:
        return json.load(f)

def save_licenses(data):
    with open(LICENSE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def generate_key(pc_id):
    return hashlib.sha256((SECRET_KEY + pc_id).encode()).hexdigest()[:16].upper()

@app.route('/')
def index():
    data = load_licenses()
    return render_template('index.html', licenses=data.get('licenses', {}))

@app.route('/add', methods=['POST'])
def add():
    pc_id = request.form['pc_id'].strip()
    expires = request.form['expires'].strip()
    key = generate_key(pc_id)

    data = load_licenses()
    if 'licenses' not in data:
        data['licenses'] = {}
    data['licenses'][pc_id] = {
        'key': key,
        'active': True,
        'expires': expires
    }
    save_licenses(data)
    return redirect('/')

@app.route('/toggle/<pc_id>')
def toggle(pc_id):
    data = load_licenses()
    if pc_id in data['licenses']:
        data['licenses'][pc_id]['active'] = not data['licenses'][pc_id].get('active', True)
    save_licenses(data)
    return redirect('/')

@app.route('/delete/<pc_id>')
def delete(pc_id):
    data = load_licenses()
    if pc_id in data['licenses']:
        del data['licenses'][pc_id]
    save_licenses(data)
    return redirect('/')

@app.route('/json')
def export_json():
    return jsonify(load_licenses())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
