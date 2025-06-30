import os
import pandas as pd
from flask import Blueprint, request, jsonify
from datetime import datetime

feedback_bp = Blueprint('feedback', __name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data')
FEEDBACK_FILE = os.path.join(DATA_DIR, 'feedback.xlsx')

@feedback_bp.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    username = data.get('username')
    unit = data.get('unit')
    feedback = data.get('feedback')
    timestamp = datetime.now().isoformat()
    if not (username and unit and feedback):
        return jsonify({'success': False, 'error': 'Missing fields'}), 400
    row = {'username': username, 'unit': unit, 'feedback': feedback, 'timestamp': timestamp}
    if os.path.exists(FEEDBACK_FILE):
        df = pd.read_excel(FEEDBACK_FILE)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])
    df.to_excel(FEEDBACK_FILE, index=False)
    return jsonify({'success': True})

@feedback_bp.route('/api/feedback/all', methods=['GET'])
def get_all_feedback():
    if os.path.exists(FEEDBACK_FILE):
        df = pd.read_excel(FEEDBACK_FILE)
        feedback_list = df.fillna('').to_dict(orient='records')
        return jsonify({'feedback': feedback_list})
    else:
        return jsonify({'feedback': []})
