from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field

import uuid


RELIGION_CHOICES = [
    ('Islam', 'Islam'),
    ('Hinduism', 'Hinduism'),
    ('Christianity', 'Christianity'),
    ('Sikhism', 'Sikhism'),
    ('Buddhism', 'Buddhism'),
    ('Other', 'Other'),
]

class BabyName(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    gender = models.CharField(max_length=10)
    religion = models.CharField(max_length=50)
    origin = models.CharField(max_length=100, blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)  # name length
    syllables = models.IntegerField(blank=True, null=True)
    popularity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='baby_images/', blank=True, null=True)
    meaning = models.TextField(blank=True, null=True)


    def generate_unique_slug(self):
        if not self.name or self.name == "Unnamed":
            base_slug = slugify(f"unnamed-{uuid.uuid4().hex[:8]}")
        else:
            base_slug = slugify(self.name)
        
        unique_slug = base_slug
        suffix = uuid.uuid4().hex[:8]
        counter = 1
        while BabyName.objects.filter(slug=unique_slug).exclude(id=self.id).exists():
            unique_slug = f"{base_slug}-{suffix}"
            if BabyName.objects.filter(slug=unique_slug).exclude(id=self.id).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            suffix = uuid.uuid4().hex[:8]
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('TR', 'Trending'),
        ('ED', 'Education'),
        ('IN', 'Inspiration'),
    ]
    
    title = models.CharField(max_length=200)
    content = CKEditor5Field('Text', config_name='default')
    excerpt = models.CharField(max_length=300)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    tags = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='name_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read_time = models.PositiveIntegerField(default=2)

    

    def __str__(self):
        return self.title

    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',')]
