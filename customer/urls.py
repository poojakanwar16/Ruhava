from django.urls import path
from . import views
app_name="customer"

urlpatterns = [
    path('products/<str:gender>/', views.items, name='items'),
    path('product/<int:id>/',views.product_detail,name='product_detail'),
    path('product-categories/<int:category_id>',views.items2,name='items2'),
    path('products/',views.items3,name='items3'),
    path('cart/',views.cart,name='cart'),
    path('add_to_cart/<int:product_id>/',views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('toggle-wishlist/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path("increase/<str:key>/", views.increase_qty, name="increase_qty"),
    path("decrease/<str:key>/", views.decrease_qty, name="decrease_qty"),
    path("checkout/",views.checkout_from_cart,name="checkout_from_cart",
),
]
