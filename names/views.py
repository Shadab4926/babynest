from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from names.models import BabyName, BlogPost
from .models import BabyName

def home_view(request):
    """Home page with trending names"""
    trending_names = BabyName.objects.all().order_by('-popularity')[:4]
    return render(request, 'home.html', {'trending_names': trending_names})

def babyname_detail(request, slug):
    """Detail page for a single baby name"""
    babyname = get_object_or_404(BabyName, slug=slug)
    return render(request, 'names/name_detail.html', {'babyname': babyname})

def girls_name_list(request):
    names = BabyName.objects.filter(gender__iexact='Girl')
    return render(request, 'names/list.html', {'names': names})

def boys_name_list(request):
    names = BabyName.objects.filter(gender__iexact='Boy')
    return render(request, 'names/list.html', {'names': names})



def name_list(request):
    names = BabyName.objects.all()

    # 🔍 Search by name
    query = request.GET.get('q')
    if query:
        names = names.filter(name__icontains=query)

    # 👧 Filter by gender (Boy/Girl)
    gender = request.GET.get('gender')
    if gender:
        names = names.filter(gender__iexact=gender)

    # 🔤 Filter by starting letter
    starts_with = request.GET.get('starts_with')
    if starts_with:
        names = names.filter(name__istartswith=starts_with)

    # 🕊️ Filter by religion
    religion = request.GET.get('religion')
    if religion:
        names = names.filter(religion__iexact=religion)

    context = {
        'names': names,
    }
    return render(request, 'names/list.html', context)

def advanced_name_generator(request):
    names = BabyName.objects.all()

    search = request.GET.get('search')
    gender = request.GET.get('gender')
    starts_with = request.GET.get('starts_with')
    religion = request.GET.get('religion')

    if search:
        names = names.filter(name__icontains=search)

    if gender and gender != "":
        names = names.filter(gender__iexact=gender)

    if starts_with and starts_with != "":
        names = names.filter(name__istartswith=starts_with)

    if religion and religion != "":
        names = names.filter(religion__iexact=religion)

    context = {
        'names': names,
    }
    return render(request, 'names/advanced_generator.html', context)

def blog_home(request):
    """Blog homepage with published posts"""
    posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'blog/home.html', {'posts': posts})

def ajax_filter_names(request):
    """AJAX endpoint for dynamic filtering"""
    gender = request.GET.get('gender')
    starts_with = request.GET.get('starts_with')
    religion = request.GET.get('religion')

    filters = Q()
    if gender: filters &= Q(gender__iexact=gender)
    if starts_with: filters &= Q(name__istartswith=starts_with)
    if religion: filters &= Q(religion__iexact=religion)

    names = BabyName.objects.filter(filters).values(
        'name', 'gender', 'religion', 'origin', 'slug', 'meaning'
    )
    return JsonResponse(list(names), safe=False)
