# Generated by Django 5.1.1 on 2024-09-17 18:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, null=True)),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('followers', models.ManyToManyField(blank=True, related_name='following_profiles', to=settings.AUTH_USER_MODEL)),
                ('following', models.ManyToManyField(blank=True, related_name='follower_profiles', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
