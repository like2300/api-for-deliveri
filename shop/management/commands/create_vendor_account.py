from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from shop.models import Boutique, VendorUser


class Command(BaseCommand):
    help = 'Create a new vendor account with an initial password'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username for the vendor account')
        parser.add_argument('--email', type=str, help='Email for the vendor account (optional)')
        parser.add_argument('--boutique-name', type=str, help='Name of the boutique')
        parser.add_argument('--description', type=str, help='Description of the boutique')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        boutique_name = options['boutique_name']
        description = options['description']

        if not username or not boutique_name:
            self.stdout.write(
                self.style.ERROR('Both username and boutique-name are required!')
            )
            return

        # Generate a random initial password
        initial_password = get_random_string(length=12)
        
        # Create the vendor user
        vendor_user = VendorUser.objects.create_user(
            username=username,
            email=email or '',
            password=initial_password
        )
        
        # Create the boutique and associate it with the vendor user
        boutique = Boutique.objects.create(
            name=boutique_name,
            description=description or f'Boutique for {username}',
            image='boutique_images/default.jpg'  # Placeholder image
        )
        
        # Link the boutique to the vendor user
        boutique.owner = vendor_user
        boutique.save()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created vendor account "{username}" with boutique "{boutique_name}"\n'
                f'Initial password: {initial_password}\n'
                f'The vendor should change this password after first login.'
            )
        )