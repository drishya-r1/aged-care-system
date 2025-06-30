import pandas as pd
import os

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
    """Update a record by its ID."""
    file_path = os.path.join(DATA_DIR, file_name)
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        mask = df[id_column] == id_value
        if mask.any():
            for key, value in update_dict.items():
                df.loc[mask, key] = value
            df.to_excel(file_path, index=False)
            return True
    return False

# Example usage:
# add_record('residents.xlsx', {'resident_id': 4, 'first_name': 'Bob', 'last_name': 'Lee', 'room_number': '104', 'date_of_birth': '1945-09-10', 'dietary_notes': 'Vegan'})
# update_record_by_id('residents.xlsx', 'resident_id', 4, {'dietary_notes': 'Vegan, Gluten-Free'})