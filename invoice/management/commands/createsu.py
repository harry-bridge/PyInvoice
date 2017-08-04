from django.core.management.base import BaseCommand
from invoice.models import Profile as User

class Command(BaseCommand):
    help = 'Creates a super user'

    def handle(self, *args, **options):
        if not User.objects.filter(is_staff=True, is_superuser=True).exists():
            User.objects.create_superuser(
                'su', 'su@su.com', 'su', first_name='Super', last_name='User'
                )
