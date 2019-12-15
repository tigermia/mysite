from .models import Question
from django.db import models as mdls
import datetime
from django.utils import timezone


class QuestionChild(Question):
    question_new = mdls.CharField(max_length=200)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


