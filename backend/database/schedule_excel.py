import pandas as pd
from datetime import date
from backend.database.excel_manager import ExcelManager

class ScheduleExcel:
    def get_today_checklist(self, sheet_name):
        try:
            data = self.read_data(sheet_name)
            if data is not None:
                today = date.today().strftime('%Y-%m-%d')
                return data[data['date'] == today]
            return pd.DataFrame()  # Return empty DataFrame if no data found
        except Exception as e:
            print(f"Error getting today's checklist from {sheet_name}: {e}")
            return pd.DataFrame()
    
    def get_patient_data(self, sheet_name, patient_id):
        try:
            data = self.read_data(sheet_name)
            if data is not None:
                return data[data['patientID'] == patient_id]
            return pd.DataFrame()  # Return empty DataFrame if no data found
        except Exception as e:
            print(f"Error getting patient data from {sheet_name}: {e}")
            return pd.DataFrame()
    
    def update_checklist(self, sheet_name, patient_id, column, value):
        try:
            data = self.read_data(sheet_name)
            if data is not None:
                mask = (data['patientID'] == patient_id) & (data['date'] == date.today().strftime('%Y-%m-%d'))
                if mask.any():
                    data.loc[mask, column] = value
                    self.write_data(sheet_name, data)
                else:
                    print(f"No matching record found for patient {patient_id} on today's date.")
        except Exception as e:
            print(f"Error updating checklist for {sheet_name}: {e}")
    
    def get_roster_for_today(self, sheet_name):
        try:
            data = self.read_data(sheet_name)
            if data is not None:
                today = date.today().strftime('%Y-%m-%d')
                return data[data['date'] == today]
            return pd.DataFrame()  # Return empty DataFrame if no data found
        except Exception as e:
            print(f"Error getting today's roster from {sheet_name}: {e}")
            return pd.DataFrame()
    
    def get_patient_appointments(self, sheet_name, patient_id):
        try:
            data = self.read_data(sheet_name)
            if data is not None:
                return data[data['patientID'] == patient_id]
            return pd.DataFrame()  # Return empty DataFrame if no data found
        except Exception as e:
            print(f"Error getting patient appointments from {sheet_name}: {e}")
            return pd.DataFrame()
    
    def get_all_patients(self, sheet_name):
        try:
            data = self.read_data(sheet_name)
            if data is not None:
                return data
            return pd.DataFrame()  # Return empty DataFrame if no data found
        except Exception as e:
            print(f"Error getting all patients from {sheet_name}: {e}")
            return pd.DataFrame()
    
    def get_patient_checklist(self, sheet_name, patient_id):
        try:
            data = self.read_data(sheet_name)
            if data is not None:
                return data[data['patientID'] == patient_id]
            return pd.DataFrame()  # Return empty DataFrame if no data found
        except Exception as e:
            print(f"Error getting patient checklist from {sheet_name}: {e}")
            return pd.DataFrame()
    
    def get_patient_roster(self, sheet_name, patient_id):
        try:
            data = self.read_data(sheet_name)
            if data is not None:
                return data[data['patientID'] == patient_id]
            return pd.DataFrame()  # Return empty DataFrame if no data found
        except Exception as e:
            print(f"Error getting patient roster from {sheet_name}: {e}")
            return pd.DataFrame()
    
    def get_patient_alerts(self, sheet_name, patient_id):
        try:
            data = self.read_data(sheet_name)
            if data is not None:
                return data[data['patientID'] == patient_id]
            return pd.DataFrame()  # Return empty DataFrame if no data found
        except Exception as e:
            print(f"Error getting patient alerts from {sheet_name}: {e}")
            return pd.DataFrame()
    
    def get_patient_medications(self, sheet_name, patient_id):
        try:
            data = self.read_data(sheet_name)
            if data is not None:
                return data[data['patientID'] == patient_id]
            return pd.DataFrame()  # Return empty DataFrame if no data found
        except Exception as e:
            print(f"Error getting patient medications from {sheet_name}: {e}")
            return pd.DataFrame()
    
    def get_patient_history(self, sheet_name, patient_id):
        try:
            data = self.read_data(sheet_name)
            if data is not None:
                return data[data['patientID'] == patient_id]
            return pd.DataFrame()  # Return empty DataFrame if no data found
        except Exception as e:
            print(f"Error getting patient history from {sheet_name}: {e}")
            return pd.DataFrame()
    
    def get_patient_incidents(self, sheet_name, patient_id):
        try:
            data = self.read_data(sheet_name)
            if data is not None:
                return data[data['patientID'] == patient_id]
            return pd.DataFrame()  # Return empty DataFrame if no data found
        except Exception as e:
            print(f"Error getting patient incidents from {sheet_name}: {e}")
            return pd.DataFrame()