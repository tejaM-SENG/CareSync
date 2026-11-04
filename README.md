# CareSync – Healthcare Management System

CareSync is a web-based Healthcare Management System developed using Python and Django. It provides a centralized platform for managing patients, doctors, appointments-related workflows, and healthcare administration through role-based dashboards.

## 🚀 Live Demo

**Live Application:** https://caresync-qcqh.onrender.com/

**GitHub Repository:** https://github.com/tejaM-SENG/CareSync

## 📌 Project Overview

CareSync is designed to simplify healthcare administration by providing separate interfaces and access permissions for administrators, staff members, and doctors.

The application allows administrators to manage doctors and patients, while approved doctors can access their assigned patient information through a dedicated dashboard.

## ✨ Key Features

- **Admin Dashboard:** Centralized interface for healthcare administration.
- **Doctor Management:** Add, view, update, and manage doctor records.
- **Doctor Registration:** Doctors can register and submit their information for approval.
- **Doctor Approval System:** Administrators can approve or reject doctor registrations.
- **Patient Management:** Register, view, and manage patient information.
- **Doctor Dashboard:** Dedicated dashboard for approved doctors.
- **Patient Assignment:** Manage doctor-to-patient assignments.
- **Role-Based Authentication:** Different access permissions for administrators, staff, and doctors.
- **REST API Integration:** Backend APIs for patient and doctor management.
- **Responsive Interface:** Bootstrap-based interface for different screen sizes.

## 🛠️ Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend Framework | Django |
| API Framework | Django REST Framework |
| Frontend | HTML, CSS, JavaScript |
| UI Framework | Bootstrap 5 |
| Database | SQLite3 |
| Authentication | Django Session Authentication |
| API Development | REST APIs |
| Deployment | Render |
| Version Control | Git & GitHub |

## 👥 User Roles

### 1. Administrator / Staff
- Access the administration dashboard.
- Manage doctor records.
- Manage patient records.
- Review doctor registrations.
- Approve or reject doctor applications.
- Assign patients to doctors.

### 2. Doctor
- Register through the doctor registration process.
- Access the system after approval.
- View the doctor dashboard.
- Access assigned patient information.
- View and manage permitted patient records.

## 🔐 Demo Login Credentials

Use the following accounts to explore the live application.

| User Role | Username | Password |
|---|---|---|
| Admin / Staff | demo@admin | demo@1234 |
| Doctor | demo@doctor | doct@1234 |

**Note:** Replace these placeholders with the actual demo accounts created in your deployed application. Do not publish your personal administrator password. Use dedicated demo accounts with sample data and restricted permissions.

## 📂 Project Structure

```text
CareSync/
│
├── healthcare/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── forms.py
│   ├── urls.py
│   ├── __init__.py
│   ├── apps.py
│   ├── middleware.py
│   ├── tests.py
│   └── admin.py
│
├── project_3/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│   └── healthcare/
│
├── screenshots/
│
├── static/
│   ├── css/
│   └── images/
│
├── manage.py
├── requirements.txt
├── db.sqlite3
└── README.md
```

*Note: Update the structure to reflect your actual repository.*

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/tejaM-SENG/CareSync.git
```

### 2. Navigate to the Project Directory

```bash
cd CareSync
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file based on `.env.example`.

Configure the required Django secret key and environment-specific settings.

Never commit actual secrets or database credentials to GitHub.

### 7. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Create an Administrator Account

```bash
python manage.py createsuperuser
```

### 9. Start the Development Server

```bash
python manage.py runserver
```

Open your browser:

http://127.0.0.1:8000/

## 🔗 API Endpoints

The application includes REST API functionality for healthcare data management.

| Endpoint | Description |
|---|---|
| `/api/` | API root |
| `/api/patients/` | Patient management API |
| `/api/doctors/` | Doctor management API |

## 🖥️ Application Screenshots

Screenshots will demonstrate the main application interfaces.

| Interface | Screenshot |
|---|---|
| Admin Dashboard | <img width="1876" height="804" alt="image" src="https://github.com/user-attachments/assets/bafc1e92-4d73-4e55-902c-201d6ef85a6d" /><img width="1870" height="708" alt="image" src="https://github.com/user-attachments/assets/84fdb79e-41a2-4d45-8093-c0752015efb3" /><img width="1888" height="516" alt="image" src="https://github.com/user-attachments/assets/7195f8cb-7b37-4cd7-9d1b-7c51b15192d4" /> |
| Doctor Dashboard | <img width="1870" height="826" alt="image" src="https://github.com/user-attachments/assets/3df546ce-1745-4699-9d9a-260cdcc6880e" /><img width="1864" height="564" alt="image" src="https://github.com/user-attachments/assets/43e18749-ecfb-410e-9609-30d7749b7d24" /><img width="1866" height="706" alt="image" src="https://github.com/user-attachments/assets/ef9627d0-ce25-4330-88ae-5818b570d880" /><img width="1872" height="700" alt="image" src="https://github.com/user-attachments/assets/ffd94724-fba1-4813-9f9e-7a46b0afea78" /> |
| Patient Management | <img width="1858" height="826" alt="image" src="https://github.com/user-attachments/assets/e1d08d35-ab88-4f3d-a86b-ef94b5da5408" /><img width="1872" height="664" alt="image" src="https://github.com/user-attachments/assets/e399c279-d7ea-4c75-b364-b1cf5506f513" /><img width="1872" height="706" alt="image" src="https://github.com/user-attachments/assets/8673f10b-5f12-483f-87f4-79dd7410d7d0" /> |
| Doctor Management | <img width="1856" height="798" alt="image" src="https://github.com/user-attachments/assets/1a09ea43-4dbd-4b2b-bfe9-f2b33a4784b1" /><img width="1822" height="702" alt="image" src="https://github.com/user-attachments/assets/5436e36d-baf8-47fb-91c1-2be1b423a1f0" /><img width="1866" height="710" alt="image" src="https://github.com/user-attachments/assets/d56bff71-bfa5-47b5-ae3a-49009645def6" /><img width="1876" height="706" alt="image" src="https://github.com/user-attachments/assets/cb12505d-905d-440a-ac74-2ea2ea30a3fd" /> |
| Login Page | <img width="1880" height="822" alt="image" src="https://github.com/user-attachments/assets/0c082f22-bdab-470e-9362-ca57e5f4cbc8" /><img width="1872" height="706" alt="image" src="https://github.com/user-attachments/assets/9024bfc4-bb01-4176-b9c8-7c26efbc7d04" /> |

## ☁️ Deployment

CareSync is deployed using Render.

Deployment process:

1. Push the source code to GitHub.
2. Connect the repository to Render.
3. Configure the Python environment.
4. Install dependencies using `requirements.txt`.
5. Configure environment variables.
6. Apply database migrations.
7. Configure static files and database settings.
8. Deploy the application.

**Live URL:** https://caresync-qcqh.onrender.com/

## 🎯 Project Objectives

- Develop a centralized healthcare management platform.
- Simplify doctor and patient administration.
- Implement role-based authentication and authorization.
- Build REST APIs using Django REST Framework.
- Implement doctor registration and approval workflows.
- Develop responsive dashboards using Bootstrap.
- Gain practical experience in full-stack development and cloud deployment.

## 👨‍💻 Developer

**Teja Muddangula**

Python Full-Stack Developer

- GitHub: https://github.com/tejaM-SENG
- LinkedIn: https://linkedin.com/in/teja-muddangula-38a92a218

---

*Developed as a Python Full-Stack Web Development project.*
