from django.db import models
from datetime import datetime, timedelta
from forum.models import User

class UserMessage(models.Model):
    user_from = models.ForeignKey(User, related_name='user_from')
    user_to = models.ForeignKey(User, related_name='user_to')
    text = models.TextField()
    send_date = models.DateTimeField(default=datetime.now)
    is_new = models.BooleanField(default=True)
