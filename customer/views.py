from django.shortcuts import render, redirect, get_object_or_404
from shopkeeper.models import Product
from shopkeeper.models import Category
from shopkeeper.models import ProductImage
from django.http import JsonResponse
from .models import Wishlist

def toggle_wishlist(request, product_id):
   if not request.user.is_authenticated:
        return redirect('account:login')   # change if your login url name is different

   product = get_object_or_404(Product, id=product_id)
   wishlist_item = Wishlist.objects.filter(
        user=request.user,
        product=product
    )
   if wishlist_item.exists():
        wishlist_item.delete()
   else:
        Wishlist.objects.create(
            user=request.user,
            product=product
        )
   return redirect(request.META.get('HTTP_REFERER', '/'))

# Wishlist page
def wishlist(request):

    if not request.user.is_authenticated:
        return redirect('account:login')

    wishlist_items = Wishlist.objects.filter(user=request.user)
    liked_ids = wishlist_items.values_list('product_id', flat=True)
    return render(
        request,
        'wishlist.html',
        {'wishlist_items': wishlist_items ,'liked_ids': liked_ids}
    )

def items(request, gender):
    products = Product.objects.filter(gender__iexact=gender)   #iexact handle case sensitive men/Men
    images = ProductImage.objects.all()
    if request.user.is_authenticated:
        liked_products = Wishlist.objects.filter(
            user=request.user
        ).values_list('product_id', flat=True)
    else:
        liked_products=[]    

    return render(request , 'product.html',{
        'products' : products,
        'liked_products': liked_products,
        'images':images
    })    

def product_detail(request, id):
    product = Product.objects.get(id=id)      # Main product
    images = ProductImage.objects.filter(product=product)
    products = Product.objects.all()          # Products for below section

    cart = request.session.get("cart", {})
    product_in_cart = any(str(id) in key for key in cart.keys())


    return render(request, "product_detail.html", {
        "product": product,
        "images": images,
        "products": products,
        "product_in_cart": product_in_cart
    })

def items2(request, category_id):
    products = Product.objects.filter(category__id=category_id).distinct()
    images = ProductImage.objects.all()
    if request.user.is_authenticated:
        liked_products = Wishlist.objects.filter(
            user=request.user
        ).values_list('product_id', flat=True)
    else:
        liked_products = []

    return render(request, 'product.html', {
        'products': products,
        'liked_products': liked_products,
        'category_id':category_id
    })

def items3(request):
    products=Product.objects.all()
    if request.user.is_authenticated:
        liked_products = Wishlist.objects.filter(
            user=request.user
        ).values_list('product_id', flat=True)
    else:
        liked_products = []

    return render(request, 'product.html', {
        'products': products,
        'liked_products': liked_products
    })

def cart(request):
    cart = request.session.get("cart", {})

    products = []
    total = 0

    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)

        subtotal = product.price * item["quantity"]

        products.append({
            "key": product_id,
            "product": product,
            "size": item["size"],
            "quantity": item["quantity"],
            "subtotal": subtotal,
        })

        total += subtotal

    return render(request, "cart.html", {
        "products": products,
        "total": total,
    })

def add_to_cart(request, product_id):

    if request.method != "POST":
        return redirect("customer:product_detail", id=product_id)

    selected_size = request.POST.get("selected_size")

    if not selected_size:
        return redirect("customer:product_detail", id=product_id)

    action = request.POST.get("action")

    product_id = str(product_id)

    # ================= BUY NOW =================

    if action == "buy":

        request.session["checkout_type"] = "buy_now"

        request.session["buy_now"] = {
            "product_id": product_id,
            "quantity": 1,
            "size": selected_size,
        }

        request.session.modified = True

        return redirect("order:checkout")

    # ================= ADD TO CART =================

    cart = request.session.get("cart", {})

    if product_id in cart:
        cart[product_id]["quantity"] += 1
    else:
        cart[product_id] = {
            "quantity": 1,
            "size": selected_size,
        }

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("customer:cart")

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('customer:cart')

def checkout_from_cart(request):

    request.session["checkout_type"] = "cart"

    return redirect("order:checkout")

def increase_qty(request, key):
    key = str(key)
    cart = request.session.get("cart", {})

    if key in cart:
        cart[key]["quantity"] += 1

    request.session["cart"] = cart
    return redirect("customer:cart")

def decrease_qty(request, key):
    key = str(key)
    cart = request.session.get("cart", {})

    if key in cart:
        cart[key]["quantity"] -= 1

        if cart[key]["quantity"] <= 0:
            del cart[key]

    request.session["cart"] = cart
    return redirect("customer:cart")