# 🏥 Sri Ram Physico Clinic - Management Software

## 1. Overview
This is a **full-stack web application** designed to streamline the daily operations of the **Sri Ram Physico Clinic**.  
The software provides a complete solution for:

- 🧾 Patient registration  
- 📅 Visit tracking  
- 💊 Service management  
- 💰 Billing and reporting  

All accessible through a **clean, modern, and data-driven user interface**.

---

## 2. Application Workflow

The application follows the natural workflow of a patient visiting the clinic:

### 🔐 Login
- The user logs in through a professional, secure login screen.  
- No page is accessible without successful authentication.

### 🏠 Dashboard
- After logging in, the user lands on an **action-oriented dashboard** serving as a launchpad for the day’s common tasks.

### 👩‍⚕️ Patient Arrival
#### New Patient
- Click **“Manage Patients” → “Add New Patient”**  
- Register the patient using the `add-patient.html` form.

#### Existing Patient
- For returning patients, create a visit from the dashboard by clicking **“Create New Visit”**.

### 📋 Create a Visit
- On the **Create Visit** page:
  - Search the patient by name or contact number.
  - Click **“+ Add Visit”** to open a popup and enter the problem or reason for the visit.

- The visit then appears on the **visits.html** page — acting as a queue for all patients checked in for the day, showing their arrival time.

### 💳 Billing Process
1. When a visit is created, a corresponding **empty, unpaid bill** is auto-generated.
2. Navigate to the **Billing** page to view all pending bills.
3. Click **[Open Bill]** for the specific patient.
4. On the **manage-bill.html** page:
   - Add treatments received
   - Add medical remarks
   - Select payment method
   - Click **[Mark as Paid & Save]**
5. The bill is now marked **Paid** and appears under:
   - **Today’s Payments**
   - **Final Reports**

### UI DEMO 
(https://kramprakash2005.github.io/clinic.github.io/login.html)[click here]
Sample UserName: admin
Sample Password: password
---

## 3. Features

✅ **Secure Authentication** – Professional login system to protect data.  
✅ **Action-Oriented Dashboard** – Quick access to common daily tasks.  
✅ **Patient Management** – Full CRUD functionality with detailed profiles and billing history.  
✅ **Service Management** – Manage all clinic services and treatments (CRUD).  
✅ **Visit Management** – Track and manage all patient visits for the day.  
✅ **Billing Management** – Add treatments, track payments, and manage pending bills.  
✅ **Reporting** – Filterable date-range reports for payments, services, and new patients.  
✅ **Professional UI** – Built with **Bootstrap 5**, includes confirmation dialogs & notifications.

---

## 4. Technology Stack

| Component | Technology |
|------------|-------------|
| **Backend** | Python (FastAPI) |
| **Database** | MongoDB (NoSQL) |
| **Frontend** | HTML, CSS, JavaScript |
| **UI Framework** | Bootstrap 5 |

---

## 5. Database Design

The application uses **MongoDB** with separate collections, mirroring a relational design for clarity and reporting efficiency.

### 🗂 Collections

| Collection | Description |
|-------------|--------------|
| **counters** | Tracks next readable ID for patients, visits, and bills |
| **patients** | Stores patient info with a unique `patient_id` |
| **visits** | Stores visit details linked to a patient |
| **bills** | Stores billing info linked to visits, with treatment snapshots |
| **treatments** | Catalog of all clinic services |

### 🧩 Initialization
```js
use sriRamPhysicoClinic
db.createCollection("patients")
db.createCollection("visits")
db.createCollection("bills")
db.createCollection("treatments")
db.createCollection("counters")

db.counters.insertMany([
  { "_id": "patients", "sequence_value": 0 },
  { "_id": "visits", "sequence_value": 0 },
  { "_id": "bills", "sequence_value": 0 }
])
```

---

## 6. Setup and Installation

### 🧱 Prerequisites
- Python **3.8+**
- MongoDB installed & running
- Web browser

### ⚙️ Step 1: Set Up the Project
```bash
cd path/to/sri-ram-physico-clinic
```

### 🐍 Step 2: Create and Activate Virtual Environment
```bash
# Create
python -m venv venv

# Activate
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 📦 Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### 🗃 Step 4: Set Up MongoDB
Run Mongo shell:
```bash
mongosh
```

Then execute:
```js
use sriRamPhysicoClinic
db.createCollection("patients")
db.createCollection("visits")
db.createCollection("bills")
db.createCollection("treatments")
db.createCollection("counters")

db.counters.insertMany([
  { "_id": "patients", "sequence_value": 0 },
  { "_id": "visits", "sequence_value": 0 },
  { "_id": "bills", "sequence_value": 0 }
])
```

Exit the shell after completion.

---

## 7. Running the Application

The system has two parts:
- 🖥 Backend (FastAPI)
- 🌐 Frontend (HTML files)

### ▶️ Step 1: Start the Backend
```bash
uvicorn app.main:app --reload
```

Server will run at:  
👉 **http://127.0.0.1:8000**

### 🌍 Step 2: Open Frontend
1. Go to your project folder.  
2. Open **login.html** in your browser.

---

### 🔑 Default Login Credentials
| Field | Value |
|--------|--------|
| **Username** | `admin` |
| **Password** | `password` |

*(You can change these in `login.html`)*

---

## 8. API Documentation

The FastAPI backend automatically generates interactive API docs.

Access it at:  
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### 🧠 Author
**Sri Ram Physico Clinic Management Software**  
Developed for streamlining clinical operations using FastAPI + MongoDB + Bootstrap.

---
