from django_ckeditor_5.fields import CKEditor5Field
from django.conf import settings
from django.db import models
from django.utils.html import mark_safe
import requests
from bs4 import BeautifulSoup


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Retailer(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='retailers/', blank=True)
    affiliate_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Feature(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class (optional)")

    def __str__(self):
        return self.name


class Specification(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}: {self.value}"


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    quantity = models.IntegerField(default=1)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    image = models.ImageField(upload_to='products/')
    key_features = models.TextField(blank=True)
    shipping_info = models.TextField(blank=True)
    description = CKEditor5Field('Description', config_name='default')
    content = CKEditor5Field('Content', config_name='default')
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    last_price_update = models.DateTimeField(auto_now=True)
    pros = models.TextField(blank=True, help_text="One pro per line")
    cons = models.TextField(blank=True, help_text="One con per line")
    shipping_time = models.CharField(max_length=50, blank=True)
    source = models.CharField(max_length=100, blank=True)
    buy_link = models.URLField(blank=True)
    primary_retailer = models.ForeignKey(Retailer, on_delete=models.SET_NULL, null=True, blank=True)

    features = models.ManyToManyField(Feature, blank=True, related_name='products')
    specifications = models.ManyToManyField(Specification, blank=True, related_name='products')

    bundled_with = models.ManyToManyField(
        'self',
        through='ProductBundleItem',
        symmetrical=False,
        related_name='bundled_in',
        blank=True
    )

    similar_products = models.ManyToManyField(
        'self',
        through='RelatedProduct',
        symmetrical=False,
        related_name='related_from',
        blank=True
    )

    def __str__(self):
        return self.title

    @property
    def discount_percentage(self):
        if self.original_price and self.price < self.original_price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0

    @property
    def average_rating(self):
        return self.reviews.aggregate(models.Avg('rating'))['rating__avg'] or self.rating


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image for {self.product.title}"

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return None


class ProductBadge(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='badges')
    label = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, help_text="Use FontAwesome icon class, e.g. fa-check")

    def __str__(self):
        return f"{self.label} - {self.product.title}"




class ProductBundleItem(models.Model):
    main_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='bundle_as_main'
    )
    bundled_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='bundle_as_component'
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('main_product', 'bundled_product')

    def __str__(self):
        return f"{self.bundled_product.title} bundled with {self.main_product.title}"


class RelatedProduct(models.Model):
    source_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='outgoing_relations'
    )
    target_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='incoming_relations'
    )
    relation_type = models.CharField(max_length=100, blank=True, help_text="E.g. 'similar', 'complementary'")

    class Meta:
        unique_together = ('source_product', 'target_product')

    def __str__(self):
        return f"{self.source_product.title} → {self.target_product.title} ({self.relation_type})"


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    author = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rating}/5 by {self.author}"


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    affiliate_url = models.URLField()
    last_updated = models.DateTimeField(auto_now=True)
    in_stock = models.BooleanField(default=True)

    class Meta:
        ordering = ['-last_updated']
        unique_together = ['product', 'retailer']

    def __str__(self):
        return f"{self.product.title} @ {self.retailer.name}: ₹{self.price}"
