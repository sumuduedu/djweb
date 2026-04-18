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
