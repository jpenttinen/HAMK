from django.urls import path

from . import views

app_name = 'aggregator'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('sources/', views.source_list, name='source_list'),
    path('sources/<int:pk>/edit/', views.source_edit, name='source_edit'),
    path('sources/<int:pk>/delete/', views.source_delete, name='source_delete'),
]
