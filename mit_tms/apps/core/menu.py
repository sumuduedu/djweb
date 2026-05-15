# =========================================================
# ADMIN MENU
# =========================================================

ADMIN_MENU = [

    {
        "section": "Dashboard",

        "items": [

            {
                "name": "Overview",
                "url": "dashboard:admin_dashboard",
                "icon": "📊"
            },
        ]
    },

    {
        "section": "Academic",

        "items": [

            {
                "name": "Courses",
                "url": "dashboard:admin_courses",
                "icon": "📚"
            },

            {
                "name": "Modules",
                "url": "dashboard:admin_modules",
                "icon": "📦"
            },

            {
                "name": "Tasks",
                "url": "dashboard:admin_tasks",
                "icon": "📝"
            },

            {
                "name": "Activities",
                "url": "dashboard:admin_activities",
                "icon": "⚡"
            },
        ]
    },

    {
        "section": "User Management",

        "items": [

            {
                "name": "All Users",
                "url": "accounts:user_list",
                "icon": "👥"
            },

            {
                "name": "Staff",
                "url": "dashboard:staff_dashboard",
                "icon": "🧑‍💼"
            },

            {
                "name": "Teachers",
                "url": "dashboard:staff_teachers",
                "icon": "👨‍🏫"
            },

            {
                "name": "Students",
                "url": "dashboard:staff_students",
                "icon": "🎓"
            },

            {
                "name": "Parents",
                "url": "dashboard:parent_children",
                "icon": "👨‍👩‍👧"
            },

            {
                "name": "Alumni",
                "url": "dashboard:alumni_profile",
                "icon": "🎓"
            },
        ]
    },
]


# =========================================================
# STUDENT MENU
# =========================================================

STUDENT_MENU = [

    {
        "section": "Student Panel",

        "items": [

            {
                "name": "Dashboard",
                "icon": "🏠",
                "url": "dashboard:student_dashboard"
            },
        ]
    },

    {
        "section": "Learning",

        "items": [

            {
                "name": "My Courses",
                "icon": "📘",
                "url": "dashboard:student_courses"
            },

            # {
            #     "name": "Assignments",
            #     "icon": "📝",
            #     "url": "dashboard:student_assignments"
            # },
            #
            # {
            #     "name": "Materials",
            #     "icon": "📂",
            #     "url": "dashboard:student_materials"
            # },
            #
            # {
            #     "name": "Attendance",
            #     "icon": "📅",
            #     "url": "dashboard:student_attendance"
            # },
        ]
    },

    {
        "section": "Performance",

        "items": [

            # {
            #     "name": "Results",
            #     "icon": "🏆",
            #     "url": "dashboard:student_results"
            # },
            #
            # {
            #     "name": "Progress",
            #     "icon": "📈",
            #     "url": "dashboard:student_progress"
            # },
            #
            # {
            #     "name": "Certificates",
            #     "icon": "🎓",
            #     "url": "dashboard:student_certificates"
            # },
        ]
    },

    {
        "section": "Communication",

        "items": [

            # {
            #     "name": "Notifications",
            #     "icon": "🔔",
            #     "url": "dashboard:student_notifications"
            # },
            #
            # {
            #     "name": "Messages",
            #     "icon": "💬",
            #     "url": "dashboard:student_messages"
            # },
            #
            # {
            #     "name": "Announcements",
            #     "icon": "📢",
            #     "url": "dashboard:student_announcements"
            # },
        ]
    },

    {
        "section": "Finance",

        "items": [

            # {
            #     "name": "Payments",
            #     "icon": "💳",
            #     "url": "dashboard:student_payments"
            # },
            #
            # {
            #     "name": "Receipts",
            #     "icon": "🧾",
            #     "url": "dashboard:student_receipts"
            # },
        ]
    },

    {
        "section": "Insights",

        "items": [

            # {
            #     "name": "Performance Insights",
            #     "icon": "🧠",
            #     "url": "dashboard:student_insights"
            # },
            #
            # {
            #     "name": "Risk Alerts",
            #     "icon": "⚠️",
            #     "url": "dashboard:student_risk"
            # },
            #
            # {
            #     "name": "Recommendations",
            #     "icon": "💡",
            #     "url": "dashboard:student_recommendations"
            # },
        ]
    },

    {
        "section": "Account",

        "items": [

            {
                "name": "Settings",
                "icon": "⚙️",
                "url": "accounts:account_settings"
            },
        ]
    },
]


