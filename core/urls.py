from django.urls import path
from . import views
from .views_i18n import SetLanguageView

app_name = 'core'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('set-language/', SetLanguageView.as_view(), name='set_language'),
]
