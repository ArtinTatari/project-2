from django.shortcuts import render
from .models import *
from django.urls import reverse
def home(request):
    category = Category.objects.all()
    return render(request , 'home/home.html' , { 'category' : category})




def all_products(request , slug=None , id=None) :
    products = Product.objects.all()
    category = Category.objects.filter(sub_cat=False)
    if slug and id :
        data = Category.objects.get(slug=slug , id=id)
    return render(request , 'home/products.html'
                  , {'products' : products})


def product_details(request , id) :
    products = Product.objects.get(id=id)
    similar = products.tag.similar_objects()[:5]
    is_like = False
    if products.like.filter(id=request.user.id) .exists():
        is_like = True
    if products.status != 'None' :
        if request.method == 'POST' :
            variant = Variants.objects.filter(product_variant_id=id)
            var_id = request.POST.get('select')
            variants = Variants.objects.get(id = var_id)
        else :
            variant = Variants.objects.filter(product_variant_id=id)
            variants = Variants.objects.get(id=variant[0].id)
        return render(request , 'home/details.html'
                  , {'products' : products , 'variant': variant , 'variants' : variants , 'similar' : similar , 'is_like' : is_like  })
    else :
        return render(request, 'home/details.html'
                  , {'products': products , 'similar' : similar , 'is_like' : is_like})
@login_required(login_url='accounts : login')
def product_like (request , id) :
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=id)
    if product.like.filter(id=request.user1.id).exists () :
        product.like.remove(request.user)
    else :
        product.like.add(request.user)
    return  redirect(url)