# =========================================================
# TEACHER MENU
# =========================================================

TEACHER_MENU = [

    {
        "section": "Teacher Panel",

        "items": [

            {
                "name": "Dashboard",
                "icon": "🏠",
                "url": "dashboard:teacher_dashboard"
            },
        ]
    },

    {
        "section": "Teaching",

        "items": [

            {
                "name": "My Courses",
                "icon": "📘",
                "url": "dashboard:teacher_courses"
            },
        ]
    },
]


# =========================================================
# STAFF MENU
# =========================================================

STAFF_MENU = [

    {
        "section": "Staff Panel",

        "items": [

            {
                "name": "Dashboard",
                "icon": "🏠",
                "url": "dashboard:staff_dashboard"
            },
        ]
    },

    {
        "section": "Management",

        "items": [

            {
                "name": "Students",
                "icon": "🎓",
                "url": "dashboard:staff_students"
            },

            {
                "name": "Teachers",
                "icon": "👨‍🏫",
                "url": "dashboard:staff_teachers"
            },

            {
                "name": "Courses",
                "icon": "📚",
                "url": "dashboard:staff_courses"
            },

            {
                "name": "Batches",
                "icon": "📦",
                "url": "dashboard:staff_batches"
            },
        ]
    },

    {
        "section": "Operations",

        "items": [

            {
                "name": "Enrollments",
                "icon": "📝",
                "url": "dashboard:staff_enrollments"
            },

            {
                "name": "Attendance",
                "icon": "📅",
                "url": "dashboard:staff_attendance"
            },

            {
                "name": "Payments",
                "icon": "💳",
                "url": "dashboard:staff_payments"
            },

            {
                "name": "Invoices",
                "icon": "🧾",
                "url": "dashboard:staff_invoices"
            },
        ]
    },
]


# =========================================================
# PARENT MENU
# =========================================================

PARENT_MENU = [

    {
        "section": "Parent Panel",

        "items": [

            {
                "name": "Dashboard",
                "icon": "🏠",
                "url": "dashboard:parent_dashboard"
            },
        ]
    },

    {
        "section": "Children",

        "items": [

            {
                "name": "My Children",
                "icon": "👨‍👩‍👧",
                "url": "dashboard:parent_children"
            },

            {
                "name": "Progress",
                "icon": "📈",
                "url": "dashboard:parent_progress"
            },

            {
                "name": "Attendance",
                "icon": "📅",
                "url": "dashboard:parent_attendance"
            },

            {
                "name": "Payments",
                "icon": "💳",
                "url": "dashboard:parent_payments"
            },
        ]
    },
]


# =========================================================
# ALUMNI MENU
# =========================================================

ALUMNI_MENU = [

    {
        "section": "Alumni Panel",

        "items": [

            {
                "name": "Dashboard",
                "icon": "🏠",
                "url": "dashboard:alumni_dashboard"
            },

            {
                "name": "Profile",
                "icon": "🎓",
                "url": "dashboard:alumni_profile"
            },

            {
                "name": "Courses",
                "icon": "📚",
                "url": "dashboard:alumni_courses"
            },

            {
                "name": "Certificates",
                "icon": "🏆",
                "url": "dashboard:alumni_certificates"
            },
        ]
    },
]


# =========================================================
# GUEST MENU
# =========================================================

GUEST_MENU = [

    {
        "section": "Guest Panel",

        "items": [

            {
                "name": "Dashboard",
                "icon": "🏠",
                "url": "dashboard:guest_dashboard"
            },
        ]
    },
]
