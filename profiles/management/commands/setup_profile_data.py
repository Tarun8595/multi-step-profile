from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Setup initial data for profile application'

    def handle(self, *args, **options):
        self.stdout.write('Setting up profile application data...')
        
        # Run migrations first
        self.stdout.write('Running migrations...')
        call_command('migrate')
        
        # Populate locations
        self.stdout.write('Populating location data...')
        call_command('populate_locations')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully set up profile application data!')
        )
