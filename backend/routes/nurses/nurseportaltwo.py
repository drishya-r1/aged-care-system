from flask import Blueprint, render_template, request, session, redirect, url_for, flash
import pandas as pd
from datetime import date
import os

nurse_bp = Blueprint('nurseportaltwo', __name__)

# File paths
ROSTER_FILE = 'Roster.xlsx'
PATIENT_FILE = 'Patient.xlsx'
PATIENT_CHECKLIST_FILE = 'PatientChecklist.xlsx'
DOCTOR_APPT_FILE = 'DoctorAppointments.xlsx'

def load_excel(file, default_columns):
    if os.path.exists(file):
        return pd.read_excel(file)
    else:
        return pd.DataFrame(columns=default_columns)

def save_excel(df, file):
    df.to_excel(file, index=False)

@nurse_bp.route('/caregiverHome', methods=['GET', 'POST'])
def caregiver_home():
    if 'level' not in session:
        return redirect(url_for('home'))
    if session['level'] != 4:
        return redirect(url_for('transfer'))
    
    today = date.today().strftime('%Y-%m-%d')
    group = 0

    # Load data
    roster_cols = ['date', 'careGiver1', 'careGiver2', 'careGiver3', 'careGiver4']
    patient_cols = ['patientID', 'fName', 'lName', 'groupID', 'approval']
    checklist_cols = ['patientID', 'date', 'morningMedCheck', 'lunchMedCheck', 'nightMedCheck', 'breakfast', 'lunch', 'dinner']
    appt_cols = ['patientID', 'date', 'morningMed', 'lunchMed', 'nightMed', 'attendance']

    roster_df = load_excel(ROSTER_FILE, roster_cols)
    patient_df = load_excel(PATIENT_FILE, patient_cols)
    checklist_df = load_excel(PATIENT_CHECKLIST_FILE, checklist_cols)
    appt_df = load_excel(DOCTOR_APPT_FILE, appt_cols)

    # Find group for caregiver
    res = roster_df[roster_df['date'] == today]
    if not res.empty:
        res = res.iloc[0]
        for i in range(1, 5):
            if res.get(f'careGiver{i}') == session.get('id'):
                group = i

    # Handle POST for checklist update
    if request.method == 'POST' and 'change' in request.form:
        change = request.form['change'].split()
        patient_id, column = change[0], change[1]
        mask = (checklist_df['patientID'] == patient_id) & (checklist_df['date'] == today)
        checklist_df.loc[mask, column] = 1
        save_excel(checklist_df, PATIENT_CHECKLIST_FILE)

    # Ensure checklist for today exists
    today_checklist = checklist_df[checklist_df['date'] == today]
    if today_checklist.empty:
        approved_patients = patient_df[patient_df['approval'] == 1]
        for _, patient in approved_patients.iterrows():
            new_row = {
                'patientID': patient['patientID'],
                'date': today,
                'morningMedCheck': 0,
                'lunchMedCheck': 0,
                'nightMedCheck': 0,
                'breakfast': 0,
                'lunch': 0,
                'dinner': 0
            }
            checklist_df = checklist_df.append(new_row, ignore_index=True)
        save_excel(checklist_df, PATIENT_CHECKLIST_FILE)

    # Join checklist with patient info for group
    merged = checklist_df[checklist_df['date'] == today].merge(
        patient_df[['patientID', 'fName', 'lName', 'groupID']],
        on='patientID', how='left'
    )
    patient_checklists = merged[merged['groupID'] == group].to_dict(orient='records')

    # For each patient, get latest DoctorAppointments
    for res in patient_checklists:
        appts = appt_df[(appt_df['patientID'] == res['patientID']) & (appt_df['attendance'] == 1)]
        if not appts.empty:
            latest = appts.sort_values('date', ascending=False).iloc[0]
            morn = (str(latest['morningMed']).upper() if pd.notna(latest['morningMed']) else "NONE")
            lunch = (str(latest['lunchMed']).upper() if pd.notna(latest['lunchMed']) else "NONE")
            night = (str(latest['nightMed']).upper() if pd.notna(latest['nightMed']) else "NONE")
        else:
            morn = lunch = night = "NONE"

        # Auto-check if no med prescribed
        for col, val in zip(['morningMedCheck', 'lunchMedCheck', 'nightMedCheck'], [morn, lunch, night]):
            if val == "NONE" and res[col] == 0:
                mask = (checklist_df['patientID'] == res['patientID']) & (checklist_df['date'] == today)
                checklist_df.loc[mask, col] = 1
                res[col] = 1
                save_excel(checklist_df, PATIENT_CHECKLIST_FILE)

        res['morn'] = morn
        res['lunch_med'] = lunch
        res['night_med'] = night

    return render_template(
        'caregiver_home.html',
        patient_checklists=patient_checklists,
        group=group
    )
