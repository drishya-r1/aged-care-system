import pandas as pd
from datetime import date
import datetime
import os
import hashlib

class ExcelManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_data(self, sheet_name):
        try:
            data = pd.read_excel(self.file_path, sheet_name=sheet_name)
            return data
        except Exception as e:
            print(f"Error reading {sheet_name}: {e}")
            return None
        
USERS_FILE = 'data/users.xlsx'
USER_COLUMNS = [
    'name', 'usertype', 'username', 'password', 'age', 'unit', 'mobile_number',
    'email','experience', 'qualifications','immediate_family_name', 'immediate_family_relation', 'immediate_family_contact_no'
]

def ensure_users_file_dir():
    dir_path = os.path.dirname(os.path.abspath(USERS_FILE))
    print(f"Ensuring directory exists: {dir_path}")
    if not os.path.exists(dir_path):
        print(f"Creating directory: {dir_path}")
        os.makedirs(dir_path)

def load_data():
    ensure_users_file_dir()
    if os.path.exists(USERS_FILE):
        print(f"Loading data from {USERS_FILE}")
        df = pd.read_excel(USERS_FILE)
        print(df[['username', 'password']])
        return pd.read_excel(USERS_FILE)
    else:
        print(f"Loading data from {USERS_FILE}")
        print(f"{USERS_FILE} does not exist. Creating an empty DataFrame.")
        return pd.DataFrame(columns=USER_COLUMNS)

def save_data(df):
    df.to_excel(USERS_FILE, index=False)

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def add_user(user_data):
    # Hash the password before storing
    if 'password' in user_data:
        user_data['password'] = hash_password(user_data['password'])
    file_path = os.path.join(DATA_DIR, 'users.xlsx')
    df = pd.read_excel(file_path) if os.path.exists(file_path) else pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([user_data])], ignore_index=True)
    df.to_excel(file_path, index=False)

def add_resident(resident_data):
    file_path = os.path.join(DATA_DIR, 'residents.xlsx')
    df = pd.read_excel(file_path) if os.path.exists(file_path) else pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([resident_data])], ignore_index=True)
    df.to_excel(file_path, index=False)

def add_nurse(nurse_data):
    file_path = os.path.join(DATA_DIR, 'nurses.xlsx')
    df = pd.read_excel(file_path) if os.path.exists(file_path) else pd.DataFrame()
    df = df.append(nurse_data, ignore_index=True)
    df.to_excel(file_path, index=False)

def update_logged_in_status(userid, status):
    file_path = os.path.join(DATA_DIR, 'users.xlsx')
    if not os.path.exists(file_path):
        return False
    df = pd.read_excel(file_path)
    df.loc[df['userid'].astype(str) == str(userid), 'logged_in_status'] = status
    df.to_excel(file_path, index=False)
    return True

def delete_user(username):
    df = load_data()
    df = df[df['username'] != username]
    save_data(df)

def update_user(username, updated_data):
    df = load_data()
    idx = df.index[df['username'] == username]
    if not idx.empty:
        for key, value in updated_data.items():
            df.at[idx[0], key] = value
        save_data(df)
        return True
    return False

def search_user(username):
    df = load_data()
    result = df[df['username'] == username]
    if not result.empty:
        return result.to_dict(orient='records')[0]
    return None

def get_accounts():
    df = load_data()
    print(df[['username', 'password']])
    return dict(zip(df['username'], df['password']))

def get_user_profiles():
    df = load_data()
    print(df[['username', 'password']])
    return df.set_index('username').to_dict(orient='index')

def login(username, password):
    accounts = get_accounts()
    user_profiles = get_user_profiles()
    hashed_password = hash_password(password)
    if username in accounts and accounts[username] == hashed_password:
        user = user_profiles.get(username, {})
        if user:
            # Return username, usertype, and userid (if present)
            return {
                "username": username,
                "usertype": user.get("usertype"),
                "userid": user.get("userid")
            }
        else:
            return None
    else:
        return None

