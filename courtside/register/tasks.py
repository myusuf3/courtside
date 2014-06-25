from time import sleep
from delorean import Delorean

from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.core.mail import EmailMultiAlternatives

from game.models import Game

class SignUpTask(object):

    def run(self, user):

        subject, from_email, to = 'Welcome', 'yusuf.mahdi@gmail.com', user.email

        html_content = render_to_string('email_signup.html', {'user': user.first_name})
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class CleanGamesTask(Task):
    def run(self, game_ids):
        # sleep for 15 seconds
        sleep(15)
        for game_id in game_ids:
            try:
                game = Game.objects.get(id=game_id)
            except:
                continue
            now = Delorean().naive()
            if game.start_date_and_time > now:
                print 'game %s has not occured yet!' % game.id
            else:
                game.active = False
            game.save()




