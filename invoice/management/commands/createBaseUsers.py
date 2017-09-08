from django.core.management.base import BaseCommand, CommandError
from invoice.models import Profile as User

from django.conf import settings


class Command(BaseCommand):
    help = 'Creates a super user'

    def handle(self, *args, **options):
        if not (settings.DEBUG or settings.STAGING):
            raise CommandError('You cannot run this command in production')

        User.objects.get_or_create('su', 'su@su.com', 'su', first_name='Super', last_name='User', is_superuser=True,
                                   is_staff=True)

        User.objects.get_or_create('staff', 'staff@staff.com', 'staff', first_name='Staff', last_name='User',
                                   is_staff=True)

        User.objects.get_or_create('basic', 'basic@casic.com', 'basic', first_name='Basic', last_name='User')