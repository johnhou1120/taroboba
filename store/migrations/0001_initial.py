# Generated by Django 3.2.8 on 2022-02-16 13:23

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('comments', models.TextField(blank=True, null=True)),
                ('startdate', models.DateField(default=datetime.date.today)),
                ('duedate', models.DateField(default=datetime.date.today)),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='ActivityType',
            fields=[
                ('code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('comments', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('code', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=25)),
                ('comments', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('discount_percent', models.FloatField(blank=True, null=True)),
                ('discount_amount', models.FloatField(blank=True, null=True)),
                ('miniconsump', models.FloatField(blank=True, null=True)),
                ('used', models.BooleanField(default=False)),
                ('duedate', models.DateTimeField(default=datetime.date(2022, 5, 17))),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity', to='store.activity')),
            ],
        ),
        migrations.CreateModel(
            name='Grouping',
            fields=[
                ('ref_code', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='g_coupon', to='store.coupon')),
            ],
            options={
                'ordering': ['ref_code'],
            },
        ),
        migrations.CreateModel(
            name='Options',
            fields=[
                ('code', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=20)),
                ('type', models.CharField(max_length=20)),
                ('price', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['short'],
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('lineid', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=25)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('birthday', models.DateTimeField(blank=True, null=True)),
                ('followdate', models.DateTimeField(default=django.utils.timezone.now)),
                ('mambercard', models.CharField(blank=True, max_length=25, null=True)),
                ('einvoice', models.CharField(blank=True, max_length=25, null=True)),
            ],
            options={
                'ordering': ['-followdate'],
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('storeid', models.CharField(max_length=25, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=25)),
                ('address', models.TextField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('state', models.BooleanField(default=False)),
                ('comments', models.TextField(blank=True, null=True)),
                ('payment', models.ManyToManyField(to='store.Payment')),
            ],
            options={
                'ordering': ['storeid'],
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('code', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=20)),
                ('price', models.PositiveIntegerField()),
                ('discount', models.PositiveIntegerField()),
                ('comments', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(null=True, upload_to='')),
                ('state', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='store.category')),
                ('enableoptions', models.ManyToManyField(blank=True, to='store.Options')),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('addition', models.ManyToManyField(to='store.Options')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.products')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('ref_code', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('pickupmethod', models.CharField(blank=True, choices=[('Pickup', '自取'), ('Delivery', '外送')], max_length=20, null=True)),
                ('status', models.CharField(choices=[('ordering', '訂購中'), ('sending', '下單中'), ('preparing', '接單準備中'), ('ready', '準備就緒'), ('delivering', '外送中'), ('finished', '訂單完成')], default='ordering', max_length=20)),
                ('paystate', models.BooleanField(default=False)),
                ('receiver', models.CharField(blank=True, max_length=20, null=True)),
                ('receiverphone', models.CharField(blank=True, max_length=20, null=True)),
                ('receiveraddress', models.TextField(blank=True, null=True)),
                ('invoice', models.CharField(choices=[('P', '實體發票'), ('M', '會員載具'), ('E', '手機載具'), ('D', '愛心捐贈')], default='P', max_length=1)),
                ('isgrouping', models.BooleanField(default=False)),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='o_coupon', to='store.coupon')),
                ('groupmamber', models.ManyToManyField(to='store.Grouping')),
                ('items', models.ManyToManyField(to='store.OrderItems')),
                ('paymethod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='paymethod', to='store.payment', to_field='short')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='o_user', to='store.users')),
            ],
            options={
                'ordering': ['ref_code'],
            },
        ),
        migrations.AddField(
            model_name='grouping',
            name='items',
            field=models.ManyToManyField(to='store.OrderItems'),
        ),
        migrations.AddField(
            model_name='grouping',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='g_user', to='store.users'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='store.users'),
        ),
        migrations.AddField(
            model_name='activity',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.activitytype'),
        ),
    ]
