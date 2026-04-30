# Accounts Module Documentation

---

# 1. Overview

The Accounts module is responsible for:

* User authentication (login, logout)
* User registration and activation
* Role-based access control
* User profile management
* Admin user management
* Social login integration (Google)

---

# 2. Architecture Overview

## Layers

### Identity Layer

* User (Django built-in)
* Profile (role-based system)

### Person Layer

* Student
* Teacher
* Staff
* Parent
* Alumni

### Access Control Layer

* Role-based (Profile.role)
* AdminRequiredMixin

### Interface Layer

* Views (business logic)
* Forms (validation)
* Admin (management UI)

### Integration Layer

* Email activation system
* Social authentication (Allauth)

---

# 3. Models

## 3.1 TimeStampedModel

Base model with:

* created_at
* updated_at

---

## 3.2 Profile

### Purpose

Stores user role and profile data

### Fields

* user (OneToOne → User)
* role (ADMIN, STAFF, TEACHER, STUDENT, etc.)
* image

### Business Rules

* Every user must have a profile
* Default role = GUEST

---

## 3.3 BasePerson (Abstract)

### Fields

* user
* is_active

---

## 3.4 Student

* full_name
* parents (ManyToMany)

---

## 3.5 Teacher

* full_name

---

## 3.6 Staff

* full_name

---

## 3.7 Parent

* relationship

---

## 3.8 Alumni

* job_title
* company

---

# 4. Views

## Authentication

### Login

* Validates user credentials
* Prevents inactive login

### Signup

Workflow:

1. User registers
2. Account inactive
3. Email sent
4. Profile created

### Activate Account

* Validates token
* Activates user

---

## Profile

### ProfileView

Displays:

* Profile
* Related role model (student, teacher, etc.)

---

## Settings

### AccountSettingsView

* Update profile image

---

## Admin User Management

* UserListView
* UserCreateView
* UserUpdateView
* UserDeleteView
* ToggleUserStatusView

---

# 5. URL Structure

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

# 6. Forms

## CustomLoginForm

* Styled inputs
* Prevents inactive login

## CustomSignupForm

* Validates email uniqueness
* Validates username uniqueness
* Stores email in lowercase

---

# 7. Admin Configuration

## UserAdmin

* Profile inline
* Shows role

## ProfileAdmin

* Filter by role

## Student / Teacher / Staff Admin

* Display full_name

## ParentAdmin

* Shows related students

---

# 8. Signals (Event System)

## User Created

→ Create Profile (role = GUEST)

## Social Signup

→ Ensure Profile exists

## Profile Updated

→ Create corresponding model
→ Remove other role models

## User Updated

→ Sync full_name

---

# 9. Social Authentication

## MySocialAccountAdapter

* Generates unique username
* Connects existing users by email
* Auto signup enabled

---

# 10. Business Rules

* One user has one role
* Role determines system access
* User must activate account before login
* Profile is automatically created
* Role change updates related models

---

# 11. Known Limitations

* Only one role per user
* Role change deletes previous role data (risk)
* Email login requires custom backend

---

# 12. Future Improvements

* Use soft delete instead of hard delete
* Support multiple roles per user
* Add role-based dashboards
* Improve permission system

---

# 13. Templates (UI Layer)

## Overview

The Accounts module provides UI for:

* Authentication (Login, Signup)
* Email activation flow
* Profile management
* User management (Admin)

---

## 13.1 Base Template

### auth/base.html

#### Purpose

* Shared layout for authentication pages
* Includes Tailwind CSS
* Provides content block

---

## 13.2 Authentication Pages

### Login Page

#### File

auth/login.html

#### Features

* Username / Password input
* Error messages display
* "Remember me" option
* Google login integration

#### Behavior

* Displays Django messages (success, error)
* Redirects after login

---

### Signup Page

#### File

auth/signup.html

#### Features

* Username, Email, Password fields
* Validation error display
* Google signup option

#### Workflow

