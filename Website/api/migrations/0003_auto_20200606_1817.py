# Generated by Django 3.0.7 on 2020-06-06 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200606_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='classes',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='api.Classes'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assignment',
            name='students',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='api.Student'),
            preserve_default=False,
        ),
    ]