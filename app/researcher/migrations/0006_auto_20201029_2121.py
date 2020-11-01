# Generated by Django 3.1.2 on 2020-10-29 13:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('researcher', '0005_auto_20201005_0258'),
    ]

    operations = [
        migrations.CreateModel(
            name='K_User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(120)])),
                ('gender', models.CharField(max_length=1)),
                ('location', models.CharField(max_length=32)),
                ('test_result', models.CharField(choices=[('True', 'Positive'), ('False', 'Negative'), ('None', 'Unknown')], max_length=5)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(default=9, max_length=1),
            preserve_default=False,
        ),
    ]