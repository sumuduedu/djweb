# Accounts Module Specification

## Training Management System (TMS)

---

# 1. Introduction

## 1.1 Purpose

The Accounts module manages user identity, authentication, and role-based access within the system.

It ensures that users can securely register, authenticate, and interact with the system according to their assigned roles.

---

## 1.2 Scope

This module includes:

* User authentication (login, logout)
* User registration and account activation
* Role-based access control (RBAC)
* Profile and identity management
* Administrative user management
* Social authentication integration (Google)

---

# 2. System Architecture

## 2.1 Layered Architecture

### Identity Layer

* Django User (core identity)
* Profile (role and metadata)

### Domain Layer

* Student
* Teacher
* Staff
* Parent
* Alumni

### Access Control Layer

* Role-based authorization via Profile
* View-level access control using mixins

### Application Layer

* Views (business logic)
* Forms (validation and input handling)

### Presentation Layer

* Django Templates (UI)
* Tailwind CSS for styling

### Integration Layer

* Email activation system
* Social authentication (django-allauth)

---

# 3. Data Model Design

## 3.1 Core Models

### User (Django Built-in)

Stores authentication credentials.

---

### Profile

#### Purpose

Extends User with role-based access control.

#### Fields

* user: OneToOneField(User)
* role: CharField (choices)
* image: ImageField (optional)

#### Roles

* ADMIN
* STAFF
* TEACHER
* STUDENT
* PARENT
* ALUMNI
* GUEST

#### Constraints

* Each user must have exactly one profile
* Default role = GUEST

---

### BasePerson (Abstract)

#### Fields

* user: OneToOneField(User)
* is_active: BooleanField

---

## 3.2 Domain Models

### Student

* full_name: CharField
* parents: ManyToManyField(Parent)

---

### Teacher

* full_name: CharField

---

### Staff

* full_name: CharField

---

### Parent

* relationship: CharField

---

### Alumni

* job_title: CharField
* company: CharField

---

# 4. Business Logic

## 4.1 Role-Based System

* Each user has a single role
* Role determines:

  * Access permissions
  * Available UI components
  * Associated domain model

---

## 4.2 Account Lifecycle

### Registration Flow

1. User submits signup form
2. Account created as inactive
3. Profile automatically created
4. Activation email sent
5. User activates account

---

### Authentication Flow

1. User submits credentials
2. System validates:

   * Credentials
   * Active status
3. User redirected to dashboard

---

### Social Login Flow

1. User logs in via Google
2. System retrieves email
3. If user exists → link account
4. Else → create new user
5. Profile ensured

---

## 4.3 Role Synchronization (Event-Driven)

When Profile.role changes:

* Corresponding domain model is created
* Other role models are removed or deactivated
* User identity remains consistent

---

## 4.4 Data Consistency Rules

* Profile is automatically created for each user
* Full name is synchronized across related models
* Role changes propagate automatically

---

# 5. Access Control

## 5.1 Authorization Strategy

Role-based access control (RBAC) using Profile.role

---

## 5.2 Admin Access

Only users with:

```
profile.role == 'ADMIN'
```

can access:

* User management
* System configuration

---

## 5.3 UI-Level Access Control

Templates enforce role-based visibility:

```django
{% if profile.role == "ADMIN" %}
```

---

# 6. Views and Functional Components

## 6.1 Authentication Views

* LoginView
* LogoutView
* SignupView
* ActivateAccountView

---

## 6.2 Profile Management

* ProfileView
* AccountSettingsView

---

## 6.3 Administrative Views

* UserListView
* UserDetailView
* UserCreateView
* UserUpdateView
* UserDeleteView
* ToggleUserStatusView

---

# 7. URL Design

## Authentication

* /accounts/login/
* /accounts/logout/
* /accounts/signup/
* /accounts/activate/<uid>/<token>/

## Profile

* /accounts/profile/

## Settings

* /accounts/settings/

## User Management

* /accounts/users/
* /accounts/users/create/
* /accounts/users/<id>/
* /accounts/users/<id>/update/
* /accounts/users/<id>/delete/
* /accounts/users/<id>/toggle/

---

# 8. Forms and Validation

## Login Form

* Validates credentials
* Prevents inactive users

---

## Signup Form

* Ensures unique username
* Ensures unique email
* Validates password confirmation

---

# 9. Signals (Event System)

## Events

### User Created

→ Profile automatically created

### Profile Updated

→ Role models synchronized

### User Updated

→ Name synchronized

---

## Design Pattern

Observer Pattern (event-driven architecture)

---

# 10. Admin Interface

* UserAdmin with Profile inline
* Role-based filtering
* Search and pagination support

---

# 11. UI Design

## Framework

* Tailwind CSS

## Features

* Responsive layout
* Role-based UI rendering
* Form validation feedback
* Message-based alerts

---

# 12. Security Considerations

* Password hashing via Django
* Email verification required
* Inactive users blocked from login
* Role-based access restrictions

---

# 13. Limitations

* Single role per user
* Role change may remove associated data
* Email login requires custom backend

---

# 14. Future Enhancements

* Multi-role support
* Soft delete for role transitions
* Advanced permission system
* Role-based dashboards
* Audit logging
