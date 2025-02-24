from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('editor/', views.editor, name='editor'),
    path('reviewer/', views.reviewer, name='reviewer'),
    path('guidelines/author/', views.author_guidelines, name='author_guidelines'),
    path('guidelines/editor/', views.editor_guidelines, name='editor_guidelines'),
    path('guidelines/reviewer/', views.reviewer_guidelines, name='reviewer_guidelines'),
    path('join/member/', views.join_member, name='join_member'),
    path('join/editor/', views.join_editor, name='join_editor'),
    path('join/reviewer/', views.join_reviewer, name='join_reviewer'),
    # path('guidelines/', views.guidelines, name='guidelines'),
    path('submit-paper/', views.submit_paper, name='submit_paper'),
    path('archives/', views.archives, name='archives'),
]
