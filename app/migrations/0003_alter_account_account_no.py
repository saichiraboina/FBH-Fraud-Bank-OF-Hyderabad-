# Generated by Django 5.1.7 on 2025-04-10 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_account_account_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='Account_no',
            field=models.BigAutoField(default=1234567890, primary_key=True, serialize=False),
        ),
    ]
