# Generated by Django 5.1.5 on 2025-01-21 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folder_aplikacji', '0006_alter_osoba_data_dodania'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='osoba',
            name='data_dodania',
        ),
    ]
