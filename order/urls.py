from django.urls import path
from . import views
app_name="order"
urlpatterns = [
    path('checkout/',views.checkout,name='checkout'),
    path("review/", views.review_order, name="review_order"),
    path('place-order/',views.place_order,name="place_order"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("details/<int:order_id>/", views.order_details, name="order_details"),
    path("confirm-delivery/<int:order_id>/", views.confirm_delivery, name="confirm_delivery"),
]
