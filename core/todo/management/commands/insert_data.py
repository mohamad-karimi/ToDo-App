from django.core.management.base import BaseCommand
import random
from faker import Faker
from todo.models import Tasks
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "insert the fake data for task to the data base"

    def __init__(
        self, stdout=None, stderr=None, no_color=None, force_color=None
    ):
        super().__init__(stdout, stderr, no_color, force_color)
        self.fake = Faker()

    def handle(self, *args, **options):

        user, created = User.objects.get_or_create(
            username="ahmad",
            email="testfakedata@gmail.com",
        )

        if created:
            user.set_password("@1234567")
            user.save()

        for _ in range(5):
            Tasks.objects.create(
                user=user,
                title=self.fake.paragraph(nb_sentences=1),
                completed=random.choice([True, False]),
            )

        self.stdout.write(
            self.style.SUCCESS("Fake data created successfully!")
        )
