import pandas as pd
from datetime import date
import os 

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data'))

def send_alert(nurse_id, alert_message):
    # TODO: Implement alert sending logic
    print(f"Sending alert to nurse {nurse_id}: {alert_message}")
    return True

def load_alerts():
    try:
        df = pd.read_excel('alerts.xlsx', sheet_name='Alerts')
        return df
    except Exception as e:
        print(f"Error loading alerts: {e}")
        return pd.DataFrame(columns=['nurse_id', 'alert_message', 'timestamp'])
    
def save_alerts(df):
    try:
        with pd.ExcelWriter('alerts.xlsx', engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, sheet_name='Alerts', index=False)
    except Exception as e:
        print(f"Error saving alerts: {e}")

def log_alert(nurse_id, alert_message):
    df = load_alerts()
    new_alert = {
        'nurse_id': nurse_id,
        'alert_message': alert_message,
        'timestamp': pd.Timestamp.now()
    }
    df = df.append(new_alert, ignore_index=True)
    save_alerts(df)
    send_alert(nurse_id, alert_message)
    return True

def add_alert(alert_data):
    file_path = os.path.join(DATA_DIR, 'alert.xlsx')
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        df = pd.concat([df, pd.DataFrame([alert_data])], ignore_index=True)
    else:
        df = pd.DataFrame([alert_data])
    df.to_excel(file_path, index=False)
    return True
# Example usage

if __name__ == "__main__":
    nurse_id = 1
    alert_message = "Patient needs immediate attention"
    if log_alert(nurse_id, alert_message):
        print("Alert logged successfully.")
    else:
        print("Failed to log alert.")
# This code is a simplified version of the alert management system.