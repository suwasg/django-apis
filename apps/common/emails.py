from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

def send_html_email(subject, to_email, template_name, context):
    """
    Send an HTML email using Django's EmailMultiAlternatives.
    Args:
        subject (str): The subject of the email.
        to_email (str): The recipient's email address.
        template_name (str): The name of the HTML template to render.
        context (dict): Context data to render the template with.
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    # Render the HTML content from the template 
    html_content = render_to_string(template_name, context)
    # Create a plain text version of the email content
    text_content = strip_tags(html_content)
    # Create the email message
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content or " ",
        from_email=from_email,
        to=[to_email],
    )
    # Attach the HTML content to the email
    if html_content:
        email.attach_alternative(html_content, "text/html")
        # Send the email
    email.send()