# apps/core/gateway.py

try:
    # 🔷 WEBSITE SERVICES
    from apps.website.services import (
        create_contact_message,
        create_enrollment_inquiry,
        get_inbox_messages,
        get_sent_messages,
        create_reply,
        send_email_and_store,
    )
except ImportError:
    def create_contact_message(data): return None
    def create_enrollment_inquiry(data): return None
    def get_inbox_messages(): return []
    def get_sent_messages(): return []
    def create_reply(msg, text): return None
    def send_email_and_store(*args): return None


# 🔥 ADD THIS BLOCK (IMPORTANT)
try:
    from apps.enrollment.services import get_student_enrollments
except ImportError:
    def get_student_enrollments(user):
        return []
