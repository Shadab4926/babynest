from django.db import models
from django.contrib.auth.models import User  # ✅ ye line zaroori hai
from django_ckeditor_5.fields import CKEditor5Field






class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    excerpt = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='blog_images/')
    date = models.DateField(auto_now_add=True)
    read_time = models.PositiveIntegerField(default=2)
    category = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    content = CKEditor5Field('Content', config_name='default')  # or 'extends' for more features

    


    def __str__(self):
        return self.title

@property
def read_time(self):
    word_count = len(self.content.split())
    return max(1, word_count // 200)
