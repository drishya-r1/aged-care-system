from flask import Blueprint, jsonify, request
from backend.database import excel_manager

resident_bp = Blueprint('resident', __name__)

@resident_bp.route('/api/resident/<int:userid>', methods=['GET'])
def get_resident_by_id(userid):
    """
    Get resident details by userid (user_id).
    """
    resident = excel_manager.read_record_by_id('residents.xlsx', 'userid', userid)
    if resident:
        return jsonify({'success': True, 'resident': resident})
    else:
        return jsonify({'success': False, 'message': 'Resident not found'}), 404

@resident_bp.route('/api/residents', methods=['GET'])
def get_all_residents():
    """
    Get details of all residents.
    """
    residents = excel_manager.read_all_rows('residents.xlsx')
    return jsonify({'success': True, 'residents': residents})

@resident_bp.route('/api/resident', methods=['POST'])
def add_resident():
    """
    Add a new resident.
    Expects JSON with all required resident fields.
    """
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    excel_manager.add_record('residents.xlsx', data)
    return jsonify({'success': True, 'message': 'Resident added'})

@resident_bp.route('/api/resident/<int:userid>', methods=['PUT'])
def update_resident(userid):
    """
    Update an existing resident by resident_id.
    Expects JSON with fields to update.
    """
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    updated = excel_manager.update_record_by_id('residents.xlsx', 'resident_id', userid, data)
    if updated:
        return jsonify({'success': True, 'message': 'Resident updated'})
    else:
        return jsonify({'success': False, 'message': 'Resident not found'}), 404

@resident_bp.route('/api/get_events', methods=['GET'])
def get_events():
    events = excel_manager.read_all_events()
    return jsonify({'events': events})

@resident_bp.route('/api/resident/details', methods=['GET'])
def get_resident_details():
    userid = request.args.get('userid')
    residents = excel_manager.read_all_residents()  # Implement this function
    resident = next((r for r in residents if str(r.get('userid')) == str(userid)), None)
    if resident:
        return jsonify({
            'resident_id': resident.get('resident_id'),
            'unit': resident.get('unit'),
            'name': resident.get('name')
        })
    else:
        return jsonify({'error': 'Resident not found'}), 404