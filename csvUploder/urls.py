from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv'),
    path('generate-testcases/', views.generate_testcases, name='generate_testcases'),
    path('generate-edgecases/', views.generate_edgecases, name='generate_edgecases'),
    path('upload-syllabus/', views.upload_syllabus, name='upload_syllabus'),
]