from django.urls import path
from . import views
from .views import RegisterView

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),

]
