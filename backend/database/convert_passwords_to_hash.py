import pandas as pd
import hashlib
import os

USERS_FILE = os.path.join(os.path.dirname(__file__), '../../data/users.xlsx')

def is_sha256(s):
    return isinstance(s, str) and len(s) == 64 and all(c in '0123456789abcdef' for c in s.lower())

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def convert_passwords_to_hash():
    df = pd.read_excel(USERS_FILE)
    if 'password' not in df.columns:
        print('No password column found.')
        return
    changed = False
    for idx, row in df.iterrows():
        pwd = row['password']
        if not is_sha256(str(pwd)):
            df.at[idx, 'password'] = hash_password(str(pwd))
            changed = True
    if changed:
        df.to_excel(USERS_FILE, index=False)
        print('Passwords converted to SHA-256 hashes.')
    else:
        print('All passwords already hashed.')

if __name__ == '__main__':
    convert_passwords_to_hash()
