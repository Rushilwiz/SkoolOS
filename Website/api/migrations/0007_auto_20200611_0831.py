# Generated by Django 3.0.7 on 2020-06-11 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20200610_0631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classes',
            name='id',
        ),
        migrations.AlterField(
            model_name='classes',
            name='name',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
