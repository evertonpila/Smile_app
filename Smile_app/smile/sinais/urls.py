
from django.urls import  path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'), 
    path('home', views.home, name='home'),
    path('chave', views.chave, name='chave'),
    path('editar_conta', views.editar_conta, name='editar_conta'),
    
]
