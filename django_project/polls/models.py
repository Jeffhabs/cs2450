import uuid
from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    user = models.ForeignKey(User)
    question_text = models.CharField(max_length=128)
    pub_date = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    @property
    def get_uuid(self):
        return unicode(self.uuid)

    def __unicode__(self, *args, **kwargs):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=128)
    votes = models.PositiveIntegerField(default=0)

    def __unicode__(self, *args, **kwargs):
        return self.question.question_text + " - " + self.choice_text
