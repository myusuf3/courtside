from celery.registry import tasks
from celery.task import Task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class GameSignUpTask(Task):

    def run(self, user, game):
        """This method is responsible for asynchronously
            sending welcome email to users when they sign up.

            arguments:
                user- user object who just signed up

        """
        subject, from_email, to = 'Welcome', 'support@courtside.me', user.email
        html_content = render_to_string('game_email.html', {'user':user.first_name, 'game': game})
        text_content = strip_tags(html_content)
        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(subject, text_content, from_email,  [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()



class SignUpTask(Task):

    def run(self, user):
        """This method is responsible for asynchronously
           sending welcome email to users when they sign up.

        Keyword agruments:
        user- user object who just signed up

        """
        subject, from_email, to = 'Welcome', 'support@courtside.me', user.email
        html_content = render_to_string('email_signup.html', {'user':user.first_name})
        text_content = strip_tags(html_content)
        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(subject, text_content, from_email,  [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

# register the task with celery
tasks.register(SignUpTask)
