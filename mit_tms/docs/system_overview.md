# MIT Training Management System (TMS)

## Complete System Specification

---

# 1. Introduction

## 1.1 Purpose

The MIT Training Management System (TMS) is a web-based platform designed to manage vocational education processes, including user management, course delivery, enrollment, and role-based access control.

---

## 1.2 Objectives

* Provide structured learning delivery
* Manage users and roles efficiently
* Control access based on roles
* Support scalable educational workflows
* Enable future integration with analytics and AI systems

---

# 2. System Overview

## 2.1 Core Modules

### 1. Accounts Module

Handles:

* Authentication
* Role management
* Profile management
* User administration

---

### 2. Courses Module

Handles:

* Course structure
* Modules and lessons
* Enrollment system
* Learning content delivery

---

### 3. Dashboard Module

Handles:

* Role-based system entry points
* Navigation and quick access
* System overview for users

---

## 2.2 System Architecture

### Layered Design

#### Identity Layer

* User (Django)
* Profile (Role-based system)

---

#### Domain Layer

* Student
* Teacher
* Staff
* Parent
* Alumni
* Course
* Module
* Lesson
* Enrollment

---

#### Access Control Layer

* Role-Based Access Control (RBAC)
* View-level restrictions
* Template-level restrictions

---

#### Application Layer

* Views (business logic)
* Forms (validation)
* Signals (event-driven processing)

---

#### Presentation Layer

* Django Templates
* Tailwind CSS UI

---

#### Integration Layer

* Email activation system
* Social authentication (Google via Allauth)

---

# 3. Identity and Role System

## 3.1 User Model

Django built-in model used for authentication.

---

## 3.2 Profile Model

### Fields

* user (OneToOne)
* role
* image

---

## 3.3 Roles

* ADMIN
* STAFF
* TEACHER
* STUDENT
* PARENT
* ALUMNI
* GUEST

---

## 3.4 Role Behavior

* Each user has one role
* Role determines:

  * Access permissions
  * UI rendering
  * Associated domain model

---

## 3.5 Person Models

* Student
* Teacher
* Staff
* Parent
* Alumni

Each linked to User and managed via signals.

---

# 4. Course System

## 4.1 Course Structure

Course
→ Module
→ Lesson

---

## 4.2 Models

### Course

* title
* description
* duration
* fee
* is_active

---

### Module

* title
* order
* course (FK)

---

### Lesson

* title
* content / file
* module (FK)

---

### Enrollment

* student (FK)
* course (FK)
* enrolled_at
* status

---

## 4.3 Enrollment Rules

* Only students can enroll
* Enrollment required before access
* One student can enroll in multiple courses

---

# 5. Core Workflows

## 5.1 User Registration

1. User signs up
2. Account created (inactive)
3. Profile created (role = GUEST)
4. Activation email sent
5. User activates account

---

## 5.2 Login

1. User submits credentials
2. System validates:

   * credentials
   * active status
3. Redirect to dashboard

---

## 5.3 Social Login

1. User logs in via Google
2. Email is retrieved
3. Existing user → linked
4. New user → created
5. Profile ensured

---

## 5.4 Enrollment Workflow

1. Student selects course
2. Clicks enroll
3. System validates role
4. Enrollment created
5. Access granted

---

## 5.5 Learning Workflow

1. Student accesses enrolled course
2. Views modules
3. Views lessons

---

# 6. Access Control

## 6.1 Role-Based Access Matrix

| Role    | Access                  |
| ------- | ----------------------- |
| ADMIN   | Full system access      |
| TEACHER | Manage courses          |
| STUDENT | Access enrolled courses |
| STAFF   | Limited admin access    |
| PARENT  | View student data       |
| ALUMNI  | Limited access          |
| GUEST   | No course access        |

---

## 6.2 Core Rule

> A student cannot access course content unless enrolled.

---

## 6.3 Backend Enforcement

```python
if not Enrollment.objects.filter(student=user.student, course=course).exists():
    return redirect("courses:list")
```

---

## 6.4 Template Enforcement

```django
{% if is_enrolled %}
    <!-- show content -->
{% else %}
    <!-- show enroll button -->
{% endif %}
```

---

# 7. Dashboard System

## 7.1 Purpose

Provides role-based entry points and navigation.

---

## 7.2 Role-Based Dashboards

### Admin Dashboard

* User management
* Course statistics

---

### Teacher Dashboard

* Assigned courses
* Student management

---

### Student Dashboard

* Enrolled courses
* Learning access

---

## 7.3 Routing Logic

```python
if role == "ADMIN":
    return "/dashboard/admin/"
elif role == "TEACHER":
    return "/dashboard/teacher/"
elif role == "STUDENT":
    return "/dashboard/student/"
```

---

# 8. Signals (Event-Driven System)

## Events

### User Created

→ Profile created

### Profile Updated

→ Role models synchronized

### User Updated

→ Name synchronized

---

## Design Pattern

Observer Pattern

---

# 9. UI Design

## Features

* Tailwind CSS
* Responsive layout
* Role-based rendering
* Message alerts

---

## UI Components

* Authentication pages
* Profile page
* Course pages
* Dashboard views
* Admin panels

---

# 10. Security Considerations

* Email verification required
* Role-based access enforcement
* Admin protection
* Password hashing via Django

---

# 11. Known Limitations

* Single role per user
* Role change may delete previous data
* No learning analytics yet
* No progress tracking

---

# 12. Future Enhancements

* Multi-role support
* Learning analytics
* Student performance prediction (AI)
* Recommendation systems
* Assignment & grading system
* Notification system

---

# 13. Design Patterns Used

* Layered Architecture
* Role-Based Access Control (RBAC)
* Observer Pattern (Signals)
* MVC (Django MVT)
* Hierarchical Content Model

---

# 14. System Integration Summary

Accounts → Controls Identity & Roles
Courses → Controls Learning Content
Dashboard → Controls User Interaction

---

# 15. Core System Principle

> Identity + Role → Access Control → Learning Experience → Outcomes
