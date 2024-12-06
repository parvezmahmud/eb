from django.db import models
import uuid
from django.contrib.auth.models import User

class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    question_text = models.CharField(max_length=255, blank=True, null=True)
    option1 = models.CharField(max_length=255, blank=True, null=True)
    option1_is_correct = models.BooleanField(default=False)
    option2 = models.CharField(max_length=255, blank=True, null=True)
    option2_is_correct = models.BooleanField(default=False)
    option3 = models.CharField(max_length=255, blank=True, null=True)
    option3_is_correct = models.BooleanField(default=False)
    option4 = models.CharField(max_length=255, blank=True, null=True)
    option4_is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)  # Field to maintain order
    
    class Meta:
        ordering = ['order']


#B Unit
class EXAM_BATCH_BUNIT(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    unit = models.CharField(max_length=255, default='B-UNIT')
    title = models.CharField(max_length=255)
    number_of_questions = models.IntegerField(default=60)
    marks = models.FloatField(default=0)
    time = models.IntegerField(default=0)
    questions = models.ManyToManyField(Question)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class EXAM_BATCH_CARDS_BUNIT(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    unit = models.CharField(max_length=255, default='B-UNIT')
    drive_link = models.CharField(max_length=255)
    take_exam = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



#C UNIT
class EXAM_BATCH_CUNIT(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    unit = models.CharField(max_length=255, default='C-UNIT')
    title = models.CharField(max_length=255)
    number_of_questions = models.IntegerField(default=60)
    marks = models.FloatField(default=0)
    time = models.IntegerField(default=0)
    questions = models.ManyToManyField(Question)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class EXAM_BATCH_CARDS_CUNIT(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    unit = models.CharField(max_length=255, default='C-UNIT')
    drive_link = models.CharField(max_length=255)
    take_exam = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UserAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(null=True, blank=True, max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def is_correct(self):
        if self.selected_option == self.question.option1 and self.question.option1_is_correct:
            return True
        elif self.selected_option == self.question.option2 and self.question.option2_is_correct:
            return True
        elif self.selected_option == self.question.option3 and self.question.option3_is_correct:
            return True
        elif self.selected_option == self.question.option4 and self.question.option4_is_correct:
            return True
        return False