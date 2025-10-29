from django.urls import path
from . import views

app_name = 'utilisateurs'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('', views.UserListView.as_view(), name='list'),
    path('create/', views.UserCreateView.as_view(), name='create'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.UserUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='delete'),
]
