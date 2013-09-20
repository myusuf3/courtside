from celery.registry import tasks
from celery.task import Task

from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.core.mail import EmailMultiAlternatives

class SignUpTask(Task):

    def run(self, user):

        subject, from_email, to = 'Welcome', 'yusuf.mahdi@gmail.com', user.email

        html_content = render_to_string('email_signup.html', {'user': user.first_name})
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

tasks.register(SignUpTask)