def access_home_page(username, password):
    accounts = get_accounts()
    user_profiles = get_user_profiles()
    if username in accounts and accounts is not None:
        if accounts[username] == password:
            return user_profiles.get(username, {})
        else:
            return "Invalid password. Please try again."
    else:
        return "Unauthorized access as a resident. Please return to the login page."


    def write_data(self, sheet_name, data_frame):
        try:
            with pd.ExcelWriter(self.file_path, engine='openpyxl', mode='a') as writer:
                data_frame.to_excel(writer, sheet_name=sheet_name, index=False)
        except Exception as e:
            print(f"Error writing to {sheet_name}: {e}")

    def update_data(self, sheet_name, data_frame):
        try:
            existing_data = self.read_data(sheet_name)
            if existing_data is not None:
                updated_data = pd.concat([existing_data, data_frame]).drop_duplicates().reset_index(drop=True)
                self.write_data(sheet_name, updated_data)
        except Exception as e:
            print(f"Error updating {sheet_name}: {e}")

    def delete_data(self, sheet_name, condition):
        try:
            data = self.read_data(sheet_name)
            if data is not None:
                filtered_data = data.query(condition)
                self.write_data(sheet_name, filtered_data)
        except Exception as e:
            print(f"Error deleting from {sheet_name}: {e}")

    def get_today_data(self, sheet_name):  
        try:
            data = self.read_data(sheet_name)
            if data is not None:
                today = date.today().strftime('%Y-%m-%d')
                return data[data['date'] == today]
            return None
        except Exception as e:
            print(f"Error getting today's data from {sheet_name}: {e}")
            return None 
    
    def get_all_data(self, sheet_name):
        try:
            data = self.read_data(sheet_name)
            if data is not None:
                return data
            return None
        except Exception as e:
            print(f"Error getting all data from {sheet_name}: {e}")
            return None
    
    def save_data(self, sheet_name, data_frame):
        try:
            self.write_data(sheet_name, data_frame)
        except Exception as e:
            print(f"Error saving data to {sheet_name}: {e}")
    
    def load_data(self, sheet_name):
        try:
            data = self.read_data(sheet_name)
            if data is not None:
                return data
            return pd.DataFrame()  # Return empty DataFrame if no data found
        except Exception as e:
            print(f"Error loading data from {sheet_name}: {e}")
            return pd.DataFrame()
    
    def save_to_excel(self, data_frame, sheet_name):
        try:
            with pd.ExcelWriter(self.file_path, engine='openpyxl', mode='a') as writer:
                data_frame.to_excel(writer, sheet_name=sheet_name, index=False)
        except Exception as e:
            print(f"Error saving to {sheet_name}: {e}")
    
    def load_from_excel(self, sheet_name):
        try:
            data = pd.read_excel(self.file_path, sheet_name=sheet_name)
            return data
        except Exception as e:
            print(f"Error loading from {sheet_name}: {e}")
            return pd.DataFrame()
    
    def delete_row(self, sheet_name, condition):
        try:
            data = self.read_data(sheet_name)
            if data is not None:
                filtered_data = data.query(condition)
                self.write_data(sheet_name, filtered_data)
        except Exception as e:
            print(f"Error deleting row from {sheet_name}: {e}")

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data'))

def read_all_rows(file_name):
    """Read all rows from the Excel file."""
    file_path = os.path.join(DATA_DIR, file_name)
    if os.path.exists(file_path):
        return pd.read_excel(file_path).to_dict(orient='records')
    else:
        return []

def read_record_by_id(file_name, id_column, id_value):
    """Read a single record by its ID."""
    file_path = os.path.join(DATA_DIR, file_name)
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        record = df[df[id_column] == id_value]
        if not record.empty:
            return record.iloc[0].to_dict()
    return None

def delete_record_by_id(file_name, id_column, id_value):
    """Delete a record by its ID."""
    file_path = os.path.join(DATA_DIR, file_name)
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        new_df = df[df[id_column] != id_value]
        new_df.to_excel(file_path, index=False)
        return True
    return False

def get_records_by_column(file_name, column, value):
    """Get all records where column == value."""
    file_path = os.path.join(DATA_DIR, file_name)
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        filtered = df[df[column] == value]
        return filtered.to_dict(orient='records')
    return []

