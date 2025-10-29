from django.urls import path
from . import views

app_name = 'fournisseurs'

urlpatterns = [
    path('', views.FournisseurListView.as_view(), name='list'),
    path('create/', views.FournisseurCreateView.as_view(), name='create'),
    path('<int:pk>/', views.FournisseurDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.FournisseurUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.FournisseurDeleteView.as_view(), name='delete'),
]
