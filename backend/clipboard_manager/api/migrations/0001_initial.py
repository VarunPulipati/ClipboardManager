# Generated by Django 5.0.3 on 2024-03-26 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shortcut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=100)),
                ('keys', models.CharField(max_length=200)),
                ('action', models.CharField(max_length=10)),
            ],
        ),
    ]
