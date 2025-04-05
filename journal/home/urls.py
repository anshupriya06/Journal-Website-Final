from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import include

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
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
    path('logout/', views.logout_view, name='logout'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('terms/', views.terms_view, name='terms'),
    
    # Password Reset URLs
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='password/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),
         name='password_reset_complete'),
    path('social-auth/', include('social_django.urls', namespace='social')),
#     path('terms/', views.terms, name='terms'),
#     path('privacy/', views.privacy, name='privacy'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/update-image/', views.update_profile_image, name='update_profile_image'),
    path('journals/', views.journals, name='journals'),
    path('article/<int:article_id>/', views.view_article, name='view_article'),
]
