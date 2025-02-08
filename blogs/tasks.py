from __future__ import absolute_import, unicode_literals
from celery import Celery, shared_task
from django.core.mail import send_mail
from .models import Post
import subprocess

app = Celery('myblog')
app.conf.broker_url = "redis:/localhost:6379/0"

@shared_task
def send_message(post_id, user_now, message = None, to_user=None):
    post = Post.objects.get(id = post_id)
    subject = f'Post about {post.title}'
    message = f'{message}'
    mail_sent = send_mail(subject,message,user_now, [to_user])
    return mail_sent


@shared_task
def dump_blogs_task():
    try:
        command = [
            'python', 'manage.py', 'dampdata',
            'blogs',
            '--indent=2',
            '--output=blogs/fixtures/myblogs_data.json'
        ]
        subprocess.run(command, check=True)
        return "Data dump completed successfully"
    except subprocess.CalledProcessError as e:
        return f"Error during data dump {e}"