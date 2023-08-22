from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from config import settings


def send_email(email_from: str, email_to: str, template_id: str, dynamic_template_data: dict = {}):
    message = Mail(
        from_email=email_from,
        to_emails=email_to,
    )
    message.template_id = template_id
    message.dynamic_template_data = dynamic_template_data
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    sg.send(message)