# Generated by Django 4.1.7 on 2023-03-19 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0002_alter_pacientes_nutri_dicespatient'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dicespatient',
            old_name='paso',
            new_name='peso',
        ),
    ]
