# Generated by Django 3.1.5 on 2021-01-29 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_details_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact_book',
            name='contact_number',
            field=models.BigIntegerField(),
        ),
    ]
