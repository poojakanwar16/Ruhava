from django.urls import path
from . import views

app_name = "shopkeeper"

urlpatterns = [
    path('upload/',views.upload,name='upload'),
    path('add/',views.product_view,name='add'),
    path('products_list/', views.product_list, name='product_list'),
    path('product/update/<int:id>/', views.product_update, name='product_update'),
    path('product/delete/<int:id>/', views.product_delete, name='product_delete'),
    path('image/delete/<int:id>/', views.delete_image, name='delete_image'),
    path('shopkeer_orders/',views.shopkeeper_orders,name="shopkeeper_orders"),
]
