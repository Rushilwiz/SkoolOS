# Generated by Django 3.0.7 on 2020-06-14 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='isStudent',
            field=models.BooleanField(default=True),
        ),
    ]