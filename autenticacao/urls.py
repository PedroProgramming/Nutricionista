from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login, name="login"),
    path('validate_login/', views.validate_login, name="validate_login"),
    path('register_account/', views.register_account, name="register_account"),
    path('validate_register/', views.validate_register, name="validate_register"),
    path('exit_account/', views.exit_account, name="exit_account"),
    path('active_account/<str:token>', views.active_account, name="active_account"),
]