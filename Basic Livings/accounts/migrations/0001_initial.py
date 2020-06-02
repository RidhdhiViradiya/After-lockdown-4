# Generated by Django 3.0.3 on 2020-05-04 15:09

import accounts.managers
import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('city_id', models.AutoField(primary_key=True, serialize=False)),
                ('city_name', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
                'db_table': 'city',
            },
        ),
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('package_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200, null=True)),
                ('description', models.CharField(max_length=300)),
                ('duration', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Packages',
                'verbose_name_plural': 'Packages',
                'db_table': 'packages',
            },
        ),
        migrations.CreateModel(
            name='PublicQueries',
            fields=[
                ('query_id', models.AutoField(primary_key=True, serialize=False)),
                ('sender', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=300)),
                ('subject', models.CharField(max_length=50)),
                ('date_posted', models.DateTimeField(default=datetime.datetime(2020, 5, 4, 20, 39, 13, 948325))),
                ('message', models.CharField(max_length=1024)),
            ],
            options={
                'verbose_name': 'Public Query',
                'verbose_name_plural': 'Public Queries',
                'db_table': 'public_queries',
            },
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('area_id', models.AutoField(primary_key=True, serialize=False)),
                ('area_name', models.CharField(max_length=40)),
                ('pincode', models.CharField(default='', max_length=6)),
                ('city_id', models.ForeignKey(db_column='city_id', on_delete=django.db.models.deletion.CASCADE, to='accounts.City')),
            ],
            options={
                'verbose_name': 'Area',
                'verbose_name_plural': 'Areas',
                'db_table': 'Area',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=10, verbose_name='gender')),
                ('address', models.CharField(default='', max_length=200, verbose_name='address')),
                ('phone', models.CharField(default='', max_length=10, validators=[django.core.validators.RegexValidator(code='Invalid Phone Number', message='Enter valid Phone Number', regex='^(\\+91[\\-\\s]?)?[0]?(91)?[789]\\d{9}$')], verbose_name='phone')),
                ('is_pgVendor', models.BooleanField(default=False, verbose_name='pgVendor')),
                ('is_foodVendor', models.BooleanField(default=False, verbose_name='foodVendor')),
                ('is_student', models.BooleanField(default=True, verbose_name='student')),
                ('date_joined', models.DateTimeField(default=datetime.datetime(2020, 5, 4, 20, 39, 13, 950319), verbose_name='date joined')),
                ('email_verified_at', models.DateTimeField(blank=True, null=True, verbose_name='email verified at')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_staff', models.BooleanField(default=False)),
                ('area_id', models.ForeignKey(blank=True, db_column='area_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Area')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'user',
            },
            managers=[
                ('object', accounts.managers.UserManager()),
            ],
        ),
    ]
