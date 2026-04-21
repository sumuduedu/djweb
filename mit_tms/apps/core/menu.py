ADMIN_MENU = [
    {
        "section": "Dashboard",
        "items": [
            {"name": "Overview", "url": "core:admin_dashboard", "icon": "📊"},
            {"name": "Analytics", "url": "core:staff_reports", "icon": "📈"},
        ]
    },
    {
        "section": "Academic",
        "items": [
            {"name": "Courses", "url": "course_list", "icon": "📚"},
            {"name": "Batches", "url": "batch:batch_list", "icon": "📦"},
            {"name": "Timetable", "url": "schedule:timetable_list", "icon": "🗓"},
            {"name": "Calendar", "url": "schedule:calendar", "icon": "📅"},
        ]
    },
    {
        "section": "User Management",
        "items": [
            {"name": "All Users", "url": "accounts:user_list", "icon": "👥"},
            {"name": "Staff", "url": "core:staff_dashboard", "icon": "🧑‍💼"},
            {"name": "Teachers", "url": "core:teacher_students", "icon": "👨‍🏫"},
            {"name": "Students", "url": "core:staff_students", "icon": "👨‍🎓"},
            {"name": "Parents", "url": "core:parent_children", "icon": "👨‍👩‍👧"},
            {"name": "Alumni", "url": "core:alumni_dashboard", "icon": "🎓"},
        ]
    },
    {
        "section": "AI Insights 🔥",
        "items": [
            {"name": "Analytics", "url": "core:teacher_analytics", "icon": "📊"},
            {"name": "At-Risk Students", "url": "core:teacher_risk_students", "icon": "⚠", "badge": "risk"},
            {"name": "Student Insights", "url": "core:student_insights", "icon": "🧠"},
        ]
    },
    {
        "section": "Communication",
        "items": [
            {"name": "Notifications", "url": "core:staff_notifications", "icon": "🔔", "badge": "notifications"},
            {"name": "Messages", "url": "core:teacher_messages", "icon": "💬"},
            {"name": "Announcements", "url": "core:teacher_announcements", "icon": "📢"},
        ]
    },
]
# ================================
# 🎓 STUDENT MENU
# ================================

STUDENT_MENU = [
    {
        "section": "Student Panel",
        "items": [
            {"name": "Dashboard", "icon": "🏠", "url": "core:student_dashboard"},
        ]
    },
    {
        "section": "Learning",
        "items": [
            {"name": "My Courses", "icon": "📘", "url": "core:student_courses"},
            {"name": "Assignments", "icon": "📝", "url": "core:student_assignments"},
            {"name": "Materials", "icon": "📂", "url": "core:student_materials"},
            {"name": "Attendance", "icon": "🗓️", "url": "core:student_attendance"},
        ]
    },
    {
        "section": "Performance",
        "items": [
            {"name": "Results", "icon": "🏆", "url": "core:student_results"},
            {"name": "Progress", "icon": "📈", "url": "core:student_progress"},
            {"name": "Certificates", "icon": "🎓", "url": "core:student_certificates"},
        ]
    },
    {
        "section": "Communication",
        "items": [
            {
                "name": "Notifications",
                "icon": "🔔",
                "url": "core:student_notifications",
                "badge": "notifications"
            },
            {"name": "Messages", "icon": "💬", "url": "core:student_messages"},
            {"name": "Announcements", "icon": "📢", "url": "core:student_announcements"},
        ]
    },
    {
        "section": "Finance",
        "items": [
            {"name": "Payments", "icon": "💳", "url": "core:student_payment"},
            {"name": "Receipts", "icon": "🧾", "url": "core:student_receipts"},
        ]
    },
    {
        "section": "Insights",
        "items": [
            {"name": "Performance Insights", "icon": "🧠", "url": "core:student_insights"},
            {
                "name": "Risk Alerts",
                "icon": "⚠️",
                "url": "core:student_risk",
                "badge": "risk"
            },
            {"name": "Recommendations", "icon": "💡", "url": "core:student_recommendations"},
        ]
    },
    {
        "section": "Account",
        "items": [
            {"name": "Settings", "icon": "⚙️", "url": "accounts:account_settings"},
        ]
    }
]

# ================================
# 👨‍🏫 TEACHER MENU
# ================================

