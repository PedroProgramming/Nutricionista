from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.messages import constants
from .utils import validate_fields_patient
from .models import Pacientes, DicesPatient, Refeicao, Opcao
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url="/auth/login/")
def patient(request):
    dices_patient = Pacientes.objects.filter(nutri=request.user)

    context = {
        'dices_patient': dices_patient,
    }

    return render(request, 'patient.html', context=context)


@login_required(login_url="/auth/login/")
def validate_patient(request):

    name = request.POST.get('name')
    sexo = request.POST.get('sexo')
    age = request.POST.get('age')
    email = request.POST.get('email')
    phone = request.POST.get('phone')

    if not validate_fields_patient(name, sexo, age, email, phone):
        messages.add_message(request, constants.ERROR, 'Fields invalid.')
        return redirect('/patient/')
    
    if not age.isnumeric():
        messages.add_message(request, constants.ERROR, 'Enter a valid age.')
        return redirect('/patient/')

    if Pacientes.objects.filter(email=email).exists():
        messages.add_message(request, constants.ERROR, 'Patient already exist.')
        return redirect('/patient/')

    try:
        patient = Pacientes(
            nome=name,
            sexo=sexo,
            idade=age,
            email=email,
            telefone=phone,
            nutri=request.user,
        )
        patient.save()

        messages.add_message(request, constants.SUCCESS, 'Patient registared succssefully.')
        return redirect('/patient/')
    except:
        messages.add_message(request, constants.ERROR, 'Internal error system')
        return redirect('/patient/')
    

@login_required(login_url='/auth/login/')
def dices_patient_list(request):

    patients = Pacientes.objects.filter(nutri=request.user)

    context = {
        'patients': patients,
    }

    return render(request, 'dices_patient_list.html', context=context)


@login_required(login_url='/auth/login/')
def dices_patient(request, id):

    patients = get_object_or_404(Pacientes, id=id)

    if  patients.nutri == request.user:
        dices_patient = DicesPatient.objects.filter(patient=patients)

        context = {
            'patients': patients,
            'dices_patient': dices_patient,
        }

        return render(request, 'dices_patient.html', context=context)
    else:
        messages.add_message(request, constants.ERROR, 'Internal error system.')
        return redirect('/dices_patient_list/')
    

@login_required(login_url='/auth/login/')
def validate_dices_patient(request, id):

    patient = get_object_or_404(Pacientes, id=id)

    peso = request.POST.get('peso')
    altura = request.POST.get('altura')
    gordura = request.POST.get('gordura')
    musculo = request.POST.get('musculo')

    hdl = request.POST.get('hdl')
    ldl = request.POST.get('ldl')
    colesterol_total = request.POST.get('ctotal')
    trigliceridios = request.POST.get('triglicerídios')

    if not validate_fields_patient(peso, altura, gordura, musculo, hdl, ldl, colesterol_total, trigliceridios):
        messages.add_message(request, constants.ERROR, 'Fields invalid.')
        return redirect(f'/dices_patient/{patient.id}')
    
    try:
        patient = DicesPatient(patient=patient,
                            data=datetime.now(),
                            peso=peso,
                            altura=altura,
                            percentual_gordura=gordura,
                            percentual_musculo=musculo,
                            colesterol_hdl=hdl,
                            colesterol_ldl=ldl,
                            colesterol_total=colesterol_total,
                            trigliceridios=trigliceridios,
                            )

        patient.save()

        messages.add_message(request, constants.SUCCESS, 'Dices add succssfully.')
        return redirect(f'/dices_patient_list/')
    except:
        messages.add_message(request, constants.ERROR, 'Internal error system.')
        return redirect(f'/dices_patient/{patient.id}')
    


login_required(login_url='/auth/login/')
@csrf_exempt
def weight_chart(request, id):
    patient = Pacientes.objects.get(id=id)
    dices = DicesPatient.objects.filter(patient=patient).order_by("data")

    pesos = [dice.peso for dice in dices]
    labels = list(range(len(pesos)))
    data = {'peso': pesos,
            'labels': labels}
    return JsonResponse(data)



def food_plan_list(request):
    
    patients = Pacientes.objects.filter(nutri=request.user)

    context = {
        'patients': patients,
    }

    return render(request, 'food_plan_list.html', context=context)

def food_plan(request, id):

    patient_food = get_object_or_404(Pacientes, id=id)

    if  patient_food.nutri == request.user:

        snack_patient = Refeicao.objects.filter(patient=patient_food).order_by('horario')
        option_snack_patient = Opcao.objects.all()

        context = {
            'patient_food': patient_food,
            'snack_patient': snack_patient,
            'option_snack_patient': option_snack_patient,
        }

        return render(request, 'food_plan.html', context=context)
    else:
        messages.add_message(request, constants.ERROR, 'Internal error system24.')
        return redirect('/food_plan_list/')

    

def snack(request, id):

    patient = get_object_or_404(Pacientes, id=id)

    if patient.nutri == request.user:

        titulo = request.POST.get('titulo')
        horario = request.POST.get('horario')
        carboidratos = request.POST.get('carboidratos')
        proteinas = request.POST.get('proteinas')
        gorduras = request.POST.get('gorduras')

        if not validate_fields_patient(titulo, horario, carboidratos, proteinas, gorduras):
            messages.add_message(request, constants.ERROR, 'Fields invalid.')
            return redirect(f'/food_plan/{patient.id}')

        try:
            snack = Refeicao(patient=patient,
                            titulo=titulo,
                            horario=horario,
                            carboidratos=carboidratos,
                            proteinas=proteinas,
                            gorduras=gorduras,
                            )
            snack.save()

            messages.add_message(request, constants.SUCCESS, 'Snack registared successfully.')
            return redirect(f'/food_plan/{patient.id}')
        except:
            messages.add_message(request, constants.ERROR, 'Internal error system.')
            return redirect(f'/food_plan/{patient.id}')
    else:
        messages.add_message(request, constants.ERROR, 'Internal error system.')
        return redirect('/food_plan_list/')
    


def option(request, id):
    patient = get_object_or_404(Pacientes, id=id)


    if request.method == 'POST':
        id_snack = request.POST.get('refeicao')
        imagem = request.FILES.get('imagem')
        descricao = request.POST.get('descricao')

        if not validate_fields_patient(descricao):
            messages.add_message(request, constants.ERROR, 'Fields invalid.')
            return redirect(f'/food_plan/{patient.id}')


        option_snack = Opcao(refeicao_id=id_snack,
                            imagem=imagem,
                            descricao=descricao
                            )
        option_snack.save()

        messages.add_message(request, constants.SUCCESS, 'Snack registared successfully!')
        return redirect(f'/food_plan/{patient.id}')
