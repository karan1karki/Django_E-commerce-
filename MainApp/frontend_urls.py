from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('register/', TemplateView.as_view(template_name='register.html'), name='register_page'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login_page'),
]