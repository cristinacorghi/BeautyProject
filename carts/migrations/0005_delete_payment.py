# Generated by Django 3.2.3 on 2021-08-11 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0004_alter_payment_phone_number'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Payment',
        ),
    ]