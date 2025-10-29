from django.urls import path
from . import views

app_name = 'produits'

urlpatterns = [
    path('', views.ProduitListView.as_view(), name='list'),
    path('create/', views.ProduitCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ProduitDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ProduitUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ProduitDeleteView.as_view(), name='delete'),
    path('categories/', views.CategorieListView.as_view(), name='categorie_list'),
    path('categories/create/', views.CategorieCreateView.as_view(), name='categorie_create'),
]
