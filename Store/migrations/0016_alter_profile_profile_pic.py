# Generated by Django 3.2.3 on 2021-08-16 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0015_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='../static/img/'),
        ),
    ]
