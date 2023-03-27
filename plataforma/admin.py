from django.contrib import admin
from .models import Pacientes, DicesPatient, Refeicao, Opcao


@admin.register(Pacientes)
class Patient(admin.ModelAdmin):
    list_display = ('nome', 'sexo', 'idade', 'email', 'telefone', 'nutri')
    readonly_fields = ('nome', 'sexo', 'idade', 'email', 'telefone', 'nutri')

@admin.register(DicesPatient)
class Dices(admin.ModelAdmin):
    list_display = ('patient', 'data', 'altura')
    readonly_fields = ('patient', 'data', 'altura', 'percentual_gordura', 'percentual_musculo', 'colesterol_hdl', 'colesterol_ldl', 'colesterol_total', 'trigliceridios')

@admin.register(Refeicao)
class Reifeicao_patient(admin.ModelAdmin):
    list_display = ('patient', 'titulo', 'horario')
    readonly_fields = ('patient', 'titulo', 'horario', 'carboidratos', 'proteinas', 'gorduras')

@admin.register(Opcao)
class Opcao_patient(admin.ModelAdmin):
    list_display = ('refeicao', )
    readonly_fields = ('refeicao', 'imagem', 'descricao')