from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main import models
from datetime import date
from main.funcs import staff_required
from itertools import chain


def index(request):
    category = models.Category.objects.all()
    products = models.Product.objects.all()
    reviews = models.Review.objects.all()
    videos = models.ProductVideo.objects.all()
    # product_news = models.Product.objects.last()[-4]
    mark = 0
    for i in reviews:
        mark += i.mark
    
    mark = int(mark/len(reviews)) if reviews else 0

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = models.Product.objects.get(id=product_id)
        cart = models.Cart.objects.filter(tatus=1)
        is_product = models.CartProduct.objects.filter(product=product,cart__status=1).first()
        if is_product:
            is_product.count += 1
            is_product.save()
            return redirect('front:active_cart')
        if not cart:
            cart = models.Cart.objects.create(
                user=request.user,
                status=1
            )
        
        models.CartProduct.objects.create(
            product=product,
            cart=cart.first(),
            count=1
        )
        return redirect('front:active_cart')

    context = {
        'category':category,
        'products':products,
        'videos':videos,
        'rating':range(1,6),
        'mark':mark,
        
        }
    return render(request, 'front/index.html',context)

def delete_cart(request, id):
    cart = models.Cart.objects.filter(status=1)[0]
    cart_product = models.CartProduct.objects.filter(id=id)[0]
    cart_product.delete()
    return redirect('front:cart_detail', cart.code)


def category_list(request, id):
        category = models.Category.objects.all()
        categor = models.Category.objects.get(id=id)
        products = models.Product.objects.filter(category=categor)
        wishlist = models.WishList.objects.filter(user=request.user)
        context = {
            'category':category,
            'categor':categor,
            'products':products,
            'wishlist': wishlist,
            }
        return render(request, 'front/category/category_list.html', context)

def product_list(request):
    category = models.Category.objects.all()
    products = models.Product.objects.all()
    wishlist = models.WishList.objects.filter(user=request.user)
    context = {
        'category':category,
        'products':products,
        'wishlist': wishlist,
        }
    return render(request, 'front/product/product_list.html', context)

def product_detail(request, id):
    category = models.Category.objects.all()
    product = models.Product.objects.get(id=id)
    reviews = models.Review.objects.filter(product=product)
    images = models.ProductImg.objects.filter(product=product)
    mark = 0
    wishlist = models.WishList.objects.filter(product=product, user=request.user)
    if wishlist:
        wishlist = wishlist[0]

    for i in reviews:
        mark += i.mark

    mark = int(mark/len(reviews)) if reviews else 0
    context = {
        'product':product,
        'mark':mark,
        'rating':range(1,6),
        'images':images,
        'reviews':reviews,
        'wishlist': wishlist,
        'category':category 
        
    }
    return render(request, 'front/product/product_detail.html', context)

@login_required(login_url='auth:login')
def carts(request):
    category = models.Category.objects.all()
    queryset = models.Cart.objects.filter(user=request.user, status__in=[2,3,4]) #False
    context = {'queryset':queryset, 'category':category}
    return render(request, 'front/carts/list.html', context)


@login_required(login_url='auth:login')
def active_cart(request):
    queryset , _ = models.Cart.objects.get_or_create(user=request.user, status=1) #True
    return redirect('front:cart_detail', queryset.code)


@login_required(login_url='auth:login')
def cart_detail(request, code):
    category = models.Category.objects.all()
    cart = models.Cart.objects.get(code=code)
    queryset = models.CartProduct.objects.filter(cart=cart)
    if request.method == 'POST':
        cart.status = 2
        cart.order_date = date.today()
        cart.save()
        data = list(request.POST.items())[1::]
        for id,value in data:
            product = models.CartProduct.objects.get(id=id)
            product.count = value
            product.save()
    context = {
        'cart': cart,
        'queryset':queryset,
        'category': category

        }
    return render(request, 'front/carts/detail.html', context)


@login_required(login_url='auth:login')
def cart_deactivate(request):
    cart = models.Cart.objects.get(user=request.user, status=1)
    cart.status = 2
    cart.save()
    return redirect('front:index')

def add_cart(request, code):
    if models.Product.objects.filter(code=code):
        product = models.Product.objects.get(code=code)
        cart, _ = models.Cart.objects.get_or_create(status=1, user=request.user)
        is_product = models.CartProduct.objects.filter(product=product,cart__status=1,cart__user=request.user).first()
        if is_product:
            is_product.count += 1
            is_product.save()
        if not cart:
            cart = models.Cart.objects.create(
                user=request.user,
                status=1
            )
        
        models.CartProduct.objects.create(
            product=product,
            cart=cart,
            count=1
        )
        
    return redirect('front:index')



def update_quantity(request, id):
    product = models.CartProduct.objects.get(id=id)
    code = product.cart.code
    product.count = int(request.POST['count'])
    product.save()
    return redirect('front:cart_detail', code)



@login_required(login_url='auth:login')
def list_wishlist(request):
    queryset = models.WishList.objects.filter(user=request.user)
    category = models.Category.objects.all()
    context = {'queryset':queryset, 'category':category}
    return render(request, 'front/wishlist/list.html', context)


@login_required(login_url='auth:login')
def remove_wishlist(request, code):
    wishlist = models.WishList.objects.get(product__code = code, user=request.user)
    wishlist.delete()
    return redirect('front:list_wishlist')


@login_required(login_url='auth:login')
def add_wishlist(request, code):
    product = models.Product.objects.get(code=code)
    models.WishList.objects.create(product = product, user=request.user)
    return redirect(request.META.get('HTTP_REFERER', 'front:list_wishlist'))

@login_required(login_url='auth:login')
def add_review(request, code):
    product = models.Product.objects.get(code=code)
    review = models.Review.objects.create(product=product, user=request.user, mark=request.POST.get('mark'))
    review.save()
    return redirect('front:cart_detail', code)