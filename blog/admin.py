from django.contrib import admin
from .models import BlogPost
from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms
from django.db import models

# Custom form with CKEditor5
class BlogPostAdminForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = '__all__'
        widgets = {
            'content': CKEditor5Widget(
                config_name='extends',  # or 'default' based on your config
                attrs={'class': 'django_ckeditor_5'}
            ),
        }

# Admin class
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = ('title', 'author', 'date', 'category', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'author', 'category']
    list_filter = ['category', 'is_featured']


