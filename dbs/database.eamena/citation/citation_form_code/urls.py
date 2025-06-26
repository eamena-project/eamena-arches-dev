from django.urls import path
from . import views

urlpatterns = [
	path('citations/', views.citation_generator, name='citation_generator')
]
