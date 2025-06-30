import pandas as pd

def log_incident(resident_id, incident_description):
    # TODO: Implement logging to Excel
    print(f"Logging incident for resident {resident_id}: {incident_description}")
    return True

def load_incidents():   
    try:
        df = pd.read_excel('incidents.xlsx', sheet_name='Incidents')
        return df
    except Exception as e:
        print(f"Error loading incidents: {e}")
        return pd.DataFrame(columns=['resident_id', 'incident_description', 'timestamp'])
    
def save_incidents(df):
    try:
        with pd.ExcelWriter('incidents.xlsx', engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, sheet_name='Incidents', index=False)
    except Exception as e:
        print(f"Error saving incidents: {e}")

def log_incident(resident_id, incident_description):
    df = load_incidents()
    new_incident = {
        'resident_id': resident_id,
        'incident_description': incident_description,
        'timestamp': pd.Timestamp.now()
    }
    df = df.append(new_incident, ignore_index=True)
    save_incidents(df)
    print(f"Incident logged for resident {resident_id}: {incident_description}")
    return True

# Example usage
if __name__ == "__main__":
    resident_id = 1
    incident_description = "Resident fell in the common area."
    if log_incident(resident_id, incident_description):
        print("Incident logged successfully.")
    else:
        print("Failed to log incident.")
# This code is a simplified version of the incident logging system.

