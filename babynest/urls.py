from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from names import views as names_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ Include only ONCE
    path('products/', include('affiliate_products.urls', namespace='affiliate_products')),
    
    # Other apps
    path('advanced-generator/', names_views.advanced_name_generator, name='advanced_generator'),
    path('', include('pages.urls')),              # Home page
    path('names/', include('names.urls')),        # Baby name URLs
    path('blog/', include('blog.urls')),          # Blog URLs
    path('accounts/', include('allauth.urls')),   # Login/Signup
    path('tools/', include(('tools.urls', 'tools'), namespace='tools')),

    # CKEditor upload
    path('ckeditor5/', include('django_ckeditor_5.urls')),

]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
