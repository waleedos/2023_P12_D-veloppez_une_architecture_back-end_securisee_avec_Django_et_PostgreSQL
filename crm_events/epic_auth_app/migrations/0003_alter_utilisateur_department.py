# Generated by Django 4.2.7 on 2023-11-22 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epic_auth_app', '0002_utilisateur_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='department',
            field=models.CharField(choices=[('ADM', 'Administration'), ('COM', 'Commercial'), ('SUP', 'Support'), ('GES', 'Gestion')], default='COM', max_length=3, verbose_name='département'),
        ),
    ]
