from flask import Blueprint, request, jsonify, session
from backend.database import excel_manager
import random
import string
import os
import pandas as pd
import boto3
import zipfile
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

def generate_temp_password(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@admin_bp.route('/api/admin/onboard_resident', methods=['POST'])
def onboard_resident():
    data = request.get_json()
    temp_password = generate_temp_password()
    user_data = {
        'userid': data['userid'],
        'username': data['username'],
        'usertype': 'RES',
        'password': temp_password,  # Will be hashed in excel_manager
        'logged_in_status': False
    }
    excel_manager.add_user(user_data)
    resident_data = {
        'resident_id': data['resident_id'],
        'userid': data['userid'],
        'username': data['username'],
        'first_name': data.get('first_name', ''),
        'last_name': data.get('last_name', ''),
        'name': data.get('name', ''),
        'unit': data.get('unit', ''),
        'date_of_birth': data.get('date_of_birth', ''),
        'dietary_notes': data.get('dietary_notes', '')
    }
    excel_manager.add_resident(resident_data)
    return jsonify({'success': True, 'temp_password': temp_password})

@admin_bp.route('/api/admin/onboard_nurse', methods=['POST'])
def onboard_nurse():
    data = request.get_json()
    temp_password = generate_temp_password()
    user_data = {
        'userid': data['userid'],
        'username': data['name'],
        'usertype': 'NUR',
        'password': temp_password,  # Will be hashed in excel_manager
        'logged_in_status': False
    }
    excel_manager.add_user(user_data)
    nurse_data = {
        'nurse_id': data['nurse_id'],
        'name': data['name'],
        'DOB': data.get('DOB', ''),
        'units_allocated': data.get('units_allocated', ''),
        'mobile_number': data.get('mobile_number', ''),
        'email': data.get('email', ''),
        'experience': data.get('experience', ''),
        'qualifications': data.get('qualifications', ''),
        'userid': data['userid']
    }
    excel_manager.add_nurse(nurse_data)
    return jsonify({'success': True, 'temp_password': temp_password})

@admin_bp.route('/api/admin/search_residents', methods=['GET'])
def search_residents():
    from backend.database import excel_manager
    resident_id = request.args.get('resident_id', '').strip()
    name = request.args.get('name', '').strip().lower()
    unit = request.args.get('unit', '').strip().lower()
    residents = excel_manager.read_all_residents()
    results = []
    for r in residents:
        if resident_id and str(r.get('resident_id', '')).strip() != resident_id:
            continue
        if name and name not in str(r.get('name', '')).strip().lower():
            continue
        if unit and unit not in str(r.get('unit', '')).strip().lower():
            continue
        results.append(r)
    return jsonify({'residents': results})

@admin_bp.route('/api/admin/update_resident', methods=['POST'])
def update_resident():
    data = request.get_json()
    resident_id = data.get('resident_id')
    if not resident_id:
        return jsonify({'success': False, 'error': 'Resident ID required'})
    # Remove resident_id from update dict to avoid overwriting the key
    update_dict = {k: v for k, v in data.items() if k != 'resident_id'}
    print('Update Resident Data:', update_dict)
    from backend.database import excel_manager
    success = excel_manager.update_record_by_id('residents.xlsx', 'resident_id', resident_id, update_dict)
    return jsonify({'success': success})

@admin_bp.route('/api/admin/search_nurses', methods=['GET'])
def search_nurses():
    from backend.database import excel_manager
    nurse_id = request.args.get('nurse_id', '').strip()
    name = request.args.get('name', '').strip().lower()
    units_allocated = request.args.get('units_allocated', '').strip().lower()
    nurses = excel_manager.read_all_nurses()
    results = []
    for n in nurses:
        if nurse_id and str(n.get('nurse_id', '')).strip() != nurse_id:
            continue
        if name and name not in str(n.get('name', '')).strip().lower():
            continue
        if units_allocated and units_allocated not in str(n.get('units_allocated', '')).strip().lower():
            continue
        results.append(n)
    return jsonify({'nurses': results})

@admin_bp.route('/api/admin/update_nurse', methods=['POST'])
def update_nurse():
    data = request.get_json()
    nurse_id = data.get('nurse_id')
    if not nurse_id:
        return jsonify({'success': False, 'error': 'Nurse ID required'})
    update_dict = {k: v for k, v in data.items() if k != 'nurse_id'}
    from backend.database import excel_manager
    success = excel_manager.update_record_by_id('nurses.xlsx', 'nurse_id', nurse_id, update_dict)
    return jsonify({'success': success})

@admin_bp.route('/api/admin/search_users')
def search_users():
    users_file = os.path.join(os.path.dirname(__file__), '../../data/users.xlsx')
    users_file = os.path.abspath(users_file)
    df = pd.read_excel(users_file)
    df.columns = df.columns.str.strip()
    userid = request.args.get('userid', '').strip()
    username = request.args.get('username', '').strip().lower()
    users = []
    for _, row in df.iterrows():
        if userid and str(row.get('userid', '')).strip() != userid:
            continue
        if username and username not in str(row.get('username', '')).strip().lower():
            continue
        users.append({
            'userid': row.get('userid', ''),
            'username': row.get('username', ''),
            'active': bool(row.get('active', True))
        })
    return jsonify({'users': users})

@admin_bp.route('/api/admin/reset_user_password', methods=['POST'])
def reset_user_password():
    data = request.get_json()
    username = data.get('username')
    if not username:
        return jsonify({'success': False, 'message': 'Username required'})
    temp_password = generate_temp_password()
    success = excel_manager.reset_user_password_by_username(username, temp_password)
    if success:
        return jsonify({'success': True, 'temp_password': temp_password})
    return jsonify({'success': False, 'message': 'User not found'})

@admin_bp.route('/api/admin/toggle_user_active', methods=['POST'])
def toggle_user_active():
    data = request.get_json()
    userid = data.get('userid')
    active = data.get('active')
    users_file = os.path.join(os.path.dirname(__file__), '../../data/users.xlsx')
    users_file = os.path.abspath(users_file)
    df = pd.read_excel(users_file)
    df.columns = df.columns.str.strip()
    mask = df['userid'].astype(str) == str(userid)
    if mask.any():
        df.loc[mask, 'active'] = bool(active)
        df.to_excel(users_file, index=False)
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'User not found'})

@admin_bp.route('/api/admin/backup', methods=['POST'])
def backup_data():
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data')
    backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    backup_path = os.path.join(data_dir, backup_name)
    with zipfile.ZipFile(backup_path, 'w') as backup_zip:
        for filename in os.listdir(data_dir):
            if filename.endswith('.xlsx'):
                backup_zip.write(os.path.join(data_dir, filename), filename)
    s3 = boto3.client('s3')
    bucket_name = 'aged-care-system-data-backup' 
    try:
        s3.upload_file(backup_path, bucket_name, backup_name)
        os.remove(backup_path)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
