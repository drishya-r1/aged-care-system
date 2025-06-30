from flask import Flask, send_from_directory
from flask import jsonify
from flask import request
from flask_cors import CORS
from backend.routes.login import login_bp
#from backend.routes.emergency import emergency_bp
from backend.routes.nurses.nurseportal import nurseportal_bp
from backend.routes.residents.food_requests import food_bp
from backend.routes.residents.resident_details import resident_bp
from backend.routes.residents.emergency import emergency_bp
from backend.routes.admin.admin import admin_bp
import sys
import os

app = Flask(__name__, static_folder='../frontend')
app.secret_key = 'G1bb0nS3cr3tK3y'  # Set a secret key for session management
CORS(app)

# Registering the login routes
app.register_blueprint(login_bp)

# Registering the emergency routes
#app.register_blueprint(emergency_bp)

# Registering the nurse portal routes
app.register_blueprint(nurseportal_bp) 
app.register_blueprint(resident_bp)
app.register_blueprint(emergency_bp)

app.register_blueprint(food_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def serve_login():
    return send_from_directory(app.static_folder, 'html/login.html')

@app.route('/frontend/html/<path:filename>')
def serve_frontend_html(filename):
    return send_from_directory(os.path.join(app.root_path, '../frontend/html'), filename)
# def home():
#     return jsonify({"message": "Welcome to the Aged Care Assistance System API"})

if __name__ == '__main__':
    app.run(debug=True)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))