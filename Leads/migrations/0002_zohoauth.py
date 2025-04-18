# Generated by Django 5.1.7 on 2025-04-15 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Leads', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZohoAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=255)),
                ('refresh_token', models.CharField(max_length=255)),
                ('expires_in', models.DateTimeField()),
                ('token_type', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
