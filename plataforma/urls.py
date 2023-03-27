from django.urls import path
from . import views


urlpatterns = [
    path('patient/', views.patient, name="patient"),
    path('validate_patient/', views.validate_patient, name="validate_patient"),
    path('dices_patient_list/', views.dices_patient_list, name="dices_patient_list"),
    path('dices_patient/<int:id>', views.dices_patient, name="dices_patient"),
    path('validate_dices_patient/<int:id>', views.validate_dices_patient, name="validate_dices_patient"),
    path('weight_chart/<int:id>', views.weight_chart, name="weight_chart"),
    path('food_plan_list/', views.food_plan_list, name="food_plan_list"),
    path('food_plan/<int:id>', views.food_plan, name="food_plan"),
    path('snack/<int:id>', views.snack, name="snack"),
    path('option/<int:id>', views.option, name="option"),
]