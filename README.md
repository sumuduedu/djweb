**# 📘 MIT TMS – Training Management System

## 📌 Overview

The **MIT Training Management System (MIT TMS)** is a web-based application developed using Django to manage vocational and academic training processes. It supports course management, student enrollment, scheduling, and performance tracking in a centralized platform.

---

## 🎯 Objectives

- Centralize training and academic management
- Improve student performance tracking
- Automate administrative workflows
- Provide role-based dashboards
- Enable structured course and batch management
- Support data-driven decision-making

---

## 🏗️ System Architecture

### 🔧 Technology Stack

| Component   | Technology |
|------------|-----------|
| Backend     | Django (Python) |
| Frontend    | HTML, Tailwind CSS, Alpine.js, HTMX |
| Database    | SQLite (default) / PostgreSQL / MySQL |
| Server      | Gunicorn / Django Dev Server |
| Environment | Python Virtual Environment |

---

## 📁 Project Structure
**
## 📁 Project Structure

```
mit_tms/
│
├── manage.py
├── mit_tms/              # Core project settings
│
├── apps/
│   ├── accounts/        # Authentication & user management
│   ├── courses/         # Course and module management
│   ├── batch/           # Batch management
│   ├── enrollment/      # Enrollment handling
│   ├── scheduling/      # Timetable & sessions
│   ├── core/            # Shared utilities
│   ├── website/         # Public-facing pages
│
├── templates/           # HTML templates
├── static/              # CSS, JS, assets
├── media/               # Uploaded files
├── db.sqlite3           # Database
├── requirements.txt     # Dependencies
└── .env                 # Environment variables
```
---

## 🔐 User Roles

### 👑 Admin
- Full system control
- Manage users, courses, batches, and reports

### 👨‍🏫 Instructor
- Manage courses and sessions
- Monitor student progress
- Conduct assessments

### 🎓 Student
- View enrolled courses
- Access schedules
- Track performance

---

## ⚙️ Core Modules

### 🔑 Accounts (`apps/accounts`)
- Authentication (login/logout)
- Profile management
- Role-based access control

---

### 📚 Courses (`apps/courses`)
- Course creation and management
- Module and task structuring

---

### 👥 Batch (`apps/batch`)
- Group students into batches
- Assign instructors

---

### 📝 Enrollment (`apps/enrollment`)
- Student enrollment tracking
- Status management

---

### 📅 Scheduling (`apps/scheduling`)
- Session planning
- Timetable management

---

### 🧩 Core (`apps/core`)
- Shared utilities
- Base models and helpers

---

### 🌐 Website (`apps/website`)
- Public pages
- Landing pages

---

## 📊 Key Features

- ✅ Course & module management  
- ✅ Student enrollment system  
- ✅ Batch management  
- ✅ Scheduling & timetables  
- ✅ Role-based dashboards  
- ✅ Interactive UI (HTMX + Alpine.js)  
- ✅ Modern UI (Tailwind CSS)  

---

## 🗄️ Database Design (High-Level)

**Main Entities:**
- User
- Profile (Student/Instructor)
- Course
- Module
- Task
- Batch
- Enrollment
- Schedule

**Relationships:**
- One Course → Many Modules  
- One Module → Many Tasks  
- One Batch → Many Students  
- One Student → Many Enrollments  

---

## 🚀 Installation & Setup

### 1️⃣ Clone Repository

### 1️⃣ Clone Repository
```bash
git clone <repository-url>
cd mit_tms
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run Migrations
```bash
python manage.py migrate
```

### 5️⃣ Create Superuser
```bash
python manage.py createsuperuser
```

### 6️⃣ Run Server
```bash
python manage.py runserver
```

---

## 🚀 Deployment

### Production Setup

- Use **Gunicorn** as WSGI server  
- Use **Nginx** as reverse proxy  
- Configure `.env` for environment variables  
- Use **PostgreSQL** for production database  

---

## 🔒 Security

- Environment-based configuration  
- Django authentication system  
- CSRF protection enabled  
- Role-based access control  

---

## 📈 Future Enhancements

- AI-based student performance prediction  
- Real-time notifications  
- Learning analytics dashboard  
- LMS integration  
- Mobile UI improvements  

---

## 🧠 Research Integration

This system supports research in:

> **Predictive Modeling for Identifying Early Warning Signs of Underperformance in Vocational Education**

### Possible Extensions

- Feature extraction (attendance, scores, engagement)  
- Machine learning models (Logistic Regression, Neural Networks, etc.)  
- Early warning systems  

---

## 📄 License

This project is for educational and research purposes.

---

## 👨‍💻 Author

**Sumudu Hettiarachchi**  
MIT Graduate | NVQ Instructor | Researcher in AI & Education
