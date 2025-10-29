from django.urls import path
from . import views

app_name = 'ventes'

urlpatterns = [
    path('', views.VenteListView.as_view(), name='list'),
    path('create/', views.VenteCreateView.as_view(), name='create'),
    path('<int:pk>/', views.VenteDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.VenteUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.VenteDeleteView.as_view(), name='delete'),
    path('<int:pk>/finaliser/', views.VenteFinaliserView.as_view(), name='finaliser'),
]
