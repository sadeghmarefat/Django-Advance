
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker

from accounts.models import Profile

User = get_user_model()


class Command(BaseCommand):
    help = "Create fake users and profiles"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=1,
        )

    def handle(self, *args, **options):
        fake = Faker()
        count = options["count"]
        password = "Test123456"

        for _ in range(count):
            email = fake.unique.email()

            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=fake.first_name(),
                is_verified=True,
            )

            profile = user.profile
            profile.last_name = fake.last_name()
            profile.bio = fake.text(max_nb_chars=150)
            profile.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"{count} users created successfully."
            )
        )
