from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    question_detail_text = models.TextField()

    def __str__(self):
        return self.question_text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()

    def __str__(self):
        return "Ответ на вопрос ID=" + str(self.question_id)
# Create your models here.
