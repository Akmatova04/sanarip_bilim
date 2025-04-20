# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Башка барактардын жолдору
    path('', views.index_view, name='index'),
    path('about/', views.about_view, name='about'),
    path('courses/', views.courses_view, name='courses'),
    path('course/<int:pk>/', views.course_detail_view, name='course_detail'),
    path('resources/', views.resources_view, name='resources'),
    path('faq/', views.faq_view, name='faq'),
    path('contact/', views.contact_view, name='contact'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # --- БЛОГ ҮЧҮН URL МАРШРУТТАРЫ ---
    path('blog/', views.blog_view, name='blog'), # Блог тизмеси
    path('blog/post/<int:pk>/', views.post_detail_view, name='post_detail'), # Деталдуу барак
    # ------------------------------------
]