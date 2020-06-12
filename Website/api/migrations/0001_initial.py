# Generated by Django 3.0.7 on 2020-06-12 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('due_date', models.DateTimeField()),
                ('files', models.CharField(blank=True, default='', max_length=100)),
                ('path', models.CharField(max_length=100)),
                ('classes', models.CharField(max_length=100)),
                ('teacher', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('repo', models.URLField(default='')),
                ('path', models.CharField(default='', max_length=100)),
                ('teacher', models.CharField(default='', max_length=100)),
                ('assignments', models.CharField(default='', max_length=100)),
                ('default_file', models.CharField(default='', max_length=100)),
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
            name='Student',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('student_id', models.IntegerField()),
                ('ion_user', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('email', models.CharField(blank=True, default='', max_length=100)),
                ('grade', models.IntegerField()),
                ('git', models.CharField(max_length=100)),
                ('repo', models.URLField(blank=True, default='')),
                ('classes', models.CharField(blank=True, default='', max_length=100)),
                ('added_to', models.CharField(blank=True, default='', max_length=100)),
                ('completed', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('classes', models.CharField(blank=True, default='', max_length=100)),
                ('ion_user', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('git', models.CharField(max_length=100)),
                ('email', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
    ]
