from django.core import management
from django.core.management.base import BaseCommand, CommandError

from django.conf import settings


class Command(BaseCommand):
    help = "导出初始数据"
    
    def handle(self, *args, **options):
        baykeadposition = settings.BASE_DIR / 'baykeshop/conf/baykeadposition.json'
        baykeadspace = settings.BASE_DIR / 'baykeshop/conf/baykeadspace.json'
        baykeshopcategory = settings.BASE_DIR / 'baykeshop/conf/baykeshopcategory.json'
        management.call_command('dumpdata', 'system.baykeadposition', output=baykeadposition, indent=2, format='json')
        management.call_command('dumpdata', 'system.baykeadspace', output=baykeadspace, indent=2, format='json')
        management.call_command('dumpdata', 'shop.baykeshopcategory', output=baykeshopcategory, indent=2, format='json')
        self.stdout.write(self.style.SUCCESS(f"数据导出成功，导出数据路径在{settings.BASE_DIR / 'baykeshop/conf'}文件夹下"))