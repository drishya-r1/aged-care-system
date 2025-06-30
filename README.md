# Aged Care Assistance System

## Overview
The Aged Care Assistance System is designed to improve data management and emergency response in retirement facilities. This system utilizes a Python backend with Flask, a frontend built with HTML, CSS, and JavaScript, and Excel as the database for storing resident information and incident reports.

## Project Structure
```
aged-care-assistance-system
├── backend
│   ├── app.py
│   ├── database
│   │   └── excel_manager.py
│   ├── routes
│   │   └── emergency.py
│   └── requirements.txt
├── frontend
│   ├── index.html
│   ├── css
│   │   └── styles.css
│   └── js
│       └── main.js
├── data
│   └── residents.xlsx
└── README.md
```

## Features
- **Emergency Alerts**: Quickly log incidents and send alerts to nursing staff.
- **Resident Management**: Manage resident records, health information, and incident reports using an Excel database.
- **User-Friendly Interface**: A responsive frontend that allows easy interaction for staff members.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd aged-care-assistance-system
   ```

2. **Install Backend Dependencies**:
   Navigate to the `backend` directory and install the required packages:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Run the Backend**:
   Start the Flask application from the project root:
   ```bash
   python backend/app.py
   ```
   This will start the backend server (usually on `http://127.0.0.1:5000`).

4. **Open the Frontend**:
   - **Recommended:** From the `frontend` directory, start a simple HTTP server:
     ```bash
     python -m http.server 8000
     ```
     Then visit [http://localhost:8000](http://localhost:8000) in your browser.
   - **Alternatively:** Open `frontend/index.html` directly in a web browser (some features may not work due to browser security restrictions).

## Usage Guidelines
- Use the buttons on the frontend to log incidents or request assistance.
- Ensure that the `residents.xlsx` file is properly formatted to store resident data and incident reports.
- The frontend communicates with the backend for data operations; ensure both are running simultaneously.
- If you encounter CORS errors, enable CORS in the Flask backend (e.g., with `flask-cors`).

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.