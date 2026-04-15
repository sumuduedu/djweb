# 📘 MIT TMS – Training Management System

## 📌 Overview

The **MIT Training Management System (MIT TMS)** is a web-based application developed using Django to manage vocational and academic training processes. It supports course management, student enrollment, batch management, and scheduling.

---

## ⚡ Quick Start

Get MIT TMS running in 5 minutes:

```bash
# Clone repository
git clone <repository-url>
cd mit_tms

# Setup environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install & run
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://localhost:8000` and log in with your superuser credentials.

---

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **pip** - Comes with Python
- **Git** - [Download Git](https://git-scm.com/downloads)
- **Virtual Environment** - Built into Python

**Operating System:**
- Linux / macOS / Windows (with WSL recommended)

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

```bash
git clone <repository-url>
cd mit_tms
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
# On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration (Optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
```

> **⚠️ Security Note:** Never commit `.env` to version control. Add it to `.gitignore`.

### 5️⃣ Run Migrations

```bash
python manage.py migrate
```

### 6️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7️⃣ Run Server

```bash
python manage.py runserver
```

Access the application at `http://localhost:8000`

---

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.accounts

# Run with verbose output
python manage.py test --verbosity=2

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 🔧 Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | `True` | Enable debug mode (set to `False` in production) |
| `SECRET_KEY` | - | Django secret key for security |
| `DATABASE_URL` | `sqlite:///db.sqlite3` | Database connection string |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Allowed domain names |
| `EMAIL_BACKEND` | `console` | Email backend service |

---

## 🚀 Deployment

### Production Setup

1. **Configure Environment:**
   - Set `DEBUG=False`
   - Update `SECRET_KEY` to a strong value
   - Set `ALLOWED_HOSTS` to your domain

2. **Use Gunicorn:**
   ```bash
   pip install gunicorn
   gunicorn mit_tms.wsgi:application --bind 0.0.0.0:8000
   ```

3. **Use Nginx as Reverse Proxy:**
   - Configure Nginx to forward requests to Gunicorn
   - Enable HTTPS with SSL certificates

4. **Database:**
   - Use **PostgreSQL** for production (recommended)
   - Update `DATABASE_URL` accordingly

5. **Static Files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

6. **Process Manager:**
   - Use **Systemd**, **Supervisor**, or **Docker** to manage Gunicorn process

---

## 🔒 Security

- ✅ Environment-based configuration  
- ✅ Django authentication system  
- ✅ CSRF protection enabled  
- ✅ Role-based access control  
- ✅ Password hashing with PBKDF2
- ⚠️ Always use HTTPS in production
- ⚠️ Keep dependencies updated: `pip list --outdated`

---

## 🐛 Troubleshooting

### Common Issues

**Issue: "ModuleNotFoundError: No module named 'django'"**
- **Solution:** Activate virtual environment and run `pip install -r requirements.txt`

**Issue: "Port 8000 already in use"**
- **Solution:** `python manage.py runserver 8001` or kill the process using port 8000

**Issue: "Migration errors"**
- **Solution:** 
  ```bash
  python manage.py migrate --fake-initial
  python manage.py migrate
  ```

**Issue: Database locked (SQLite)**
- **Solution:** Switch to PostgreSQL for production

**Issue: Static files not loading**
- **Solution:** 
  ```bash
  python manage.py collectstatic --clear
  python manage.py collectstatic
  ```

---

## 📈 Future Enhancements

- AI-based student performance prediction  
- Real-time notifications  
- Learning analytics dashboard  
- LMS integration  
- Mobile UI improvements  
- REST API endpoints
- GraphQL support

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/your-feature`
3. **Commit changes:** `git commit -m "Add your feature"`
4. **Push to branch:** `git push origin feature/your-feature`
5. **Open a Pull Request** with a clear description

### Code Style
- Follow PEP 8 for Python
- Use meaningful variable names
- Add docstrings to functions

---

## 🧠 Research Integration

This system supports research in:

> **Predictive Modeling for Identifying Early Warning Signs of Underperformance in Vocational Education**

### Possible Extensions

- Feature extraction (attendance, scores, engagement)  
- Machine learning models (Logistic Regression, Neural Networks, etc.)  
- Early warning systems  

---

## 📚 Useful Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [HTMX](https://htmx.org/)
- [Alpine.js](https://alpinejs.dev/)

---

## 📄 License

This project is for educational and research purposes.

---

## 👨‍💻 Author

**Sumudu Hettiarachchi**  
MIT Graduate | NVQ Instructor | Researcher in AI & Education

**Contact:** [Your Email/Website]  
**GitHub:** [@sumuduedu](https://github.com/sumuduedu)

---

**Last Updated:** April 2026
