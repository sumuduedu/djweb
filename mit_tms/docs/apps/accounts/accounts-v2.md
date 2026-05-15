# MIT TMS / SIS Dashboard System Documentation

## Overview

MIT TMS is a modular enterprise-style educational platform designed as a:

- Training Management System (TMS)
- Student Information System (SIS)
- Learning Management System (LMS)

The system supports:

- Role-based dashboards
- Modular architecture
- Dynamic sidebar navigation
- Namespaced URL routing
- Reusable UI components
- Secure authentication and authorization

The navigation architecture is centralized in `menu.py`. :contentReference[oaicite:0]{index=0}

---

# 1. System Architecture

## Project Structure

```text
MIT_TMS
│
├── apps/
│   ├── accounts/
│   ├── dashboard/
│   ├── courses/
│   ├── batch/
│   ├── schedule/
│   ├── lessonplan/
│   └── core/
│
├── templates/
├── static/
└── media/
