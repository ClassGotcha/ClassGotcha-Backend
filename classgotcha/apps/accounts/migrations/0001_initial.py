# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-10 19:08
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
                name='Account',
                fields=[
                    ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('password', models.CharField(max_length=128, verbose_name='password')),
                    ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                    ('is_superuser', models.BooleanField(default=False,
                                                         help_text='Designates that this user has all permissions without explicitly assigning them.',
                                                         verbose_name='superuser status')),
                    ('email', models.EmailField(max_length=254, unique=True)),
                    ('username', models.CharField(max_length=40, unique=True)),
                    ('is_admin', models.BooleanField(default=False)),
                    ('is_student', models.BooleanField(default=True)),
                    ('is_professor', models.BooleanField(default=False)),
                    ('created', models.DateTimeField(auto_now_add=True)),
                    ('updated', models.DateTimeField(auto_now=True)),
                    ('first_name', models.CharField(blank=True, max_length=40)),
                    ('mid_name', models.CharField(blank=True, max_length=40)),
                    ('last_name', models.CharField(blank=True, max_length=40)),
                    ('gender', models.CharField(blank=True, max_length=40)),
                    ('birthday', models.DateField(blank=True, null=True)),
                    ('school_year', models.CharField(blank=True, max_length=40)),
                    ('avatar', models.URLField(blank=True)),
                    ('friends', models.ManyToManyField(related_name='_account_friends_+', to=settings.AUTH_USER_MODEL)),
                    ('groups', models.ManyToManyField(blank=True,
                                                      help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                                                      related_name='user_set', related_query_name='user',
                                                      to='auth.Group', verbose_name='groups')),
                ],
                options={
                    'abstract': False,
                },
        ),
        migrations.CreateModel(
                name='Major',
                fields=[
                    ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('major', models.CharField(max_length=10)),
                    ('major_name', models.CharField(max_length=100)),
                    ('major_school', models.CharField(max_length=100)),
                ],
        ),
        migrations.AddField(
                model_name='account',
                name='major',
                field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Major'),
        ),
        migrations.AddField(
                model_name='account',
                name='user_permissions',
                field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.',
                                             related_name='user_set', related_query_name='user', to='auth.Permission',
                                             verbose_name='user permissions'),
        ),
    ]
