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
│   │   ├── admin
│   │   │   └── admin.py
│   │   ├── nurses
│   │   │   └── nurseportal.py
│   │   └── residents
│   │       ├── emergency.py
│   │       ├── food_requests.py
│   │       └── resident_details.py
│   └── requirements.txt
├── frontend
│   ├── html
│   │   ├── admin.html
│   │   ├── login.html
│   │   ├── nurseportaltwo.html
│   │   ├── ondemand_food.html
│   │   └── residents_index.html
│   ├── css
│   │   └── styles.css
│   └── js
│       ├── main.js
│       ├── login_hash.js
│       ├── admin_alerts.js
│       └── alerts_analytics.js
├── data
│   ├── residents.xlsx
│   ├── nurses.xlsx
│   ├── users.xlsx
│   ├── alerts.xlsx
│   ├── food_alerts.xlsx
│   └── feedback.xlsx
└── README.md
```

## Features
- **Emergency Alerts**: Quickly log incidents and send alerts to nursing staff for rapid response.
- **Resident Management**: Onboard, search, view, and edit resident records, health information, and incident reports using an Excel database.
- **Nurse Management**: Onboard, search, view, and edit nurse records and unit allocations.
- **Food Requests**: Residents can request on-demand food; nurses can view and serve food requests.
- **User Management**: Admins can manage user accounts, reset passwords, and activate/deactivate users.
- **Data Backup**: Admins can back up all system data to an AWS S3 bucket with a single click.
- **Analytics & Reporting**: View statistics and analytics on alerts, food requests, and system usage.
- **Resident Feedback**: Collect and review feedback from residents for continuous improvement.
- **User-Friendly Interface**: Responsive frontend for easy interaction by staff, nurses, and admins.

## Setup Instructions
Pre-requisites:
- Python 3.x installed
- Flask installed (`pip install Flask`)

1. **Clone the Repository to a folder in your local machine**:
   ```bash
   git clone https://github.com/drishya-r1/aged-care-system.git
   cd aged-care-system
   ```
2. **Install Backend Dependencies**:
   Navigate to the `backend` directory and install the required packages:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

   ```

3. **Install Backend Dependencies**:
   Install the required packages:
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Run the Backend**:
   Start the Flask application from the project root:
   ```bash
   python3 -m backend.app
   ```
   This will start the backend and frontend server (usually on `http://127.0.0.1:5000`).
   Then visit [http://127.0.0.1:5000](http://127.0.0.1:5000)  in your browser.

## System Usage

### Admin
- Log in with your admin credentials.
- Use the sidebar to onboard residents and nurses, search/edit records, reset passwords, view alerts, review feedback, and perform data backup to AWS S3.
- Use the Analytics section to view system statistics and reports.

### Nurse
- Log in with your nurse credentials.
- View and attend to emergency alerts and food requests for your assigned units.
- Update alert statuses as you respond to requests.

### Resident
- Log in with your resident credentials.
- Request food on demand and submit feedback.
- View your own information and request assistance as needed.

All actions are performed through a user-friendly web interface accessible via your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## System Flowchart

```mermaid
flowchart TD
    Start([Start])
    Login[User Login]
    Decision{User Type?}
    Admin[Admin Portal]
    Nurse[Nurse Portal]
    Resident[Resident Portal]
    End([End])

    Start --> Login --> Decision
    Decision -- Admin --> Admin
    Decision -- Nurse --> Nurse
    Decision -- Resident --> Resident
    Admin --> End
    Nurse --> End
    Resident --> End
```

## Detailed System Flowchart for Admin Actions

```mermaid
flowchart TD
    subgraph ExcelDB[Excel Data Store]
        excel1[(Residents.xlsx)]
        excel2[(Nurses.xlsx)]
        excel3[(Users.xlsx)]
        excel4[(Alerts.xlsx)]
        excel5[(Food_Alerts.xlsx)]
        excel6[(Feedback.xlsx)]
    end
    subgraph Cloud[Cloud: AWS S3]
        cloud1((Backup))
    end
    A([fa:fa-user Admin logs in]) --> B{Select Menu Option}
    B -- Resident Onboarding --> C([fa:fa-keyboard-o Fill Resident Details])
    C --> D([fa:fa-sign-in Submit])
    D --> excel1
    D --> excel3
    D --> E([fa:fa-desktop Resident Added Display])
    B -- Nurse Onboarding --> F([fa:fa-keyboard-o Fill Nurse Details])
    F --> G([fa:fa-sign-in Submit])
    G --> excel2
    G --> excel3
    G --> H([fa:fa-desktop Nurse Added Display])
    B -- Search/Edit Resident --> I([fa:fa-keyboard-o Search Resident])
    I --> excel1
    excel1 --> J{Resident Found?}
    J -- Yes --> K([fa:fa-keyboard-o Edit Details])
    K --> L([fa:fa-sign-in Save Changes])
    L --> excel1
    L --> M([fa:fa-desktop Resident Updated Display])
    J -- No --> N([fa:fa-desktop Show Not Found])
    B -- Search/Edit Nurse --> O([fa:fa-keyboard-o Search Nurse])
    O --> excel2
    excel2 --> P{Nurse Found?}
    P -- Yes --> Q([fa:fa-keyboard-o Edit Details])
    Q --> R([fa:fa-sign-in Save Changes])
    R --> excel2
    R --> S([fa:fa-desktop Nurse Updated Display])
    P -- No --> T([fa:fa-desktop Show Not Found])
    B -- Reset Password --> U([fa:fa-keyboard-o Enter Username])
    U --> V([fa:fa-sign-in Reset Password])
    V --> excel3
    V --> W([fa:fa-desktop Show Temp Password])
    B -- Alerts --> X([fa:fa-desktop View Alerts])
    X --> excel4
    X --> Y([fa:fa-desktop Take Action])
    B -- Feedback --> Z([fa:fa-desktop View Feedback])
    Z --> excel6
    B -- Data Backup --> AA([fa:fa-cloud Click Backup Button])
    AA --> cloud1
    cloud1 --> AB([fa:fa-desktop Show Success/Failure])
    B -- Analytics --> AD([fa:fa-desktop View Analytics])
    AD --> excel4
    AD --> excel5
```

## Decision Tree (User Actions)

```mermaid
graph TD
    A[User logs in] --> B{User type}
    B -- Admin --> C[Show admin menu]
    C --> D[Onboard Resident/Nurse]
    C --> E[Search/Edit Resident/Nurse]
    C --> F[View Alerts/Feedback]
    C --> G[Backup Data]
    C --> H[View Analytics]
    B -- Nurse --> I[Show nurse dashboard]
    I --> J[View/respond to alerts]
    I --> K[View/respond to food requests]
    B -- Resident --> L[Show resident dashboard]
    L --> M[Request food]
    L --> N[Submit feedback]
    L --> O[Request assistance]
```
