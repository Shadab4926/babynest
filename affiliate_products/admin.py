from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category, ProductImage, ProductBadge, ProductBundleItem, RelatedProduct

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductBadgeInline(admin.TabularInline):
    model = ProductBadge
    extra = 1

class ProductBundleItemInline(admin.TabularInline):
    model = ProductBundleItem
    fk_name = 'main_product'
    extra = 1

class RelatedProductInline(admin.TabularInline):
    model = RelatedProduct
    fk_name = 'source_product'
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'image_preview', 'source']
    search_fields = ['title']
    readonly_fields = ['image_preview']
    inlines = [ProductImageInline, ProductBadgeInline, ProductBundleItemInline, RelatedProductInline]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" style="object-fit:contain;" />', obj.image.url)
        return "No Image"

    image_preview.short_description = 'Image'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
