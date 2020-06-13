# Generated by Django 3.0.7 on 2020-06-13 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.TextField()),
                ('email', models.TextField()),
                ('first_name', models.TextField()),
                ('last_name', models.TextField()),
                ('isStudent', models.BooleanField()),
                ('token', models.CharField(max_length=255)),
            ],
        ),
    ]