TEACHER_MENU = [
    {
        "section": "Teacher Panel",
        "items": [
            {"name": "Dashboard", "icon": "🏠", "url": "core:teacher_dashboard"},
        ]
    },
    {
        "section": "Teaching",
        "items": [
            {"name": "Courses", "icon": "📘", "url": "course_list"},
            {"name": "Batches", "icon": "📦", "url": "batch:batch_list"},
            {"name": "Timetable", "icon": "🗓️", "url": "schedule:timetable_list"},
            {"name": "Materials", "icon": "📂", "url": "core:teacher_materials"},
            {"name": "Lesson Plan", "icon": "📂", "url": "lessonplan:list"},

        ]
    },
    {
        "section": "Academic",
        "items": [
            {"name": "Assignments", "icon": "📝", "url": "core:teacher_assignments"},
            {"name": "Submissions", "icon": "📥", "url": "core:teacher_submissions"},
            {"name": "Attendance", "icon": "📊", "url": "core:teacher_attendance"},
            {"name": "Grading", "icon": "🏆", "url": "core:teacher_results"},
        ]
    },
    {
        "section": "Students",
        "items": [
            {"name": "My Students", "icon": "👨‍🎓", "url": "core:teacher_students"},
            {"name": "Performance Tracking", "icon": "📈", "url": "core:teacher_performance"},
        ]
    },
    {
        "section": "Insights",
        "items": [
            {
                "name": "At-Risk Students",
                "icon": "⚠️",
                "url": "core:teacher_risk_students",
                "badge": "risk"
            },
            {"name": "Analytics", "icon": "🧠", "url": "core:teacher_analytics"},
        ]
    },
    {
        "section": "Communication",
        "items": [
            {
                "name": "Notifications",
                "icon": "🔔",
                "url": "core:teacher_notifications",
                "badge": "notifications"
            },
            {"name": "Messages", "icon": "💬", "url": "core:teacher_messages"},
            {"name": "Announcements", "icon": "📢", "url": "core:teacher_announcements"},
        ]
    },
    {
        "section": "Account",
        "items": [
            {"name": "Settings", "icon": "⚙️", "url": "accounts:account_settings"},
        ]
    }
]

# ================================
# 🧾 STAFF MENU
# ================================

STAFF_MENU = [
    {
        "section": "Staff Panel",
        "items": [
            {"name": "Dashboard", "icon": "🏠", "url": "core:staff_dashboard"},
        ]
    },
    {
        "section": "Operations",
        "items": [
            {"name": "Students", "icon": "👨‍🎓", "url": "core:staff_students"},
            {"name": "Enrollments", "icon": "📝", "url": "core:staff_enrollments"},
            {"name": "Batches", "icon": "📦", "url": "core:staff_batches"},
            {"name": "Attendance", "icon": "📅", "url": "core:staff_attendance"},
        ]
    },
    {
        "section": "Finance",
        "items": [
            {"name": "Payments", "icon": "💳", "url": "core:staff_payments"},
            {"name": "Invoices", "icon": "🧾", "url": "core:staff_invoices"},
        ]
    },
    {
        "section": "Reports",
        "items": [
            {"name": "Reports", "icon": "📊", "url": "core:staff_reports"},
        ]
    },
    {
        "section": "Communication",
        "items": [
            {
                "name": "Notifications",
                "icon": "🔔",
                "url": "core:staff_notifications",
                "badge": "notifications"
            },
        ]
    },
    {
        "section": "Account",
        "items": [
            {"name": "Settings", "icon": "⚙️", "url": "accounts:account_settings"},
        ]
    }
]

# ================================
# 🎓 ALUMNI MENU
# ================================

ALUMNI_MENU = [
    {
        "section": "Alumni Panel",
        "items": [
            {"name": "Dashboard", "icon": "🏠", "url": "core:alumni_dashboard"},
        ]
    },
    {
        "section": "Career",
        "items": [
            {"name": "Job Opportunities", "icon": "💼", "url": "core:alumni_jobs"},
            {"name": "Networking", "icon": "🤝", "url": "core:alumni_network"},
        ]
    },
    {
        "section": "Engagement",
        "items": [
            {"name": "Events", "icon": "📅", "url": "core:alumni_events"},
            {"name": "Feedback", "icon": "📝", "url": "core:alumni_feedback"},
        ]
    },
    {
        "section": "Records",
        "items": [
            {"name": "Certificates", "icon": "🎓", "url": "core:alumni_certificates"},
        ]
    },
    {
        "section": "Account",
        "items": [
            {"name": "Settings", "icon": "⚙️", "url": "accounts:account_settings"},
        ]
    }
]

# ================================
# 👪 PARENT MENU
# ================================

PARENT_MENU = [
    {
        "section": "Parent Panel",
        "items": [
            {"name": "Dashboard", "icon": "🏠", "url": "core:parent_dashboard"},
        ]
    },
    {
        "section": "Child",
        "items": [
            {"name": "My Children", "icon": "👨‍👩‍👧", "url": "core:parent_children"},
            {"name": "Progress", "icon": "📈", "url": "core:parent_progress"},
            {"name": "Attendance", "icon": "📅", "url": "core:parent_attendance"},
            {"name": "Results", "icon": "🏆", "url": "core:parent_results"},
        ]
    },
    {
        "section": "Finance",
        "items": [
            {"name": "Payments", "icon": "💳", "url": "core:parent_payments"},
        ]
    },
    {
        "section": "Communication",
        "items": [
            {
                "name": "Notifications",
                "icon": "🔔",
                "url": "core:parent_notifications",
                "badge": "notifications"
            },
            {"name": "Messages", "icon": "💬", "url": "core:parent_messages"},
        ]
    },
    {
        "section": "Account",
        "items": [
            {"name": "Settings", "icon": "⚙️", "url": "accounts:account_settings"},
        ]
    }
]

GUEST_MENU = [
    {
        "section": "Guest Panel",
        "items": [
            {"name": "Dashboard", "icon": "🏠", "url": "core:guest_dashboard"},
        ]
    }

]
