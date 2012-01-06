from celery.task import Task
from celery.registry import tasks
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from celery.task.schedules import crontab  
from celery.decorators import periodic_task 





@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))  
def game_signup_summary():      
    GameTask.delay()



class GameTask(Task):

    def run(self):
        """ This method is for emailing the user once a day for games digest

        Keyword arguments:
        cwe -- that is being requested by the user
        user -- the user that is driving this request
        """
        

        email = user.email
        user = user
        subject, from_email, to = 'Welcome', 'games@courtside.me', email
        html_content = render_to_string('email_signup.html', {'user':user.first_name})
        text_content = strip_tags(html_content)
        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(subject, text_content, from_email,  [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


# register the task with celery
tasks.register(GameTask)
