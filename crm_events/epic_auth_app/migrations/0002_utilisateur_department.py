# Generated by Django 4.2.7 on 2023-11-19 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epic_auth_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='department',
            field=models.CharField(choices=[('COM', 'Commercial'), ('SUP', 'Support'), ('GES', 'Gestion')], default='COM', max_length=3, verbose_name='département'),
        ),
    ]
