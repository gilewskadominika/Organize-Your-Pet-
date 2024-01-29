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
from organize_your_pet import views

urlpatterns = [
    path('main/', views.DashboardView.as_view(), name='dashboard'),
    path('addPet/', views.AddPetView.as_view(), name='add_pet'),
    path('listPet/', views.PetsListView.as_view(), name='pets_list'),
    path('modifyPet/', views.ModifyPetView.as_view(), name='modify_pet'),
    path('book-appointment/', views.BookAppointmentView.as_view(), name='book_appointment'),
    path('visits/list/', views.VisitsListView.as_view(), name='visits_list'),
    path('visit/<int:pk>/', views.VisitInfoView.as_view(), name='visit_info'),
    path('visit/modify/<int:pk>/', views.VisitModifyView.as_view(), name='visit_modify')
]