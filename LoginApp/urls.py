from django.urls import path
from . import views

app_name = 'LoginApp'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('sign-in/', views.sign_in, name='signIn'),
    path('sign-out/',views.sign_out, name='sign_out'),
    path('profile/',views.user_profile, name='profile'),
    path('edit-profile/',views.edit_profile, name='edit_profile'),
]
