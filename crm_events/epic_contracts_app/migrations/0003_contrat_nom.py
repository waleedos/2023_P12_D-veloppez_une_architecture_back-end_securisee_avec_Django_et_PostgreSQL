# Generated by Django 4.2.7 on 2023-11-27 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epic_contracts_app', '0002_contrat_delete_contract'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrat',
            name='nom',
            field=models.CharField(default='Contrat sans nom', max_length=25, verbose_name='Nom du contrat'),
        ),
    ]
