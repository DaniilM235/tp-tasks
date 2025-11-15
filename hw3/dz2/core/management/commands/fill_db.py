from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Fill database with sample data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio for data generation')

    def handle(self, *args, **options):
        ratio = options['ratio']
        
        self.stdout.write(f'Starting to fill database with ratio {ratio}...')

        sample_texts = [
            "This is a sample question about programming and software development.",
            "How to implement efficient algorithms for large datasets?",
            "Best practices for database design and optimization.",
            "Understanding machine learning concepts and applications.",
            "Web development frameworks comparison and use cases.",
            "Mobile app development trends and technologies.",
            "Cloud computing services and deployment strategies.",
            "Cybersecurity measures for modern applications.",
            "DevOps practices and continuous integration.",
            "Artificial intelligence in everyday applications."
        ]
        
        sample_answers = [
            "Great question! Here's a detailed explanation based on my experience...",
            "I've encountered this issue before. The solution involves several steps...",
            "Based on the latest research, here are the best approaches...",
            "This is a common problem. Let me break it down for you...",
            "There are multiple ways to solve this. Here's the most efficient one...",
            "I recommend checking the official documentation for this...",
            "From my practical experience, here's what works best...",
            "This requires understanding the underlying principles...",
            "Here's a step-by-step guide to help you solve this...",
            "The key aspects to consider are the following..."
        ]
        

        users = []
        for i in range(ratio):
            username = f'user_{i}'
            user = User.objects.create_user(
                username=username,
                email=f'{username}@example.com',
                password='password123'
            )
            Profile.objects.create(user=user)
            users.append(user)
            if i % 100 == 0:
                self.stdout.write(f'Created {i} users...')
        

        tags = []
        for i in range(ratio):
            tag = Tag.objects.create(name=f'tag_{i}')
            tags.append(tag)
        

        questions = []
        base_date = datetime.now()
        for i in range(ratio * 10):
            author = random.choice(users)
            days_ago = random.randint(0, 365)
            created_date = base_date - timedelta(days=days_ago)
            
            question = Question.objects.create(
                title=f"Question #{i}: {random.choice(sample_texts)[:50]}",
                text=random.choice(sample_texts) * random.randint(1, 5),
                author=author,
                rating=random.randint(-10, 100),
                created_at=created_date
            )
            

            question_tags = random.sample(tags, min(3, len(tags)))
            question.tags.set(question_tags)
            questions.append(question)
            
            if i % 1000 == 0:
                self.stdout.write(f'Created {i} questions...')
        

        answers = []
        for i in range(ratio * 100):
            question = random.choice(questions)
            author = random.choice(users)
            days_ago = random.randint(0, 365)
            created_date = base_date - timedelta(days=days_ago)
            
            answer = Answer.objects.create(
                text=random.choice(sample_answers) * random.randint(1, 3),
                question=question,
                author=author,
                rating=random.randint(-5, 50),
                is_correct=random.choice([True, False]),
                created_at=created_date
            )
            answers.append(answer)
            
            if i % 10000 == 0:
                self.stdout.write(f'Created {i} answers...')
        

        question_likes_created = 0
        for user in users:
            user_questions = random.sample(questions, min(ratio * 2, len(questions)))
            for question in user_questions:
                try:
                    QuestionLike.objects.create(
                        user=user,
                        question=question,
                        value=random.choice([1, -1])
                    )
                    question_likes_created += 1
                except:
                    pass
        
        answer_likes_created = 0
        for user in users:
            user_answers = random.sample(answers, min(ratio * 20, len(answers)))
            for answer in user_answers:
                try:
                    AnswerLike.objects.create(
                        user=user,
                        answer=answer,
                        value=random.choice([1, -1])
                    )
                    answer_likes_created += 1
                except:
                    pass 
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully filled database:\n'
                f'- Users: {len(users)}\n'
                f'- Tags: {len(tags)}\n'
                f'- Questions: {len(questions)}\n'
                f'- Answers: {len(answers)}\n'
                f'- Question likes: {question_likes_created}\n'
                f'- Answer likes: {answer_likes_created}'
            )
        )