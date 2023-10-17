from django.core import management
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = "导入初始数据"
    
    def handle(self, *args, **options):
        baykeadposition = settings.BASE_DIR / 'baykeshop/conf/baykeadposition.json'
        baykeadspace = settings.BASE_DIR / 'baykeshop/conf/baykeadspace.json'
        baykeshopcategory = settings.BASE_DIR / 'baykeshop/conf/baykeshopcategory.json'
        management.call_command('loaddata', baykeadposition, verbosity=0)
        management.call_command('loaddata', baykeadspace, verbosity=0)
        management.call_command('loaddata', baykeshopcategory, verbosity=0)
        self.stdout.write(self.style.SUCCESS("数据导入成功！"))