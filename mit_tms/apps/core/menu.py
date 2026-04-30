ADMIN_MENU = [
    {
        "section": "Dashboard",
        "items": [
            {"name": "Overview", "url": "dashboard:admin_dashboard", "icon": "📊"},
         #   {"name": "Analytics", "url": "core:staff_reports", "icon": "📈"},
        ]
    },
    {
        "section": "Academic",
        "items": [
            {"name": "Courses", "url": "dashboard:admin_courses_list", "icon": "📚"},
            {"name": "Batches", "url": "batch:batch_list", "icon": "📦"},
            {"name": "Timetable", "url": "schedule:timetable_list", "icon": "🗓"},
            {"name": "Calendar", "url": "schedule:calendar", "icon": "📅"},
            {"name": "Student Enroll", "url": "schedule:calendar", "icon": "📅"},

        ]
    },
    {
        "section": "User Management",
        "items": [
            {"name": "All Users", "url": "accounts:user_list", "icon": "👥"},
            {"name": "Staff", "url": "dashboard:staff_dashboard", "icon": "🧑‍💼"},
            {"name": "Teachers", "url": "dashboard:teacher_students", "icon": "👨‍🏫"},
            {"name": "Students", "url": "dashboard:staff_students", "icon": "👨‍🎓"},
            {"name": "Parents", "url": "dashboard:parent_children", "icon": "👨‍👩‍👧"},
            {"name": "Alumni", "url": "dashboard:alumni_dashboard", "icon": "🎓"},
        ]
    },
    # {
    #     "section": "AI Insights 🔥",
    #     "items": [
    #         {"name": "Analytics", "url": "core:teacher_analytics", "icon": "📊"},
    #         {"name": "At-Risk Students", "url": "core:teacher_risk_students", "icon": "⚠", "badge": "risk"},
    #         {"name": "Student Insights", "url": "core:student_insights", "icon": "🧠"},
    #     ]
    # },
    # {
    #     "section": "Communication",
    #     "items": [
    #         {"name": "Notifications", "url": "core:staff_notifications", "icon": "🔔", "badge": "notifications"},
    #         {"name": "Messages", "url": "core:teacher_messages", "icon": "💬"},
    #         {"name": "Announcements", "url": "core:teacher_announcements", "icon": "📢"},
    #     ]
    # },
]
# ================================
# 🎓 STUDENT MENU
# ================================

STUDENT_MENU = [
    {
        "section": "Student Panel",
        "items": [
            {"name": "Dashboard", "icon": "🏠", "url": "dashboard:student_dashboard"},
        ]
    },
    {
        "section": "Learning",
        "items": [
            {"name": "My Courses", "icon": "📘", "url": "dashboard:student_courses"},
            {"name": "Assignments", "icon": "📝", "url": "dashboard:student_assignments"},
            {"name": "Materials", "icon": "📂", "url": "dashboard:student_materials"},
            {"name": "Attendance", "icon": "🗓️", "url": "dashboard:student_attendance"},
        ]
    },
    {
        "section": "Performance",
        "items": [
            {"name": "Results", "icon": "🏆", "url": "dashboard:student_results"},
            {"name": "Progress", "icon": "📈", "url": "dashboard:student_progress"},
            {"name": "Certificates", "icon": "🎓", "url": "dashboard:student_certificates"},
        ]
    },
    {
        "section": "Communication",
        "items": [
            {
                "name": "Notifications",
                "icon": "🔔",
                "url": "dashboard:student_notifications",
                "badge": "notifications"
            },
            {"name": "Messages", "icon": "💬", "url": "dashboard:student_messages"},
            {"name": "Announcements", "icon": "📢", "url": "dashboard:student_announcements"},
        ]
    },
    {
        "section": "Finance",
        "items": [
            {"name": "Payments", "icon": "💳", "url": "dashboard:student_payment"},
            {"name": "Receipts", "icon": "🧾", "url": "dashboard:student_receipts"},
        ]
    },
    {
        "section": "Insights",
        "items": [
            {"name": "Performance Insights", "icon": "🧠", "url": "dashboard:student_insights"},
            {
                "name": "Risk Alerts",
                "icon": "⚠️",
                "url": "dashboard:student_risk",
                "badge": "risk"
            },
            {"name": "Recommendations", "icon": "💡", "url": "dashboard:student_recommendations"},
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
            {"name": "Dashboard", "icon": "🏠", "url": "dashboard:teacher_dashboard"},
        ]
    },
 # {
 #        "section": "Communication",
 #        "items": [
 #            {
 #                "name": "Notifications",
 #                "icon": "🔔",
 #                "url": "dashboard:teacher_notifications",
 #                "badge": "notifications"
 #            },
 #            {"name": "Messages", "icon": "💬", "url": "dashboard:teacher_messages"},
 #            {"name": "Announcements", "icon": "📢", "url": "core:teacher_announcements"},
 #        ]
 #    },
  {
    "section": "Teaching & Delivery",
    "items": [
        {
            "name": "My Courses",
            "icon": "📘",
            "url": "dashboard:teacher_courses"
        },
        {
            "name": "My Batches",
            "icon": "📦",
            "url": "batch:batch_list"
        },

    ]
},
        {
        "section": "Lesson Planing & Schduling ",
        "items": [
            {"name": "Timetable", "icon": "🗓️", "url": "schedule:timetable_list"},
            {"name": "Lesson Plan", "icon": "📂", "url": "lessonplan:list"},


        ]
    },


    # {
    #     "section": "Assesments & Evaluation",
    #     "items": [
    #         {"name": "Learning Materials", "icon": "📂", "url": "dashboard:teacher_materials" },
    #         {"name": "Assignments", "icon": "📝", "url": "dashboard:teacher_assignments"},
    #         {"name": "Submissions", "icon": "📥", "url": "dashboard:teacher_submissions"},
    #         {"name": "Attendance", "icon": "📊", "url": "dashboard:teacher_attendance"},
    #         {"name": "Grading", "icon": "🏆", "url": "dashboard:teacher_results"},
    #
    #     ]
    # },


    # {
    #     "section": "Students",
    #     "items": [
    #         {"name": "My Students", "icon": "👨‍🎓", "url": "dashboard:teacher_students"},
    #         {"name": "Performance Tracking", "icon": "📈", "url": "dashboard:teacher_performance"},
    #     ]
    # },
    # {
    #     "section": "Insights",
    #     "items": [
    #         {
    #             "name": "At-Risk Students",
    #             "icon": "⚠️",
    #             "url": "dashboard:teacher_risk_students",
    #             "badge": "risk"
    #         },
    #         {"name": "Analytics", "icon": "🧠", "url": "dashboard:teacher_analytics"},
    #     ]
    # },

    # {
    #     "section": "Account",
    #     "items": [
    #         {"name": "Settings", "icon": "⚙️", "url": "accounts:account_settings"},
    #     ]
    # }
]