def add_record(file_name, record_dict):
    """Add a new record to the Excel file."""
    file_path = os.path.join(DATA_DIR, file_name)
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        df = pd.concat([df, pd.DataFrame([record_dict])], ignore_index=True)
    else:
        df = pd.DataFrame([record_dict])
    df.to_excel(file_path, index=False)
    return True

def update_record_by_id(file_name, id_column, id_value, update_dict):
    file_path = os.path.join(DATA_DIR, file_name)
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip()  # Remove leading/trailing spaces
        print("Columns in DataFrame:", df.columns.tolist())  # Debug
        mask = df[id_column].astype(str) == str(id_value)
        if mask.any():
            for key, value in update_dict.items():
                if key in df.columns:
                    df.loc[mask, key] = value
                else:
                    print(f"Column '{key}' not found in DataFrame.")
            df.to_excel(file_path, index=False)
            return True
        else:
            print(f"No matching record for {id_column} == {id_value}")
    else:
        print(f"File {file_path} does not exist.")
    return False

def read_all_food_items():
    file_path = os.path.join(DATA_DIR, 'ondemand_food_menu.xlsx')
    if os.path.exists(file_path):
        return pd.read_excel(file_path).to_dict(orient='records')
    else:
        return []

def add_food_alert(alert_data):
    file_path = os.path.join(DATA_DIR, 'food_alerts.xlsx')
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        df = pd.concat([df, pd.DataFrame([alert_data])], ignore_index=True)
    else:
        df = pd.DataFrame([alert_data])
    df.to_excel(file_path, index=False)
    return True
# Example usage:
# add_record('residents.xlsx', {'resident_id': 4, 'first_name': 'Bob', 'last_name': 'Lee', 'room_number': '104', 'date_of_birth': '1945-09-10', 'dietary_notes': 'Vegan'})
# update_record_by_id('residents.xlsx', 'resident_id', 4, {'dietary_notes': 'Vegan, Gluten-Free'})
def read_all_events():
    file_path = os.path.join(DATA_DIR, 'events.xlsx')
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        def convert_value(val):
            if isinstance(val, (datetime.datetime, datetime.date, datetime.time)):
                return str(val)
            return val
        records = df.map(convert_value).to_dict(orient='records')
        return records
    else:
        return []

def add_event(event_data):
    file_path = os.path.join(DATA_DIR, 'events.xlsx')
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        df = pd.concat([df, pd.DataFrame([event_data])], ignore_index=True)
    else:
        df = pd.DataFrame([event_data])
    df.to_excel(file_path, index=False)
    return True

def modify_event(event_id, updated_data):
    file_path = os.path.join(DATA_DIR, 'events.xlsx')
    if not os.path.exists(file_path):
        return False
    df = pd.read_excel(file_path)
    df.loc[df['event_id'] == event_id, list(updated_data.keys())] = list(updated_data.values())
    df.to_excel(file_path, index=False)
    return True

def delete_event(event_id):
    file_path = os.path.join(DATA_DIR, 'events.xlsx')
    if not os.path.exists(file_path):
        return False
    df = pd.read_excel(file_path)
    df = df[df['event_id'] != event_id]
    df.to_excel(file_path, index=False)
    return True

def read_all_alerts():
    file_path = os.path.join(DATA_DIR, 'alert.xlsx')

    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        # print df for debugging
        print(df.head())
        df.columns = df.columns.str.strip()
        return df.fillna('').to_dict(orient='records')
    return []

def read_all_food_alerts():
    file_path = os.path.join(DATA_DIR, 'food_alerts.xlsx')
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip()
        return df.fillna('').to_dict(orient='records')
    return []

def update_alert_status(alert_id, new_status):
    file_path = os.path.join(DATA_DIR, 'alert.xlsx')
    if not os.path.exists(file_path):
        return False
    df = pd.read_excel(file_path)
    # Ensure comparison is done as string to avoid type mismatch
    df.loc[df['alert_id'].astype(str) == str(alert_id), 'status'] = new_status
    df.to_excel(file_path, index=False)
    return True

def update_food_alert_status(alert_id, new_status):
    file_path = os.path.join(DATA_DIR, 'food_alerts.xlsx')
    if not os.path.exists(file_path):
        return False
    df = pd.read_excel(file_path)
    # Ensure comparison is done as string to avoid type mismatch
    df.loc[df['alert_id'].astype(str) == str(alert_id), 'status'] = new_status
    df.to_excel(file_path, index=False)
    return True

