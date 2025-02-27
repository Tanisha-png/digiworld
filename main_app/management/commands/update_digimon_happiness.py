import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main_app.models import Digimon

class Command(BaseCommand):
    help = 'Update Digimon happiness with random values'

    def handle(self, *args, **options):
        # Get or create a default user
        user, created = User.objects.get_or_create(
            username='christianburroughs',
        )
        if created:
            user.set_password('123')
            user.save()

        # Retrieve all Digimon objects
        digimons = Digimon.objects.all()

        # Iterate through each Digimon and update happiness with a random value
        for digimon in digimons:
            # Generate a random happiness value (assuming it should be between 0 and 100)
            digimon.happiness = random.randint(0, 100)
            digimon.save()  # Save the updated Digimon instance

        self.stdout.write(self.style.SUCCESS('Successfully updated Digimon happiness values.'))