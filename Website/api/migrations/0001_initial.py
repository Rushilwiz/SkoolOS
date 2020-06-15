# Generated by Django 3.0.7 on 2020-06-14 23:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('description', models.CharField(default='Class Description', max_length=500)),
                ('repo', models.URLField(blank=True, default='')),
                ('path', models.CharField(default='', max_length=100)),
                ('assignments', models.TextField(blank=True, default='')),
                ('default_file', models.CharField(blank=True, default='', max_length=100)),
                ('confirmed', models.TextField(blank=True, default='')),
                ('unconfirmed', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='DefFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('path', models.CharField(max_length=100)),
                ('assignment', models.CharField(default='', max_length=100)),
                ('classes', models.CharField(max_length=100)),
                ('teacher', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('git', models.CharField(blank=True, default='', max_length=100)),
                ('classes', models.ManyToManyField(to='api.Class')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField(blank=True, default=0)),
                ('git', models.CharField(blank=True, default='', max_length=100)),
                ('repo', models.URLField(blank=True, default='')),
                ('classes', models.CharField(blank=True, default='', max_length=100)),
                ('added_to', models.CharField(blank=True, default='', max_length=100)),
                ('completed', models.TextField(blank=True, default='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('due_date', models.DateTimeField()),
                ('files', models.CharField(blank=True, default='', max_length=100)),
                ('path', models.CharField(max_length=100)),
                ('classes', models.CharField(max_length=100)),
                ('teacher', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
