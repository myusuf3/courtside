from celery.decorators import periodic_task
from celery.registry import tasks
from celery.task import Task
from celery.task.schedules import crontab
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
def game_signup_summary():
    GameTask.delay()


class GameTask(Task):

    def run(self, cwe, user):
        """ This method is for emailing the user once a day for games digest

        arguments:
        cwe -- that is being requested by the user
        user -- the user that is driving this request
        """

        subject, from_email, to = 'Welcome', 'games@courtside.me', user.email
        html_content = render_to_string('email_signup.html', {'user':user.first_name})
        text_content = strip_tags(html_content)
        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

# register the task with celery
tasks.register(GameTask)
