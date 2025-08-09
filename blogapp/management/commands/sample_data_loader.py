from django.core.management.base import BaseCommand
from django.utils import timezone
from blogapp.models import User, Blog, Comments, Likes, Category
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Generate realistic sample data with Faker (100 users, 300+ blogs, 1000+ comments, 1500+ likes)'

    def handle(self, *args, **kwargs):
        # 🧹 Clear existing data except admin
        self.stdout.write(self.style.WARNING("🧹 Deleting old data..."))
        Likes.objects.all().delete()
        Comments.objects.all().delete()
        Blog.objects.all().delete()
        Category.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()
        self.stdout.write(self.style.SUCCESS("✅ Old data cleared."))

        # ✅ Create 100 Users
        users = []
        for _ in range(100):
            email = fake.unique.email()
            user = User.objects.create_user(
                email=email,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password="pass1234",
                is_active=True
            )
            users.append(user)
        self.stdout.write(self.style.SUCCESS("✅ Created 100 users with realistic names/emails."))

        # ✅ Create 5 Categories
        categories = []
        cat_names = ["Technology", "Health", "Travel", "Education", "Entertainment"]
        for name in cat_names:
            categories.append(Category.objects.create(category=name))
        self.stdout.write(self.style.SUCCESS("✅ Created 5 categories."))

        # ✅ Create 300 Blogs (3 per user)
        blogs = []
        for user in users:
            for _ in range(3):
                title = fake.sentence(nb_words=6)
                blog = Blog.objects.create(
                    title=title,
                    content=fake.paragraph(nb_sentences=10),
                    author=user,
                    category=random.choice(categories),
                    created_at=fake.date_time_this_year(),
                    updated_at=timezone.now()
                )
                blogs.append(blog)
        self.stdout.write(self.style.SUCCESS(f"✅ Created {len(blogs)} blogs with varied content."))

        # ✅ Create 900+ Comments (3 per blog)
        comment_count = 0
        for blog in blogs:
            for _ in range(3):
                Comments.objects.create(
                    comment=fake.sentence(),
                    blog=blog,
                    user=random.choice(users),
                    created_at=fake.date_time_this_month(),
                    updated_at=timezone.now()
                )
                comment_count += 1
        self.stdout.write(self.style.SUCCESS(f"✅ Created {comment_count} comments."))

        # ✅ Create 1500+ Likes (4–6 per blog)
        like_count = 0
        for blog in blogs:
            likers = random.sample(users, k=random.randint(4, 6))
            for liker in likers:
                if not Likes.objects.filter(blog=blog, user=liker).exists():
                    Likes.objects.create(
                        blog=blog,
                        user=liker,
                        created_at=fake.date_time_this_month()
                    )
                    like_count += 1
        self.stdout.write(self.style.SUCCESS(f"✅ Created {like_count} likes."))

        self.stdout.write(self.style.SUCCESS("🎉 Realistic sample data generation complete!"))
