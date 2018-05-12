from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
import random

from invoice import models


class Command(BaseCommand):
    help = 'Creates some sample data to use for testing'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.user = models.Profile.objects.get(username='super')

    def handle(self, *args, **options):
        from django.conf import settings

        if not (settings.DEBUG or settings.STAGING):
            raise CommandError('You cannot run this command in production')

        random.seed('Some object to seed the random number generator')  # otherwise it is done by time, which could lead to inconsistant tests

        self.create_companies()
        self.create_invoices()
        self.create_expense_groups()
        self.create_expenses()
        self.update_user_profile()

    def create_companies(self):
        company_names = ["Acme, inc.","Widget Corp","123 Warehousing","Demo Company","Smith and Co.","Foo Bars","ABC Telecom","Fake Brothers","QWERTY Logistics","Demo, inc.","Sample Company","Sample, inc","Acme Corp","Allied Biscuit","Ankh-Sto Associates","Extensive Enterprise","Galaxy Corp","Globo-Chem","Mr. Sparkle","Globex Corporation","LexCorp","LuthorCorp","North Central Positronics","Omni Consimer Products","Praxis Corporation","Sombra Corporation","Sto Plains Holdings","Tessier-Ashpool","Wayne Enterprises","Wentworth Industries","ZiffCorp","Bluth Company","Strickland Propane","Thatherton Fuels","Three Waters","Water and Power","Western Gas & Electric","Mammoth Pictures","Mooby Corp","Gringotts","Thrift Bank","Flowers By Irene","The Legitimate Businessmens Club","Osato Chemicals","Transworld Consortium","Universal Export","United Fried Chicken","Virtucon","Kumatsu Motors","Keedsler Motors","Powell Motors","Industrial Automation","Sirius Cybernetics Corporation","U.S. Robotics and Mechanical Men","Colonial Movers","Corellian Engineering Corporation","Incom Corporation","General Products","Leeding Engines Ltd.","Blammo","Input, Inc.","Mainway Toys","Videlectrix","Zevo Toys","Ajax","Axis Chemical Co.","Barrytron","Carrys Candles","Cogswell Cogs","Spacely Sprockets","General Forge and Foundry","Duff Brewing Company","Dunder Mifflin","General Services Corporation","Monarch Playing Card Co.","Krustyco","Initech","Roboto Industries","Primatech","Sonky Rubber Goods","St. Anky Beer","Stay Puft Corporation","Vandelay Industries","Wernham Hogg","Gadgetron","Burleigh and Stronginthearm","BLAND Corporation","Nordyne Defense Dynamics","Petrox Oil Company","Roxxon","McMahon and Tate","Sixty Second Avenue","Charles Townsend Agency","Spade and Archer","Megadodo Publications","Rouster and Sideways","C.H. Lavatory and Sons","Globo Gym American Corp","The New Firm","SpringShield","Compuglobalhypermeganet","Data Systems","Gizmonic Institute","Initrode","Taggart Transcontinental","Atlantic Northern","Niagular","Plow King","Big Kahuna Burger","Big T Burgers and Fries","Chez Quis","Chotchkies","The Frying Dutchman","Klimpys","The Krusty Krab","Monks Diner","Milliways","Minuteman Cafe","Taco Grande","Tip Top Cafe","Moes Tavern","Central Perk","Chasers"]

        company_addresses = ['Somewhere in Birmingham', 'The Moon', 'My Mate\'s Garage']
        company_emails = ['lmclean0@about.com','akalker1@telegraph.co.uk','adanbrook2@blog.com','rbream3@whitehouse.gov','hmaurice4@pen.io','eatty5@patch.com','afranz6@independent.co.uk','jbeazleigh7@illinois.edu','isaltsberger8@prlog.org','ajurisic9@cbc.ca']

        person_names = ['Angelo Hearl','Celisse Lionel','Reid Poynor','Ervin Hamlen','Hamil Botha','Emery Laycock','Brandice Gaishson','Toma Kiloh','Marie-ann Conley','Teddie Ahern']
        person_phone = ['8646257126','2217858480','5122970073','6439517819']

        for i in range(10):
            models.Company.objects.create(
                name=random.choice(company_names),
                address=company_addresses[i % len(company_addresses)],
                email=company_emails[i % len(company_emails)],
                person=random.choice(person_names),
                phone=random.choice(person_phone)
                )

    def create_invoices(self):
        invoice_items = ['Some lights and PA', 'Get-out in a muddy field', 'Boring show call', 'Corproate job in Manchester', 'Dealing in child actors', 'Literal waste of my time']

        for i in range(30):  # Create 10 random invoices
            company = random.choice(models.Company.objects.all())

            invoice = models.Invoice.objects.create(
                user=self.user,
                company=company,
            )

            if i % 3 == 0:
                invoice.paid = True

            if i % 5 == 0:
                invoice.utr = True

            if i % 4 == 0:
                invoice.sent_date = timezone.now() - timezone.timedelta(days=random.randint(0, 50))

            if i % 10 == 0:
                invoice.is_quote = True

            invoice.save()

            for j in range(random.randint(2, 8)):  # Create a random number of items
                models.InvoiceItem.objects.create(
                    invoice=invoice,
                    description=random.choice(invoice_items),
                    quantity=random.randint(1, 20),
                    cost=random.randint(5, 200) / 1.25,   # Coerce that to a float
                )

    def create_expense_groups(self):
        groups = ['Uni Group', 'Random jobs', 'Things I didn\'t need', 'Explosives and stuff']

        for i in enumerate(groups):
            models.ExpenseGroup.objects.create(
                name=i[1]
            )

    def create_expenses(self):
        expense_items = ['Some petrols', 'Tools n stuff', 'Random bits of metal', 'Strippers (wire)', 'Last minute posters', 'Fixing things people broke']
        groups = models.ExpenseGroup.objects.all()

        for i in range(100):
            invoice = random.choice(models.Invoice.objects.all())

            expense = models.Expense.objects.create(
                invoice=invoice,
                description=random.choice(expense_items),
                cost=random.randint(5, 100) / 1.25,   # Coerce that to a float
            )

            if i % 5 == 0:
                expense.group = random.choice(groups)

            expense.save()

    def update_user_profile(self):
        self.user.address = 'Number 17\nBehind The Bins\nBarnaby Street'
        self.user.phone = '0123456789'
        self.user.utr = 1231234

        self.user.bank = 'Fake Bank'
        self.user.sort_code = '01-02-03'
        self.user.account_number = '98738492'

        self.user.save()
