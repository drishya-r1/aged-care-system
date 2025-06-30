from flask import Blueprint, request, jsonify
from backend.database.excel_manager import add_user, search_user

# resident_onboarding_bp = Blueprint('resident_onboarding', __name__)

@resident_onboarding_bp.route('/residents/new', methods=['POST'])
def add_resident():
    data = request.json
    if not data or not data.get('username'):
        return jsonify({'success': False, 'message': 'Username is required.'}), 400
    if search_user(data['username']):
        return jsonify({'success': False, 'message': 'Username already exists.'}), 400
    data['usertype'] = 'resident'
    add_user(data)
    return jsonify({'success': True, 'message': 'Resident added successfully.'})

@resident_onboarding_bp.route('/residents/<username>', methods=['GET'])
def get_resident_profile(username):
    user = search_user(username)
    if user and user.get('usertype') == 'resident':
        return jsonify({'success': True, 'profile': user})
    return jsonify({'success': False, 'message': 'Resident not found.'}), 404