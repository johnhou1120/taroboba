# Generated by Django 3.2.8 on 2022-02-16 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_coupon_duedate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
    ]