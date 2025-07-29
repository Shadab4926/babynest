from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'affiliate_products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('<int:pk>/review/', views.submit_review, name='submit_review'),
       
    
    # Removed duplicate product_detail path
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)