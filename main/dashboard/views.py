from django.shortcuts import render, redirect
from main import models
from main.funcs import staff_required
from itertools import chain


@staff_required
def index(request):
    category = models.Category.objects.all()
    product = models.Product.objects.all()
    cart = models.Cart.objects.all()
    context = {
        'category':category,
        'product':product,
        'cart':cart,
        }
   
    return render(request, 'dashboard/index.html', context)



@staff_required
# ---------CATEGORY-------------
def detail(request):
    category = models.Category.objects.all()
    context = {
        'category':category
    
    }
    return render(request, 'dashboard/category/detail.html', context)


@staff_required
def category_list(request):
        queryset = models.Category.objects.all()
        context = {
            'queryset':queryset
            }
        return render(request, 'dashboard/category/list.html', context)



@staff_required
def category_create(request):
    if request.method == 'POST':
        models.Category.objects.create(
            name = request.POST['name']
        )
        return redirect('dashboard:category_list')
    return render(request, 'dashboard/category/create.html')



@staff_required
def category_update(request, code):
    queryset = models.Category.objects.get(code=code)
    queryset.name = request.POST['name']
    queryset.save()
    return redirect('dashboard:category_list')


def category_delete(request, code):
    queryset = models.Category.objects.get(code=code)
    queryset.delete()
    return redirect('dashboard:category_list')

# ---------PRODUCT----------------

def product_list(request):
    categories = models.Category.objects.all()
    category_code = request.GET.get('category_code')
    if category_code and category_code != '0':
        queryset = models.Product.objects.filter(category__code=category_code)
    else:
        queryset = models.Product.objects.all()
    context = {
          'queryset':queryset,
          'categories':categories,
          'category_code':category_code,
    }
    return render(request, 'dashboard/product/list.html', context)



def product_detail(request, code):
    queryset = models.Product.objects.get(code=code)
    images = models.ProductImg.objects.filter(product=queryset)
    reviews = models.Review.objects.filter(product=queryset)
    ratings = range(5,0,-1)
    videos = models.ProductVideo.objects.filter(product=queryset)
    context = {
          'queryset':queryset,
          'images':images,
          'reviews':reviews,
          'ratings':ratings,
          'videos':videos
    }
    return render(request, 'dashboard/product/detail.html', context)
    

def product_create(request):
    categorys = models.Category.objects.all()
    context = {'categorys':categorys}
    if request.method == 'POST':
        delivery = True if request.POST.get('delivery') else False
        
        product = models.Product.objects.create(
            category_id = request.POST['category_id'],
            name = request.POST['name'],
            body = request.POST['body'],
            price = request.POST['price'],
            banner_img = request.FILES['banner_img'],
            quantity = request.POST['quantity'],
            delivery = delivery
        )
    if request.FILES.getlist('images'):
        for img in request.FILES.getlist('images'):
            models.ProductImg.objects.create(
                product = product,
                img = img
        )
    if request.FILES.getlist('videos'):
        for video in request.FILES.getlist('videos'):
            models.ProductVideo.objects.create(
                product = product,
                video = video
        )
        return redirect('dashboard:product_list')
    return render(request, 'dashboard/product/create.html', context)



def product_update(request, code):

    queryset = models.Product.objects.get(code=code)
    category = models.Category.objects.all()
    images = models.ProductImg.objects.filter(product=queryset)
    videos = models.ProductVideo.objects.filter(product=queryset)
    context = {
          'queryset':queryset,
          'category':category,
          'images':images,
          'videos':videos
    }
    if request.method == 'POST':
        if request.FILES.get('banner_img'):
            product.banner_img = request.FILES.get('banner_img')
        delivery = True if request.POST.get('delivery') else False
        product.category_id = request.POST.get('category_id')
        product.name = request.POST.get('name')
        product.body = request.POST.get('body')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        product.delivery = delivery
        product.save()
    if request.FILES.getlist('product_img'):
        for img in request.FILES.getlist('product_img'):
            models.ProductImg.objects.create(
                product = product,
                img = img
        )
        return redirect('dashboard:product_list')
    return render(request, 'dashboard/product/update.html',context )


