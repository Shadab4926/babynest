from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_home, name='blog_home'),                         # Blog homepage
    path('blog/', views.blog_home, name='blog_home'),                    # Optional, same as above
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),    # Blog detail by slug
    # Blog detail by slug

    # Static pages
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('faq/', views.faq_page, name='faq'),
    path('privacy/', views.privacy_page, name='privacy'),
  
   #missing pages
   path('about/', views.about_page, name='about'),
   path('contact/', views.contact_page, name='contact'),
   path('faq/', views.faq_page, name='faq'),
   path('privacy/', views.privacy_page, name='privacy'),
 
]

