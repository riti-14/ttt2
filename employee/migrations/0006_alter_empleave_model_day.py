# Generated by Django 4.0.4 on 2022-07-27 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0005_alter_myuser_model_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleave_model',
            name='day',
            field=models.CharField(choices=[('HALF DAY', 'Half day'), ('FULL DAY', 'Full day')], max_length=30),
        ),
    ]