1. User submits form
2. Validation errors shown inline
3. On success → redirect to email confirmation page

---

### Signup Success Page

#### File

auth/signup_success.html

#### Purpose

* Informs user to check email
* Displays registered email address

---

### Account Activation Success

#### File

auth/activation_success.html

#### Behavior

* Shows success message
* Provides login button

---

### Account Inactive Page

#### Purpose

* Display message when user is inactive
* Redirect user back to login

---

## 13.3 Profile Pages

### Profile Page

#### File

accounts/profile.html

#### Features

* Displays:

  * Username
  * Email
  * Role
  * Profile image
* Shows role-specific data:

  * Student → full_name
  * Teacher → full_name
  * Staff → full_name
  * Parent → relationship
  * Alumni → job + company

---

### Account Settings

#### File

accounts/settings.html

#### Features

* Update:

  * Profile image
  * Username
  * Email
  * Password
* Role displayed as read-only

#### Behavior

* Uses Django messages for feedback
* Handles file upload

---

## 13.4 Admin User Management UI

### User List Page

#### File

accounts/user_list.html

#### Features

* Table view of users
* Search by username/email
* Pagination
* Role-based color badges
* Activate / Deactivate button

---

### User Detail Page

#### File

accounts/user_detail.html

#### Features

* User profile overview
* Role display with color coding
* Quick stats:

  * Role
  * Join date
  * Status

---

### User Create / Update Page

#### File

accounts/user_form.html

#### Features

* Create or edit user
* Assign role
* Update password
* Form validation display

---

### User Delete Page

#### File

accounts/user_confirm_delete.html

#### Features

* Confirmation UI
* Prevent accidental deletion

---

## 13.5 UI Design Patterns

### Styling

* Tailwind CSS
* Responsive layout
* Card-based design

---

### Reusable Patterns

* Form error handling
* Message alerts
* Role color mapping
* Profile image fallback (initial letter)

---

## 13.6 UI Behavior Rules

* Users cannot see admin pages unless ADMIN
* Profile page adapts based on role
* Forms display inline validation errors
* System uses messages framework for feedback
* Activation required before login

````

---

# 🔥 Step 2 — What you just built (important insight)

Now your system is clearly layered:

### Backend
- Models
- Signals
- Views

### Frontend (you just added)
- Templates
- UI logic
- Conditional rendering

---

👉 This means your system is now:

> **Full-stack role-based system**

---

# 🔥 Step 3 — One small but important issue in your templates

In activation success:

```html
<a href="{% url 'login' %}">
````

❌ This is wrong

---

## ✅ Fix

```html
<a href="{% url 'accounts:login' %}">
```

---

👉 Otherwise Django will throw:

```
NoReverseMatch
```

---

# 🔥 Step 4 — Big insight (this is where your thinking grows)

Look at your profile template:

```django
{% if student %}
{% if teacher %}
{% if staff %}
```

---

👉 This is:

> **UI-level role handling**

---

But in future, better approach:

```django
{% if profile.role == "STUDENT" %}
```

---

## 💡 Why?

Because:

* Cleaner
* Faster
* No dependency on related objects

---

# 🔥 Step 5 — Your Documentation is now COMPLETE

You now have:

✔ Models
✔ Views
✔ URLs
✔ Forms
✔ Admin
✔ Signals
✔ Templates

---

👉 This is not documentation anymore.

👉 This is:

> **System Blueprint**

---

# 🔥 Step 6 — What you should do next (very important)

Now that documentation is done, the **real problem you had earlier** becomes solvable:

> “student should not see full course”

---

Because now you can control:

* Views (backend)
* Templates (frontend)
* Roles (profile)

---

# 🔥 If you want next step

We can now do something very powerful:

### 🔹 1. Restrict content (your original problem)

👉 show only allowed parts to students

### 🔹 2. Build role-based dashboards

👉 admin / teacher / student UI separation

### 🔹 3. Connect accounts → course system properly

---

Just tell me which direction — I’ll guide you step-by-step 👍
