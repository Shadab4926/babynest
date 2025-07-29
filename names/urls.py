from django.urls import path
from . import views

urlpatterns = [
    path('', views.name_list, name='name_list'),  # /names/
    path('names/advanced-generator/', views.advanced_name_generator, name='advanced_name_generator'),
    path('name-generator/', views.advanced_name_generator),  # Optional alias
    path('girls/', views.girls_name_list, name='girls_name_list'),  # ✅ new URL
    path('boys/', views.boys_name_list, name='boys_name_list'),
    path('ajax/filter/', views.ajax_filter_names, name='ajax_filter_names'),
    path('<slug:slug>/', views.babyname_detail, name='name_detail'),  # /names/<slug>/
    ]
