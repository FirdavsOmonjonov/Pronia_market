from django.urls import path
from . import views


app_name = 'front'



urlpatterns = [
    path('', views.index, name='index'),
    path('category-list/<int:id>/', views.category_list, name='category_list'),
    path('product-detail/<int:id>/', views.product_detail, name='product_detail'),
    path('product-list/', views.product_list, name='product_list'),
    path('carts/', views.carts, name='carts'),
    path('cart/<str:code>/', views.cart_detail, name='cart_detail'),
    path('active/cart', views.active_cart, name='active_cart'),
    path('delete/cart/<int:id>/', views.delete_cart, name='delete_cart'),
    path('update_quantity/<int:id>/', views.update_quantity, name='update_quantity'),
    path('add-cart/<str:code>', views.add_cart, name='add_cart'),
    path('wish-list', views.list_wishlist, name='list_wishlist'),
    path('remove-wishlist/<str:code>/', views.remove_wishlist, name='remove_wishlist'),
    path('create-wishlist/<str:code>/', views.add_wishlist, name='add_wishlist'),


   
]