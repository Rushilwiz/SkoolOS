# Generated by Django 3.0.7 on 2020-06-06 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20200606_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='classes',
            name='assignments',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Assignment'),
        ),
    ]
