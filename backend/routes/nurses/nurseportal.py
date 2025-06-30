from flask import Flask, render_template, request, redirect, session, flash
import pandas as pd
from datetime import datetime
import os
from flask import Blueprint, render_template, request, jsonify
from backend.database import excel_manager

nurseportal_bp = Blueprint('nurseportal', __name__)

# EXCEL_FILE = 'DoctorAppointments.xlsx'

# def load_appointments():
#     if os.path.exists(EXCEL_FILE):
#         return pd.read_excel(EXCEL_FILE)
#     else:
#         # Create an empty DataFrame with expected columns if file doesn't exist
#         columns = ['patientID', 'date', 'comment', 'morningMed', 'lunchMed', 'nightMed', 'attendance', 'fName', 'lName']
#         return pd.DataFrame(columns=columns)

# def save_appointments(df):
#     df.to_excel(EXCEL_FILE, index=False)

# @nurseportal_bp.route('/nurseportal', methods=['GET', 'POST'])
# def doctor_home():
#     if 'level' not in session:
#         return redirect('/home')
#     if session['level'] != 3:
#         return redirect('/extras/transfer')
#     date_today = datetime.now().strftime('%Y-%m-%d')
#     message = None
#     df = load_appointments()

#     if request.method == 'POST':
#         if 'create' in request.form:
#             patient = request.form['patientID']
#             date = request.form['date']
#             comment = request.form['comment']
#             morningMed = request.form['morningMed']
#             lunchMed = request.form['lunchMed']
#             nightMed = request.form['nightMed']
#             # Update the row where patientID and date match
#             mask = (df['patientID'] == patient) & (df['date'] == date)
#             if mask.any():
#                 df.loc[mask, ['comment', 'morningMed', 'lunchMed', 'nightMed', 'attendance']] = [comment, morningMed, lunchMed, nightMed, 1]
#                 message = "File Updated"
#             else:
#                 # Optionally, add a new row if not found
#                 new_row = {
#                     'patientID': patient,
#                     'date': date,
#                     'comment': comment,
#                     'morningMed': morningMed,
#                     'lunchMed': lunchMed,
#                     'nightMed': nightMed,
#                     'attendance': 1,
#                     'fName': '',  # Fill as needed
#                     'lName': ''
#                 }
#                 df = df.append(new_row, ignore_index=True)
#                 message = "New appointment added"
#             save_appointments(df)
#         elif 'search' in request.form:
#             old_appointments = df[pd.to_datetime(df['date']) < pd.to_datetime(date_today)]
#             return render_template('nursehome.html', old_appointments=old_appointments.to_dict(orient='records'), message=message)
#         elif 'submit' in request.form:
#             new_appointments = df[pd.to_datetime(df['date']) >= pd.to_datetime(date_today)]
#             return render_template('nurseportal.html', new_appointments=new_appointments.to_dict(orient='records'), message=message)

#     return render_template('nurseportal.html', message=message)


# @nurseportal_bp.route('/nurseportal')
# def nurse_portal():
#     # Example data, replace with your Excel logic as needed
#     doctor_name = "Smith"
#     appointments = [
#         {"patient_name": "John Doe", "date": "2025-06-19", "time": "09:00", "id": 1},
#         {"patient_name": "Jane Roe", "date": "2025-06-19", "time": "10:00", "id": 2}
#     ]
#     return render_template(
#         "nurseportal.html",
#         doctor_name=doctor_name,
#         appointments=appointments
#     )

@nurseportal_bp.route('/api/nurse/alerts', methods=['GET'])
def get_nurse_alerts():
    units = request.args.get('units', '')
    units_list = [str(u).strip() for u in units.split(',') if u.strip()]
    alerts = excel_manager.read_all_alerts() or []
    # Ensure each alert has a 'unit' key and filter accordingly
    print(f"Units list for filtering: {units_list}")
    print(f"Alerts loaded: {alerts}")
    # filtered = [a for a in alerts if str(a.get('unit')) in units_list]
    # print(f"Filtered alerts: {filtered}")
    # return jsonify({'alerts': filtered})
    return jsonify({'alerts': alerts})

@nurseportal_bp.route('/api/nurse/food_alerts', methods=['GET'])
def get_nurse_food_alerts():
    units = request.args.get('units', '')
    units_list = [str(u).strip() for u in units.split(',') if u.strip()]
    food_alerts = excel_manager.read_all_food_alerts() or []
    # Ensure both sides are strings for comparison
    #filtered = [a for a in food_alerts if str(a.get('unit')) in units_list]
    return jsonify({'food_alerts': food_alerts})

@nurseportal_bp.route('/api/nurse/alert_status', methods=['POST'])
def update_alert_status():
    data = request.get_json()
    alert_id = data.get('alert_id')
    print (f"Updating alert status for ID: {alert_id}")
    new_status = data.get('status')
    print (f"New status: {new_status}")
    excel_manager.update_alert_status(alert_id, new_status)
    return jsonify({'success': True})

@nurseportal_bp.route('/api/nurse/food_alert_status', methods=['POST'])
def update_food_alert_status():
    data = request.get_json()
    alert_id = data.get('alert_id')
    new_status = data.get('status')
    excel_manager.update_food_alert_status(alert_id, new_status)
    return jsonify({'success': True})

@nurseportal_bp.route('/api/nurse/details', methods=['GET'])
def get_nurse_details():
    userid = request.args.get('userid')
    nurses = excel_manager.read_all_nurses()
    # Find nurse where 'userid' matches
    nurse = next((n for n in nurses if str(n.get('userid')) == str(userid)), None)
    if nurse:
        # debug data
        print(f"Found nurse: {nurse}")
        return jsonify({
            'nurse_id': nurse.get('nurse_id'),
            'nurse_name': nurse.get('name'),
            'units': nurse.get('units_allocated')
        })
    else:
        return jsonify({'error': 'Nurse not found'}), 404

