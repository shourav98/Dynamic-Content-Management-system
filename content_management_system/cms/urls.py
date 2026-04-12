from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('content/<int:pk>/modal/', views.content_modal, name='content_modal'),
    path('explanation/<int:pk>/modal/', views.explanation_modal, name='explanation_modal'),
    path('api/content/<int:pk>/', views.api_content, name='api_content'),
]
