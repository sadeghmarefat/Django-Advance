
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from faker import Faker
from blog.models import Post, Category


User = get_user_model()


class Command(BaseCommand):
    help = "Create fake blog categories and posts"

    def add_arguments(self, parser):
        parser.add_argument(
            "--posts",
            type=int,
            default=10,
        )
        parser.add_argument(
            "--categories",
            type=int,
            default=2,
        )

    def handle(self, *args, **options):
        fake = Faker()

        post_count = options["posts"]
        category_count = options["categories"]

        # Create categories
        categories = []

        for _ in range(category_count):
            category = Category.objects.create(
                name=fake.unique.sentence(nb_words=2).rstrip(".")
            )
            categories.append(category)

        # Get users
        users = list(User.objects.filter(is_active=True))

        if not users:
            self.stdout.write(
                self.style.ERROR(
                    "No active users found. Create users first."
                )
            )
            return

        # Create posts
        for _ in range(post_count):
            Post.objects.create(
                author=fake.random_element(users),
                title=fake.sentence(nb_words=6),
                content=fake.paragraph(nb_sentences=10),
                status=fake.boolean(chance_of_getting_true=70),
                category=fake.random_element(categories)
                if categories
                else None,
                published_at=fake.date_time_between(
                    start_date="-1y",
                    end_date="now",
                    tzinfo=timezone.get_current_timezone(),
                ),
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {category_count} categories "
                f"and {post_count} posts successfully."
            )
        )
