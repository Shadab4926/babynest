from django.shortcuts import render, get_object_or_404
from .models import Product ,Category
from django.contrib import messages
from .models import Product, ProductReview
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def product_detail(request, pk):
    try:
        product = get_object_or_404(
            Product.objects.select_related('primary_retailer')
                          .prefetch_related(
                              'features',
                              'specifications',
                              'additional_images',
                              'badges',
                              'reviews'
                          ),
            pk=pk
        )
        
        # Get all related data
        main_image = product.image.url if product.image else None
        additional_images = product.additional_images.all()
        badges = product.badges.all()
        reviews = product.reviews.filter(approved=True)
        bundled_products = product.bundled_with.all()

        
        context = {
            'product': product,
            'main_image': main_image,
            'additional_images': additional_images,
            'features': product.features.all(),
            'specifications': product.specifications.all(),
            'badges': badges,
            'reviews': reviews,
            'bundled_products': bundled_products,
            'site_name': 'BabyNest'
            
        }
        return render(request, 'affiliate_products/product_detail.html', context)
        
    except Exception as e:
        print(f"Error in product_detail view: {str(e)}")
        return render(request, 'affiliate_products/error.html', status=500)



def product_list(request):
    category_slug = request.GET.get('category')
    products = Product.objects.all()

    current_category = None
    if category_slug:
        products = products.filter(category__slug=category_slug)
        current_category = Category.objects.filter(slug=category_slug).first()

    categories = Category.objects.all()

    return render(request, 'affiliate_products/product_list.html', {
        'products': products,
        'categories': categories,
        'current_category': current_category
    })



def submit_review(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        ProductReview.objects.create(
            product=product,
            author=request.POST.get('author'),
            rating=int(request.POST.get('rating')),
            content=request.POST.get('content', '')
        )
        messages.success(request, 'Your review has been submitted!')
        return redirect('affiliate_products:product_detail', pk=product_id)
    return redirect('affiliate_products:product_detail', pk=product_id)

