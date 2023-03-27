# Generated by Django 4.1.7 on 2023-03-21 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0003_rename_paso_dicespatient_peso'),
    ]

    operations = [
        migrations.CreateModel(
            name='Refeicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('horario', models.TimeField()),
                ('carboidratos', models.IntegerField()),
                ('proteinas', models.IntegerField()),
                ('gorduras', models.IntegerField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.pacientes')),
            ],
        ),
        migrations.CreateModel(
            name='Opcao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(upload_to='opcao')),
                ('descricao', models.TextField()),
                ('refeicao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.refeicao')),
            ],
        ),
    ]
