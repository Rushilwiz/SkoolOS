# Generated by Django 3.0.7 on 2020-06-08 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20200608_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deffiles',
            name='path',
            field=models.CharField(max_length=100),
        ),
    ]
