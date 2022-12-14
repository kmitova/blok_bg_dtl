# Generated by Django 4.1.3 on 2022-12-01 10:41

import django.core.validators
from django.db import migrations, models
import payment.models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=16, validators=[django.core.validators.MinLengthValidator(16)])),
                ('card_cvv', models.CharField(max_length=3, validators=[django.core.validators.MinLengthValidator(3)])),
                ('card_expiry_date', models.DateField(validators=[payment.models.check_card_date_expiry])),
            ],
        ),
    ]
