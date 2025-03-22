from django.urls import path
from . import views

app_name = 'cases'

urlpatterns = [
    path('', views.case_list, name='case_list'),
    path('create/', views.case_create, name='case_create'),
    path('<int:pk>/', views.case_detail, name='case_detail'),
    path('<int:pk>/edit/', views.case_edit, name='case_edit'),
    path('<int:case_pk>/add-natural-person/', views.add_natural_person, name='add_natural_person'),
    path('<int:case_pk>/add-legal-entity/', views.add_legal_entity, name='add_legal_entity'),
    path('<int:pk>/review/', views.case_review, name='case_review'),
]



