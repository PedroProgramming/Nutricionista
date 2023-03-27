from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as log_in, logout
from django.conf import settings
from hashlib import sha256
from .utils import password_is_valid, validate_fields
from .emails import send_email
from .models import Ativacao
import os



#  Register
 
def register_account(request):

    if request.user.is_authenticated:
        return redirect('/patient/')

    return render(request, 'register.html')


def validate_register(request):
    
    name = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')


    if not validate_fields(name, email, password, confirm_password):
        messages.add_message(request, constants.ERROR, 'Fields invalid.') 
        return redirect('/auth/register_account/')
    
    if not password_is_valid(request, password, confirm_password):
        return redirect('/auth/register_account/')
    

    try:
        user = User.objects.create_user(
            username=name,
            email=email,
            password=password,
            is_active=False
        )
        user.save()

        token = sha256(f"{name}{email}".encode()).hexdigest()
        active_account = Ativacao(token=token, user=user)
        active_account.save()

        path_template = os.path.join(settings.BASE_DIR, 'autenticacao/templates/emails/confirm_account.html')
        send_email(path_template, 'Registared Confirm', [email,], username=name, link_ativacao=f"http://127.0.0.1:8000/auth/active_account/{token}")

        messages.add_message(request, constants.SUCCESS, 'User registared successfully. Check your e-mail to active your account')
        return redirect('/auth/login/')
    except:
        messages.add_message(request, constants.ERROR, 'Internal error system.')
        return redirect('/auth/register_account/')




# Log in

def login(request):
    if request.user.is_authenticated:
        return redirect('/patient/')
    return render(request, 'login.html')


def validate_login(request):
    
    email = request.POST.get('email')
    password = request.POST.get('password')


    if not validate_fields(email, password):
        messages.add_message(request, constants.ERROR, 'Fields invalid.') 
        return redirect('/auth/login/')

    user = authenticate(username=email, password=password)

    if User.objects.filter(username=email).filter(is_active=False):
        messages.add_message(request, constants.ERROR, f'Your account not active! Plase check your e-mail to active.') 
        return redirect('/auth/login/')

    if not user:
        messages.add_message(request, constants.ERROR, 'E-mail or password invalid.') 
        return redirect('/auth/login/')
    
    else:
        log_in(request, user)
        messages.add_message(request, constants.SUCCESS, 'Welcome! Logged successfully') 
        return redirect('/patient/')


#  Exit account

def exit_account(request):
    logout(request)
    messages.add_message(request, constants.SUCCESS, 'Check back often') 
    return redirect('/auth/login/')

# Active Account

def active_account(request, token):
    
    token = get_object_or_404(Ativacao, token=token)

    if token.ativo:

        messages.add_message(request, constants.WARNING, 'Esse token já foi usado!')
        return redirect('/patient/')

    user = User.objects.get(username=token.user.username)
    user.is_active = True
    user.save()
    token.ativo = True
    token.save()
    messages.add_message(request, constants.SUCCESS, 'Conta ativa com sucesso.')
    return redirect('/auth/login/')