def product_delete(request, code):
    product = models.Product.objects.get(code=code)
    product.delete()
    return redirect('dashboard:product_list')


# ---------ENTER PRODUCT----------------
def create_product_enter(request):
    products = models.Product.objects.all()  # Yuqoridagi qatorni ko'chirib olib, POST so'rovi qilgandan keyin ishlatish uchun

    if request.method == 'POST':
        product_code = request.POST.get('product_code')
        product = models.Product.objects.get(code=product_code)
        quantity = request.POST.get('quantity')
        models.EnterProduct.objects.create(
            product=product,
            quantity=int(quantity)
        )

        return redirect('dashboard:product_list')

    context = {
        'products': products
    }
    return render(request, 'dashboard/eproduct/create.html', context)



def update_product_enter(request,code):
    if request.method == 'POST':
        enter_product = models.EnterProduct.objects.get(code=code)
        quantity = request.POST.get('quantity')
        enter_product.quantity = quantity
        enter_product.save()
    return redirect('dashboard:list_product_enter')
    


@staff_required
def list_product_enter(request):
    products = models.Product.objects.all()
    context = {
          'products':products
    }
    return render(request, 'dashboard/eproduct/list.html', context)


@staff_required
def detail_product_enter(request,code):
    queryset = models.EnterProduct.objects.filter(product__code=code)
    context = {
          'queryset':queryset
    }
    return render(request, 'dashboard/eproduct/detail.html', context)


@staff_required
def product_history(request,code):
    queryset = models.EnterProduct.objects.filter(product__code=code)
    outs = models.CartProduct.objects.filter(product__code=code,cart__status=4)
    data = list(chain(queryset, outs))
    data = sorted(data, key=lambda x: x.date, reverse=True)
    context = {
          'queryset':queryset
    }
    return render(request, 'dashboard/eproduct/history.html', context)


# def enter_product_detail(request, code):
#     product = models.Product.objects.all()
#     queryset = models.EnterProduct.objects.filter(product__code=code)
#     context = {
#           'queryset':queryset,
#           'product':product,
#     }
#     return render(request, 'dashboard/eproduct/detail.html', context)
    # queryset = models.Product.objects.get(code=code)
    # images = models.ProductImg.objects.filter(product=queryset)
    # reviews = models.Review.objects.filter(product=queryset)
    # ratings = range(5,0,-1)
    # videos = models.ProductVideo.objects.filter(product=queryset)
    # context = {
    #       'queryset':queryset,
    #       'images':images,
    #       'reviews':reviews,
    #       'ratings':ratings,
    #       'videos':videos
    # }

# def enter_product_update(request, code):

#     context = {
#         'queryset': models.EnterProduct.objects.get(code=code),
#         'products': models.Product.objects.all()
#     }

#     if request.method == 'POST':
#         product = request.POST.get('product_id')
#         quantity = request.POST.get('quantity')
#         quantity = int(quantity)
#         a = models.EnterProduct.objects.get(code=code)
#         a.product_id = product
#         a.quantity = quantity
#         a.save()
#         return redirect('dashboard:enter_product_list')
#     return render(request, 'dashboard/eproduct/update.html', context)

# def enter_product_create(request):
#     context = {'product': models.Product.objects.all()}
#     if request.method == 'POST':
#         product = models.Product.objects.get(code=request.POST.get('code'))
#         quantity = request.POST.get('quantity')
#         quantity = int(quantity)
#         models.EnterProduct.objects.create(
#             product=product,
#             quantity=quantity,
#         )
#     return render(request, 'dashboard/eproduct/create.html',context)

# def enter_product_list(request):
#     queryset = models.EnterProduct.objects.all()
#     context = {
#         'queryset': queryset
#     }
#     return render(request, 'dashboard/eproduct/list.html', context)


def product_delete(request, code):
    queryset = models.EnterProduct.objects.all()
    queryset.delete()
    return redirect('dashboard:enter_product_list')
    return render(request, 'dashboard/eproduct/detail.html', {'code': code})


def review(request, id):
    review = models.Review.objects.get(id=id)
    context = {
          'review':review
    }
    return render(request, 'dashboard/product/detail.html', context)

