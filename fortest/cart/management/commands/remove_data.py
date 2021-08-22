from django.core.management.base import BaseCommand, CommandError
from cart.models import FinalizedOrders
import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        count =0
        factors = FinalizedOrders.objects.filter(payment=False)
        now = datetime.datetime.now()
        for factor in factors:
            factor_created = factor.created.replace(tzinfo=None)
            if (now - factor_created).days >= 1:
                factor.delete()
                count += 1
            else:
                pass
        self.stdout.write(f'\n{count} factors delete from database!')