import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Count


class QuestionManager(models.Manager):
    def popular(self):
        return self.prefetch_related('likes', 'author').order_by('-rating')

    def new_questions(self):
        return self.prefetch_related('likes', 'author').order_by('-date')

    def tagged(self, str):
        return self.prefetch_related('likes', 'author').filter(tags__name=str)


class AnswerManager(models.Manager):
    def all_ans(self, pk):
        return self.prefetch_related('likes', 'author').filter(question__id=pk).annotate(like_sum=Sum('likes__like'))


class TagManager(models.Manager):
    def popular(self):
        return self.annotate(count=Count('questions')).order_by('-count')


class ProfileManager(models.Manager):
    def best(self):
        return self.annotate(count=Count('answers')).order_by('-count')


class Question(models.Model):
    header = models.CharField(max_length=255)
    content = models.TextField()
    date = models.DateField(db_index=True)
    rating = models.IntegerField(default=0, db_index=True)
    author = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, related_name='questions')
    tags = models.ManyToManyField('Tag', related_name='questions', blank=True)
    objects = QuestionManager()

    def __str__(self):
        return self.header


class Answer(models.Model):
    content = models.TextField()
    date = models.DateField()
    author = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(
        'Question', on_delete=models.CASCADE, related_name='answers')
    checked = models.BooleanField(default=False)
    objects = AnswerManager()

    def __str__(self):
        return self.content


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=255)
    avatar = models.ImageField()
    objects = ProfileManager()

    def __str__(self):
        return self.nickname


class QuestLike(models.Model):
    LIKE_VALUE = [
        (1, 'pos'),
        (-1, 'neg')
    ]
    like = models.IntegerField(choices=LIKE_VALUE, default=0)
    question = models.ForeignKey(
        'Question', on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.like) + ' ' + self.question.__str__()


class AnsLike(models.Model):
    LIKE_VALUE = [
        (1, 'pos'),
        (-1, 'neg')
    ]
    like = models.IntegerField(choices=LIKE_VALUE, default=0)
    answer = models.ForeignKey(
        'Answer', on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(
        'Profile', on_delete=models.CASCADE,  default="None")

    def __str__(self):
        return str(self.like) + ' ' + self.answer.__str__()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    objects = TagManager()

    def __str__(self):
        return self.name
