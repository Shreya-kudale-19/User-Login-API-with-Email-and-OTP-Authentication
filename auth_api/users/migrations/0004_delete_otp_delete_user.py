# Generated by Django 5.2.4 on 2025-07-23 21:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_customuser_last_otp_sent_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OTP',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
