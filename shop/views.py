from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth import authenticate
from django.contrib.auth import login
import random
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

def register_view(request):

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        address = request.POST.get("address")
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        # Check duplicate username
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("shop:register")

        # Check duplicate email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect("shop:register")

        # Check duplicate phone
        if UserProfile.objects.filter(phone=phone).exists():
            messages.error(request, "Phone already registered!")
            return redirect("shop:register")

        otp = str(random.randint(100000, 999999))

        request.session["pending_user"] = {
            "full_name": full_name,
            "address": address,
            "username": username,
            "email": email,
            "phone": phone,
            "password": password,
            "otp": otp,
        }

        # Send OTP to phone
        try:
         send_mail(
        "Your OTP Verification",
        f"Your OTP is {otp}. It is valid for 5 minutes.",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
        except Exception:
           messages.error(request, "Unable to send OTP. Please try again.")
           return redirect("shop:register")

        return redirect("shop:verify_otp")

    return render(request, "register.html")

def verify_otp(request):

    data = request.session.get("pending_user")

    if not data:
        return redirect("shop:register")

    if request.method == "POST":

        entered_otp = request.POST.get("otp")

        if entered_otp == data["otp"]:

            user = User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"],
                first_name=data["full_name"],   # Full Name
            )

            UserProfile.objects.create(
                user=user,
                phone=data["phone"],
                address=data["address"],
                otp=entered_otp,
                otp_created_at=timezone.now(),
            )

            del request.session["pending_user"]

            messages.success(request, "Account created successfully!")
            return redirect("shop:login")

        else:
            messages.error(request, "Invalid OTP!")

    return render(request, "otp.html")

def login_view(request):
    if request.method=="POST":
         username = request.POST.get("username")
         password = request.POST.get("password")
         user = authenticate(username=username, password=password)
        
         if user is not None:
            login(request, user)
     
            messages.success(
                request,
                f"Welcome, {user.username}!"
            )
            print("Role =", user.userprofile.login_as)
            #  Check role
            if user.userprofile.login_as == "customer":
                return redirect("customer:items3")

            elif user.userprofile.login_as == "Shopkeeper":
                return redirect("shopkeeper:upload")
         else:
            messages.error(request, "Invalid username or password")    

    return render(request, "login.html")
        
