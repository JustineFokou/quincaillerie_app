from django.urls import path
from . import views

app_name = 'stocks'

urlpatterns = [
    path('', views.MouvementStockListView.as_view(), name='list'),
    path('create/', views.MouvementStockCreateView.as_view(), name='create'),
    path('<int:pk>/', views.MouvementStockDetailView.as_view(), name='detail'),
    path('entree/', views.EntreeStockView.as_view(), name='entree'),
    path('sortie/', views.SortieStockView.as_view(), name='sortie'),
    path('ajustement/', views.AjustementStockView.as_view(), name='ajustement'),
]