# ================================
# 🧾 STAFF MENU
# ================================

STAFF_MENU = [
    {
        "section": "Staff Panel",
        "items": [
            {"name": "Dashboard", "icon": "🏠", "url": "dashboard:staff_dashboard"},
        ]
    },
    {
        "section": "Operations",
        "items": [
            {"name": "Students", "icon": "👨‍🎓", "url": "dashboard:staff_students"},
            {"name": "Enrollments", "icon": "📝", "url": "dashboard:staff_enrollments"},
            {"name": "Batches", "icon": "📦", "url": "dashboard:staff_batches"},
            {"name": "Attendance", "icon": "📅", "url": "dashboard:staff_attendance"},
        ]
    },
    {
        "section": "Finance",
        "items": [
            {"name": "Payments", "icon": "💳", "url": "dashboard:staff_payments"},
            {"name": "Invoices", "icon": "🧾", "url": "dashboard:staff_invoices"},
        ]
    },
    {
        "section": "Reports",
        "items": [
            {"name": "Reports", "icon": "📊", "url": "dashboard:staff_reports"},
        ]
    },
    {
        "section": "Communication",
        "items": [
            {
                "name": "Notifications",
                "icon": "🔔",
                "url": "dashboard:staff_notifications",
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
            {"name": "Dashboard", "icon": "🏠", "url": "dashboard:alumni_dashboard"},
        ]
    },
    {
        "section": "Career",
        "items": [
            {"name": "Job Opportunities", "icon": "💼", "url": "dashboard:alumni_jobs"},
            {"name": "Networking", "icon": "🤝", "url": "dashboard:alumni_network"},
        ]
    },
    {
        "section": "Engagement",
        "items": [
            {"name": "Events", "icon": "📅", "url": "dashboard:alumni_events"},
            {"name": "Feedback", "icon": "📝", "url": "dashboard:alumni_feedback"},
        ]
    },
    {
        "section": "Records",
        "items": [
            {"name": "Certificates", "icon": "🎓", "url": "dashboard:alumni_certificates"},
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
            {"name": "Dashboard", "icon": "🏠", "url": "dashboard:parent_dashboard"},
        ]
    },
    {
        "section": "Child",
        "items": [
            {"name": "My Children", "icon": "👨‍👩‍👧", "url": "dashboard:parent_children"},
            {"name": "Progress", "icon": "📈", "url": "dashboard:parent_progress"},
            {"name": "Attendance", "icon": "📅", "url": "dashboard:parent_attendance"},
            {"name": "Results", "icon": "🏆", "url": "dashboard:parent_results"},
        ]
    },
    {
        "section": "Finance",
        "items": [
            {"name": "Payments", "icon": "💳", "url": "dashboard:parent_payments"},
        ]
    },
    {
        "section": "Communication",
        "items": [
            {
                "name": "Notifications",
                "icon": "🔔",
                "url": "dashboard:parent_notifications",
                "badge": "notifications"
            },
            {"name": "Messages", "icon": "💬", "url": "dashboard:parent_messages"},
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
            {"name": "Dashboard", "icon": "🏠", "url": "dashboard:guest_dashboard"},
        ]
    }

]
