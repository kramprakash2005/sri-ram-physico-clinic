Sri Ram Physico Clinic - Management Software
1. Overview
This is a full-stack web application designed to streamline the daily operations of the Sri Ram Physico Clinic. The software provides a complete solution for patient registration, visit tracking, service management, billing, and reporting, all accessible through a clean, modern, and data-driven user interface.

2. Application Workflow
The application is designed to follow the natural workflow of a patient visiting the clinic:

Login: The user first logs in through a professional, secure login screen. The application is protected, and no page is accessible without a successful login.

Dashboard: After logging in, the user lands on an action-oriented dashboard that serves as a launchpad for the day's most common tasks.

Patient Arrival:

New Patient: If a new patient arrives, the user clicks "Manage Patients" -> "Add New Patient" and registers them by filling out the add-patient.html form.

Existing Patient: If an existing patient arrives, their visit is initiated from the dashboard by clicking "Create New Visit".

Create a Visit: On the "Create Visit" page, the user searches for the patient by name or contact number. Once found, they click "+ Add Visit" to open a popup where they enter the problem or reason for the visit.

Visit Tracking: The new visit automatically appears on the main visits.html page, which acts as a queue for all patients who have checked in for the day, displaying their arrival time.

Billing Process:

When a visit is created, a corresponding empty, unpaid bill is automatically generated in the backend.

The user navigates to the "Billing" page, which defaults to showing a list of all pending bills.

The user finds the patient's bill and clicks "

OpenBill
".

Manage Bill: On the manage-bill.html page, the user adds the specific treatments the patient received, adds any medical remarks, selects the payment method, and clicks "

Mark as Paid & Save
".

Completion: The bill is now marked as "Paid" and will appear in the "Today's Payments" tab on the billing page and in the final reports.

3. Features
Secure Authentication: A professional login system to protect application data.

Action-Oriented Dashboard: A clean "launchpad" to access the most common daily tasks.

Patient Management: Full CRUD (Create, Read, Update, Delete) functionality for patient records, including a detailed patient profile view with complete visit and billing history.

Service Management: Full CRUD functionality for managing the clinic's services and treatments.

Visit Management: A complete workflow for creating and viewing patient visits for the current day.

Billing Management: A comprehensive billing system to manage pending bills, add treatments, and track payments.

Reporting: A powerful reporting tool with a date range filter to generate detailed reports on payments, services, and new patients.

Professional UI: A consistent, clean, and modern user interface built with Bootstrap, featuring confirmation dialogs and a professional notification system.

4. Technology Stack
Backend: Python with the FastAPI framework.

Database: MongoDB (NoSQL).

Frontend: HTML, CSS, and modern JavaScript.

UI Framework: Bootstrap 5.

5. Database Design
The application uses MongoDB with a separate collections model, which is a direct adaptation of the original relational design. This provides a clean structure that is excellent for generating lists and reports.

Original Relational Design
Final MongoDB Schemas
counters: Tracks the next readable ID for patients, visits, and bills.

patients: Stores core patient information with a unique, readable patient_id.

visits: Stores visit details, linking to a patient via their ObjectId.

bills: Stores billing information, linking to a visit and containing snapshots of treatments.

treatments: A catalog of all services offered by the clinic.

6. Setup and Installation
Follow these steps to set up and run the project on a local machine.

Prerequisites
Python (version 3.8 or newer).

MongoDB installed and running on your local machine.

A web browser.

Step 1: Set Up the Project
Place the entire project folder (sri-ram-clinic-backend) in a desired location.

Open your terminal or command prompt and navigate into the project's root directory:

cd path/to/sri-ram-clinic-backend


Step 2: Create and Activate a Virtual Environment
# Create the virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate


Step 3: Install Dependencies
Install all the required Python libraries using the requirements.txt file.

pip install -r requirements.txt


Step 4: Set Up the MongoDB Database
Open the MongoDB shell (mongosh).

Create the database and the collections:

use sriRamPhysicoClinic
db.createCollection("patients")
db.createCollection("visits")
db.createCollection("bills")
db.createCollection("treatments")
db.createCollection("counters")


Initialize the counters for the readable IDs:

db.counters.insertMany([
  { "_id": "patients", "sequence_value": 0 },
  { "_id": "visits", "sequence_value": 0 },
  { "_id": "bills", "sequence_value": 0 }
])


Exit the MongoDB shell.

7. How to Run the Application
The application consists of two parts: the backend server and the frontend files.

Step 1: Run the Backend Server
In your terminal (make sure you are in the project's root directory, sri-ram-clinic-backend, and the virtual environment is active), run the following command:

uvicorn app.main:app --reload


The server is now running at http://127.0.0.1:8000. Keep this terminal window open.

Step 2: Open the Frontend Application
Navigate to the project folder in your file explorer.

Open the login.html file in your web browser.

The application is now ready to use.

Default Login Credentials
Username: admin

Password: password
(You can change these in the login.html file)

8. API Documentation
The FastAPI backend automatically generates interactive API documentation. You can access it at the following URL while the server is running:

https://www.google.com/search?q=http://127.0.0.1:8000/docs
