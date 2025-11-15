from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by('-id')
    
    def hot_questions(self):
        return self.order_by('-rating')
    
    def by_tag(self, tag_name):
        return self.filter(tags__name=tag_name).order_by('-rating')

class Question(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    rating = models.IntegerField(default=0)

    objects = QuestionManager()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('question', kwargs={'question_id': self.id})

class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer to {self.question.title}"

class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=[(1, 'Like'), (-1, 'Dislike')])

    class Meta:
        unique_together = ['user', 'question']

    def save(self, *args, **kwargs):
        if self.value not in [1, -1]:
            raise ValidationError("Value must be 1 (like) or -1 (dislike)")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} {'liked' if self.value == 1 else 'disliked'} {self.question.title}"

class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=[(1, 'Like'), (-1, 'Dislike')])

    class Meta:
        unique_together = ['user', 'answer']

    def save(self, *args, **kwargs):
        if self.value not in [1, -1]:
            raise ValidationError("Value must be 1 (like) or -1 (dislike)")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} {'liked' if self.value == 1 else 'disliked'} answer #{self.answer.id}"