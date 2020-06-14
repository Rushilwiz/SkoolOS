# Generated by Django 3.0.7 on 2020-06-14 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='website',
        ),
        migrations.AddField(
            model_name='student',
            name='added_to',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='student',
            name='classes',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='student',
            name='completed',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='student',
            name='git',
            field=models.CharField(blank=True, default='https://github.com/', max_length=100),
        ),
        migrations.AddField(
            model_name='student',
            name='grade',
            field=models.IntegerField(blank=True, default=9),
        ),
        migrations.AddField(
            model_name='student',
            name='repo',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='student',
            name='student_id',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]