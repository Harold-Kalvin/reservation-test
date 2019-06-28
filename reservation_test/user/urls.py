from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views
from .forms import LoginForm

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
            template_name='user/login_form.html',
            redirect_authenticated_user=True,
            authentication_form=LoginForm,
        ),
        name="login"
    ),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('profile/', login_required(views.update_profile), name='profile'),
]
