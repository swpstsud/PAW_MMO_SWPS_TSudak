# Generated by Django 5.1.5 on 2025-01-21 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('folder_aplikacji', '0004_alter_osoba_plec_alter_stanowisko_opis'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='osoba',
            options={'ordering': ['nazwisko']},
        ),
        migrations.AddField(
            model_name='person',
            name='pseudonim',
            field=models.CharField(default='', max_length=80),
        ),
        migrations.AlterField(
            model_name='stanowisko',
            name='opis',
            field=models.TextField(),
        ),
    ]
