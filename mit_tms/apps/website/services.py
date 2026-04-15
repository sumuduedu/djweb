from .models import ContactMessage, MessageReply, SentMessage, EnrollmentInquiry


def create_contact_message(data):
    return ContactMessage.objects.create(
        name=data.get('name'),
        email=data.get('email'),
        message=data.get('message')
    )


def create_enrollment_inquiry(data):
    return EnrollmentInquiry.objects.create(
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone'),
        course_id=data.get('course'),
        message=data.get('message')
    )


def get_inbox_messages():
    return ContactMessage.objects.order_by('-created_at')


def get_sent_messages():
    return SentMessage.objects.order_by('-sent_at')


def create_reply(message, reply_text):
    return MessageReply.objects.create(
        message=message,
        reply_text=reply_text
    )


def send_email_and_store(to_email, subject, message):
    msg = SentMessage.objects.create(
        to_email=to_email,
        subject=subject,
        message=message
    )
    return msg
