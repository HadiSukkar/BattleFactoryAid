# Generated by Django 4.2.6 on 2024-01-07 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factory_aid', '0003_teams_alter_pokemon_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='teams',
            name='tier',
            field=models.CharField(default='0', max_length=100),
        ),
    ]
