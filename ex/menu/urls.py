from django.urls import path
from .views import menu_view, element_view

urlpatterns = [
    path('<str:name>/', menu_view, name='menu'),
    path('elem/<str:name>/', element_view, name='elem'),
]