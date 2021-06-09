from django.urls import path

from . import views

urlpatterns = [
    #/registration/
    path('', views.index, name='index'),
    #/registration/23/
    path('<int:watchparty_loc_id>/', views.register, name='register'),
    #/registration_success/2/
    path('registration_success/<int:user_id>/', views.registration_success, name='registration_success'),
    #/validation_success/
    path('validation_success/', views.validation_success, name='validation_success'),
]