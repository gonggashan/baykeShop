# Generated by Django 4.2.4 on 2023-10-25 13:05

import baykeshop.common.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaykeShopBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='删除标记')),
                ('name', models.CharField(max_length=100, verbose_name='品牌名称')),
                ('desc', models.CharField(blank=True, default='', max_length=150, verbose_name='品牌描述')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='brand_logos/', verbose_name='品牌标志')),
            ],
            options={
                'verbose_name': '品牌',
                'verbose_name_plural': '品牌',
                'ordering': ['-add_date'],
            },
        ),
        migrations.CreateModel(
            name='BaykeShopCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='删除标记')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('icon', models.ImageField(blank=True, max_length=200, null=True, upload_to='shop/category', verbose_name='图标')),
                ('figure', models.ImageField(blank=True, max_length=200, null=True, upload_to='shop/category', verbose_name='形象图')),
                ('sort', models.PositiveSmallIntegerField(default=1, verbose_name='排序')),
                ('is_nav', models.BooleanField(default=True, verbose_name='推荐')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.baykeshopcategory', verbose_name='父类')),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
                'ordering': ['sort'],
            },
        ),
        migrations.CreateModel(
            name='BaykeShopOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='删除标记')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, '待付款'), (2, '待发货'), (3, '待收货'), (4, '待评价'), (5, '已完成'), (6, '已关闭'), (7, '退款中')], default=1, verbose_name='订单状态')),
                ('paymethod', models.PositiveSmallIntegerField(blank=True, choices=[(None, '(Unknown)'), (1, '支付宝支付'), (2, '微信支付'), (3, '余额支付')], null=True, verbose_name='支付方式')),
                ('order_sn', models.CharField(blank=True, max_length=100, verbose_name='订单号')),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, verbose_name='总价')),
                ('mark', models.CharField(blank=True, default='', max_length=150, verbose_name='订单备注')),
                ('name', models.CharField(blank=True, default='', max_length=50, verbose_name='签收人')),
                ('phone', models.CharField(blank=True, default='', max_length=11, validators=[baykeshop.common.validators.validate_phone], verbose_name='手机号')),
                ('email', models.EmailField(blank=True, default='', max_length=50, verbose_name='邮箱')),
                ('address', models.CharField(blank=True, default='', max_length=200, verbose_name='收货地址')),
                ('pay_time', models.DateTimeField(blank=True, editable=False, help_text='支付时间', null=True, verbose_name='支付时间')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '订单',
                'verbose_name_plural': '订单',
                'ordering': ['-add_date'],
                'permissions': [('send_out_goods', 'send out goods')],
            },
        ),
        migrations.CreateModel(
            name='BaykeShopSpec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='删除标记')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
            ],
            options={
                'verbose_name': '规格',
                'verbose_name_plural': '规格',
                'ordering': ['-add_date'],
            },
        ),
        migrations.CreateModel(
            name='BaykeShopSPU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='删除标记')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('subtitle', models.CharField(blank=True, default='', max_length=150, verbose_name='副标题')),
                ('content', tinymce.fields.TinyMCEField(verbose_name='详情')),
                ('unit', models.CharField(blank=True, default='', max_length=50, verbose_name='单位')),
                ('shipping_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, verbose_name='运费')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shop.baykeshopbrand', verbose_name='商品品牌')),
                ('category', models.ManyToManyField(blank=True, to='shop.baykeshopcategory', verbose_name='商品分类')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
                'ordering': ['-add_date'],
            },
        ),
        migrations.CreateModel(
            name='BaykeShopSPUAtlas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='删除标记')),
                ('img', models.ImageField(height_field='width', max_length=200, upload_to='spu/%Y/%m', verbose_name='商品轮播图', width_field='height')),
                ('width', models.PositiveSmallIntegerField(blank=True, default=500, verbose_name='图片宽度')),
                ('height', models.PositiveSmallIntegerField(blank=True, default=500, verbose_name='图片高度')),
                ('sort', models.PositiveSmallIntegerField(default=1, verbose_name='排序')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
                ('spu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.baykeshopspu', verbose_name='商品')),
            ],
            options={
                'verbose_name': '商品轮播图',
                'verbose_name_plural': '商品轮播图',
                'ordering': ['sort'],
            },
        ),
        migrations.CreateModel(
            name='BaykeShopSpecValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='删除标记')),
                ('value', models.CharField(max_length=50, verbose_name='规格值')),
                ('spec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.baykeshopspec', verbose_name='规格')),
            ],
            options={
                'verbose_name': '规格值',
                'verbose_name_plural': '规格值',
                'ordering': ['add_date'],
            },
        ),
        migrations.CreateModel(
            name='BaykeShopSKU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='删除标记')),
                ('img', models.ImageField(max_length=200, upload_to='shop/sku', verbose_name='主图')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='售价')),
                ('cost_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='成本价')),
                ('discount_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='划线价')),
                ('stock', models.PositiveSmallIntegerField(default=0, verbose_name='库存')),
                ('sales', models.PositiveSmallIntegerField(default=0, verbose_name='销量')),
                ('code', models.CharField(blank=True, default='', max_length=20, verbose_name='商品编码')),
                ('volume', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, verbose_name='体积')),
                ('weight', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, verbose_name='重量')),
                ('specs', models.JSONField(blank=True, default=dict, verbose_name='规格数据')),
                ('spu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.baykeshopspu', verbose_name='SPU')),
            ],
            options={
                'verbose_name': '商品规格',
                'verbose_name_plural': '商品规格',
                'ordering': ['price'],
            },
        ),
        migrations.CreateModel(
            name='BaykeShopOrderSKU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='删除标记')),
                ('count', models.PositiveSmallIntegerField(default=1, verbose_name='数量')),
                ('sku_json', models.JSONField(blank=True, default=dict, verbose_name='商品快照')),
                ('is_commented', models.BooleanField(default=False, verbose_name='是否已评价')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.baykeshoporder', verbose_name='订单')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.baykeshopsku', verbose_name='商品规格')),
            ],
            options={
                'verbose_name': '订单商品',
                'verbose_name_plural': '订单商品',
                'ordering': ['-add_date'],
            },
        ),
        migrations.CreateModel(
            name='BaykeShopCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='删除标记')),
                ('num', models.PositiveSmallIntegerField(default=1, verbose_name='数量')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.baykeshopsku', verbose_name='规格')),
            ],
            options={
                'verbose_name': '购物车',
                'verbose_name_plural': '购物车',
                'ordering': ['-add_date'],
            },
        ),
        migrations.CreateModel(
            name='BaykeAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='删除标记')),
                ('name', models.CharField(max_length=50, verbose_name='签收人')),
                ('phone', models.CharField(max_length=11, verbose_name='手机号')),
                ('email', models.EmailField(blank=True, default='', max_length=50, verbose_name='邮箱')),
                ('province', models.CharField(max_length=150, verbose_name='省')),
                ('city', models.CharField(max_length=150, verbose_name='市')),
                ('county', models.CharField(max_length=150, verbose_name='区/县')),
                ('address', models.CharField(max_length=150, verbose_name='详细地址')),
                ('is_default', models.BooleanField(default=False, verbose_name='设为默认')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '收货地址',
                'verbose_name_plural': '收货地址',
                'ordering': ['-add_date'],
            },
        ),
        migrations.AddConstraint(
            model_name='baykeshoporder',
            constraint=models.UniqueConstraint(models.F('owner'), models.F('order_sn'), name='unique_owner_order'),
        ),
        migrations.AddConstraint(
            model_name='baykeshopcart',
            constraint=models.UniqueConstraint(models.F('owner'), models.F('sku'), name='unique_owner_sku'),
        ),
    ]
