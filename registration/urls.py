from django.urls import path

from . import views

urlpatterns = [
    # /registration/
    path('', views.index, name='index'),
    # /registration/23/
    path('<int:watchparty_loc_id>/', views.register, name='register'),
    # /registration/household/wM/asldfjasdfsdlfölfj/
    path('/household/<household_pk_uidb64>/<token>/',
         views.register_with_household_id, name='register_with_household_id'),
    # /registration_success/2/
    path('registration_success/<int:user_id>/',
         views.registration_success, name='registration_success'),
    # /registration/activate/slödfkj/aölskdfj/
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # /registration/new_watchparty/
    path('new_watchparty/', views.new_watchparty, name='new_watchparty'),
    path('watchparty_activate/<uidb64>/<email_token>/',
         views.watchparty_activate, name='watchparty_activate'),
    path('watchparty_registration_success/<int:loc_id>/',
         views.watchparty_registration_success, name='watchparty_registration_success')
]
