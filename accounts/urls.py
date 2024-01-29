"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from accounts import views as account_view

urlpatterns = [
    path('login/', account_view.LoginView.as_view(), name='login_view'),
    path('logout/', account_view.LogoutView.as_view(), name='logout_view'),
    path('register/', account_view.RegistrationView.as_view(), name='registration_view'),
    path('profile/', account_view.ProfileView.as_view(), name='profile_view'),
    path('profile/edit/', account_view.ProfileEditView.as_view(), name='profile_edit_view')
]
