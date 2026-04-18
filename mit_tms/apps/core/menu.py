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


def student_menu(request):
    user = request.user

    if user.is_authenticated and hasattr(user, 'student'):
        menu = [
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
                    {"name": "Notifications", "icon": "🔔", "url": "core:student_notifications", "badge": "notifications"},
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
                    {"name": "Risk Alerts", "icon": "⚠️", "url": "core:student_risk", "badge": "risk"},
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
    else:
        menu = []

    return {
        "student_menu": menu
    }
