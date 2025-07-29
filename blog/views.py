from django.shortcuts import render, get_object_or_404
from .models import BlogPost

def blog_home(request):
    featured_post = BlogPost.objects.filter(is_featured=True).first()
    blog_posts = BlogPost.objects.exclude(id=featured_post.id) if featured_post else BlogPost.objects.all()
    return render(request, 'blog/blog_home.html', {
        'featured_post': featured_post,
        'blog_posts': blog_posts
    })

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)

    # Estimate read time if missing
    if not hasattr(post, 'read_time'):
        post.read_time = max(len(post.content.split()) // 200, 1)

    related_posts = BlogPost.objects.filter(category=post.category).exclude(id=post.id).order_by('-date')[:3]

    return render(request, 'blog/blog_detail.html', {
        'post': post,
        'related_posts': related_posts,
    })

def about_page(request):
    return render(request, 'blog/about.html')

def contact_page(request):
    return render(request, 'blog/contact.html')

def faq_page(request):
    return render(request, 'blog/faq.html')

def privacy_page(request):
    return render(request, 'blog/privacy.html')
