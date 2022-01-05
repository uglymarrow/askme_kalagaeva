
from django.core.management.base import BaseCommand
from app.models import *
from django.db.models import F
from random import choice
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Fills database with fake data'

    avatar_list = ['1.png', '2.jpeg', '3.jpg', '4.jpg', '5.jpg', '5.jpg', '6.jpg', '7.jpeg',
                   '8.jpg', '9.jpg', '10.jpg', '11.jpg', '12.jpg', '13.jpg', '14.jpg', '15.png',
                   '16.jpg', '17.jpg', '18.jpg', '19.jpg', 'memnaruto.png', 'memtsunade.jpg']

    def add_arguments(self, parser):
        parser.add_argument('--db_size', default='small', type=str, help='The size of database data to create.')

    def fill_profiles(self, cnt):
        usernames = set()
        profiles = []
        for i in range(cnt):
            # username = fake.simple_profile().get('username')
            username = fake.unique.word

            while username in usernames:
                # username = fake.simple_profile().get('username')
                username = fake.unique.word

            user = User.objects.create(
                username=username,
                password=fake.password(length=9, special_chars=True)
            )
            profiles.append(Profile(
                user_id=user.id,
                nickname=fake.word(),
                avatar=choice(self.avatar_list)
            ))
            usernames.add(username)

        Profile.objects.bulk_create(profiles)

    def fill_questions(self, cnt):
        author_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        tags_ids = list(
            Tag.objects.values_list(
                'id', flat=True
            )
        )
        questions = []
        for i in range(cnt):
            questions.append(Question(
                author_id=choice(author_ids),
                content=' '.join(fake.sentences(fake.random_int(min=5, max=15))),
                header=fake.sentence()[:-1] + '?',
                date=fake.date_between(start_date='-1y', end_date='today'),
            ))

        Question.objects.bulk_create(questions)
        for q in Question.objects.all():
            tag1 = Tag.objects.get(id=choice(tags_ids))
            tag2 = Tag.objects.get(id=choice(tags_ids))
            if tag1 != tag2:
                q.tags.add(tag1, tag2)
            else:
                q.tags.add(tag1)

    def fill_tags(self, cnt):
        tags = set()
        tags_list = []
        for i in range(cnt):
            tag = "tag"
            while tag in tags:
                tag += str(i)

                # tag += '_' + fake.unique().word
                # if len(tag) > 49:
                #     tag = fake.pystr(min_chars=2, max_chars=15)
            tags_list.append(Tag(
                name=tag,
            ))
            tags.add(tag)

        Tag.objects.bulk_create(tags_list)

    def fill_answers(self, cnt):
        author_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        questions_ids = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        answers = []
        for i in range(cnt):
            question_id = choice(questions_ids)
            answers.append(Answer(
                content=' '.join(fake.sentences(fake.random_int(min=5, max=10))),
                author_id=choice(author_ids),
                question_id=question_id,
                date=Question.objects.get(id=question_id).date
            ))
        Answer.objects.bulk_create(answers)


    def fill_question_likes(self, cnt):
        LIKE_CHOICES = [1, -1]
        questions_ids = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        author_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        question_likes = []
        for i in range(cnt):
            question_id = choice(questions_ids)
            like = choice(LIKE_CHOICES)
            question_likes.append(QuestLike(
                like=like,
                author_id=choice(author_ids),
                question_id=question_id
            ))
            # Question.objects.get(id=question_id).update(rating=F('rating') + like)
            Question.objects.get(id=question_id).rating=F('rating') + like

        QuestLike.objects.bulk_create(question_likes)

    def fill_answer_likes(self, cnt):
        LIKE_CHOICES = ['1', '-1']
        answers_ids = list(
            Answer.objects.values_list(
                'id', flat=True
            )
        )
        author_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        answers_likes = []
        for i in range(cnt):
            answers_likes.append(AnsLike(
                like=choice(LIKE_CHOICES),
                author_id=choice(author_ids),
                answer_id=choice(answers_ids)
            ))
        AnsLike.objects.bulk_create(answers_likes)

    def fill_rating(self):
        questions_ids = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        for id in questions_ids:
            rating = QuestLike.objects.filter(question_id=id).aggregate(sum=Sum('like'))
            if rating['sum']:
                Question.objects.filter(id=id).update(rating=rating['sum'])

    def handle(self, *args, **options):
        sizes = [10001, 11000, 100001, 1000001, 900000, 2000001]
        # sizes = [120, 130, 140, 150, 160, 170]

        self.fill_profiles(sizes[0])
        self.fill_tags(sizes[1])
        self.fill_questions(sizes[2])
        self.fill_answers(sizes[3])
        self.fill_question_likes(sizes[5])
        self.fill_answer_likes(sizes[5])
        self.fill_rating()
