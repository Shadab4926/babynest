from django.shortcuts import render
from names.models import BabyName

def home_view(request):
    trending_names = BabyName.objects.order_by('-popularity')[:8]
    return render(request, 'pages/home.html', {'trending_names': trending_names})