def read_all_nurses():
    file_path = os.path.join(DATA_DIR, 'nurses.xlsx')
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip()
        # Format date_of_birth as DD/MM/YYYY if the column exists
        if 'DOB' in df.columns:
            df['DOB'] = pd.to_datetime(df['DOB'], errors='coerce').dt.strftime('%d/%m/%Y')
            df['DOB'] = df['DOB'].fillna('')
        return df.fillna('').to_dict(orient='records')
    return []

def read_all_residents():
    file_path = os.path.join(DATA_DIR, 'residents.xlsx')
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip()
        if 'date_of_birth' in df.columns:
            df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce').dt.strftime('%d/%m/%Y')
            df['date_of_birth'] = df['date_of_birth'].fillna('')
        return df.fillna('').to_dict(orient='records')
    return []
def reset_user_password_by_username(username, new_password):
    file_path = os.path.join(DATA_DIR, 'users.xlsx')
    if not os.path.exists(file_path):
        return False
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()
    mask = df['username'].astype(str) == str(username)
    if mask.any():
        df.loc[mask, 'password'] = hash_password(new_password)
        df.to_excel(file_path, index=False)
        return True
    return False
# --- Add initial users if running as script ---
if __name__ == "__main__":
    # Add resident users
    add_user({
        'name': 'Karen Almond',
        'usertype': 'resident',
        'username': 'resident1',
        'password': 'resident1pass',
        'age': '76',
        'unit': '101A',
        'mobile_number': '1010102987',
        'email': None,
        'experience': None,
        'qualifications': None,
        'immediate_family_name': 'John Almond',
        'immediate_family_relation': 'Relative1',
        'immediate_family_contact_no': '123-456-7890'
    })

    add_user({
        'name': 'Theodore Phillips',
        'usertype': 'resident',
        'username': 'resident2',
        'password': 'resident2pass',
        'age': '88',
        'unit': '102B',
        'mobile_number': '2011123456',
        'email': None,
        'experience': None,
        'qualifications': None,
        'immediate_family_name': 'Alice Phillips',
        'immediate_family_relation': 'Relative1',
        'immediate_family_contact_no': '234-567-8901'
    })

    add_user({
        'name': 'Alexandria Graham',
        'usertype': 'resident',
        'username': 'resident3',
        'password': 'resident3pass',
        'age': '72',
        'unit': '103A',
        'mobile_number': '98765432000',
        'email': None,
        'experience': None,
        'qualifications': None,
        'immediate_family_name': 'Charlie Graham',
        'immediate_family_relation': 'Relative1',
        'immediate_family_contact_no': '345-678-9012'
    })

    # Add nurse users
    add_user({
        'name': 'Judy Duke',
        'usertype': 'nurse',
        'username': 'nurse1',
        'password': 'nurse1pass',
        'age': '35',
        'unit': None,
        'mobile_number': '1112223333',
        'email': 'judy.duke@example.com',
        'experience': '10 years',
        'qualifications': 'RN',
        'immediate_family_name': '',
        'immediate_family_relation': '',
        'immediate_family_contact_no': ''
    })

    add_user({
        'name': 'Pete Will',
        'usertype': 'nurse',
        'username': 'nurse2',
        'password': 'nurse2pass',
        'age': '40',
        'unit': None,
        'mobile_number': '2223334444',
        'email': 'pete.will@example.com',
        'experience': '12 years',
        'qualifications': 'BSN',
        'immediate_family_name': '',
        'immediate_family_relation': '',
        'immediate_family_contact_no': ''
    })

    add_user({
        'name': 'Ellen Micky',
        'usertype': 'nurse',
        'username': 'nurse3',
        'password': 'nurse3pass',
        'age': '29',
        'unit': None,
        'mobile_number': '3334445555',
        'email': 'ellen.micky@example.com',
        'experience': '6 years',
        'qualifications': 'MSN',
        'immediate_family_name': '',
        'immediate_family_relation': '',
        'immediate_family_contact_no': ''
    })
