from django.urls import path
from . import views
app_name="shop"
urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("login/", views.login_view, name="login"),
]
