from flask import Blueprint, request, jsonify, redirect, url_for
from flask import Blueprint, request, jsonify, session
from backend.database.excel_manager import login
from backend.database import excel_manager
import random
import string
import pandas as pd
import os

login_bp = Blueprint('login', __name__)
forgot_bp = Blueprint('forgot', __name__)

@login_bp.route('/login', methods=['POST'])
def login_route():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    user = login(username, password)
    print(f"User found: {user}")
    if user:
        session['username'] = username
        session['usertype'] = user.get('usertype')
        # Try both 'userid' and 'user_id' to be safe
        userid = user.get('userid') or user.get('user_id')
        session['userid'] = userid
        print(f"Session set for user: {session['username']}, type: {session['usertype']}, userid: {session['userid']} ")
        return jsonify({
            'success': True,
            'user': {
                'username': user.get('username'),
                'usertype': user.get('usertype'),
                'userid': userid
            }
        })
    return jsonify({'success': False, 'message': 'Invalid credentials.'}), 401

@login_bp.route('/api/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    user = data.get('user', '').strip()
    # Example: search user in users.xlsx by userid or email
    users_file = os.path.join('..', 'data', 'users.xlsx')
    if not os.path.exists(users_file):
        return jsonify({'success': False, 'message': 'User database not found.'})
    df = pd.read_excel(users_file)
    df.columns = df.columns.str.strip()
    user_row = df[(df['userid'].astype(str) == user) | (df.get('email', '').astype(str) == user)]
    if user_row.empty:
        return jsonify({'success': False, 'message': 'User not found.'})
    # Generate a new temp password
    temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    df.loc[user_row.index, 'password'] = temp_password
    df.to_excel(users_file, index=False)
    # In production, send email. For demo, just return password.
    return jsonify({'success': True, 'message': f'Your temporary password is: {temp_password}'})

# Dummy users for demonstration (replace with Excel/DB lookup in production)
# USERS = {
#     "resident1": "password123",
#     "nurse1": "nursepass",
#     "manager1": "managerpass"
# }

# @login_bp.route('/login', methods=['POST'])
# def login():
#     username = request.form.get('username')
#     password = request.form.get('password')
#     if not username or not password:
#         return jsonify({"error": "Missing username or password"}), 400

#     # Simple authentication check
#     if username in USERS and USERS[username] == password:
#         # Redirect based on role (for demo, just by username)
#         if username.startswith("resident"):
#             return redirect("/homeresidents")
#         elif username.startswith("nurse"):
#             return redirect("/homenurse")
#         elif username.startswith("manager"):
#             return redirect("/homemanager")
#         else:
#             return redirect("/")
#     else:
#         return jsonify({"error": "Invalid credentials"}), 401

@login_bp.route('/forgot-password')
def forgot_password_route():
    # In a real app, trigger email/SMS alert to manager here
    return jsonify({"message": "Alert sent to the manager!"}), 200

@login_bp.route('/api/logout', methods=['POST'])
def logout():
    data = request.get_json()
    userid = data.get('userid')
    if userid:
        excel_manager.update_logged_in_status(userid, False)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'No userid provided'}), 400