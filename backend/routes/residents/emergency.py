from flask import Blueprint, request, jsonify
from backend.database import alert_excel

emergency_bp = Blueprint('emergency', __name__)

# @emergency_bp.route('/log_incident', methods=['POST'])
# def log_incident_route():
#     data = request.json
#     resident_id = data.get('resident_id')
#     incident_description = data.get('description')
    
#     if not resident_id or not incident_description:
#         return jsonify({'error': 'Resident ID and description are required.'}), 400
    
#     success = log_incident(resident_id, incident_description)
    
#     if success:
#         return jsonify({'message': 'Incident logged successfully.'}), 201
#     else:
#         return jsonify({'error': 'Failed to log incident.'}), 500

# @emergency_bp.route('/send_alert', methods=['POST'])
# def send_alert_route():
#     data = request.json
#     nurse_id = data.get('nurse_id')
#     alert_message = data.get('message')
    
#     if not nurse_id or not alert_message:
#         return jsonify({'error': 'Nurse ID and alert message are required.'}), 400
    
#     success = send_alert(nurse_id, alert_message)
    
#     if success:
#         return jsonify({'message': 'Alert sent successfully.'}), 200
#     else:
#         return jsonify({'error': 'Failed to send alert.'}), 500


# @emergency_bp.route('/send_food_request', methods=['POST'])
# def send_food_request_route():
#     data = request.json
#     nurse_id = data.get('nurse_id')
#     food_request_message = data.get('message')

#     if not nurse_id or not food_request_message:
#         return jsonify({'error': 'Nurse ID and food request message are required.'}), 400

#     success = send_alert(nurse_id, food_request_message)

#     if success:
#         return jsonify({'message': 'Alert sent successfully.'}), 200
#     else:
#         return jsonify({'error': 'Failed to send alert.'}), 500
@emergency_bp.route('/api/alerts', methods=['POST'])
def add_alert():
    data = request.get_json()
    # Add code to save alert to alerts.xlsx
    alert_excel.add_alert(data)
    return jsonify({'success': True, 'message': 'Alert sent'})