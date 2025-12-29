from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('register/', TemplateView.as_view(template_name='register.html'), name='register_page'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login_page'),
    path('/', TemplateView.as_view(template_name='home.html'), name='home_page'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard_page'),
]