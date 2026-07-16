from django.shortcuts import render , redirect , get_object_or_404
from shop.models import UserProfile
from .models import Order
from shopkeeper.models import Product
from decimal import Decimal
from django.contrib import messages
from .models import Order, OrderItem
from datetime import timedelta
from django.utils import timezone
def checkout(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        request.session["checkout_data"] = {
            "name": request.POST.get("name"),
            "phone": request.POST.get("phone"),
            "address": request.POST.get("address"),
        }

        checkout_type = request.session.get("checkout_type")
        products = []
        total = 0
        # ---------------- CART ---------------- #

        if checkout_type == "cart":
            cart = request.session.get("cart", {})
            for product_id, item in cart.items():
                product = get_object_or_404(Product, id=product_id)
                subtotal = product.price * item["quantity"]
                products.append({
                    "product_id": product.id,
                    "name": product.name,
                    "price": float(product.price),
                    "quantity": item["quantity"],
                    "size": item["size"],
                    "subtotal": float(subtotal),
                })
                total += subtotal

        # ---------------- BUY NOW ---------------- #

        else:

            buy_now = request.session.get("buy_now")

            product = get_object_or_404(
                Product,
                id=buy_now["product_id"]
            )

            subtotal = product.price * buy_now["quantity"]

            products.append({

                "product_id": product.id,
                "name": product.name,
                "price": float(product.price),
                "quantity": buy_now["quantity"],
                "size": buy_now["size"],
                "subtotal": float(subtotal),

            })

            total += subtotal

        request.session["review_products"] = products
        request.session["review_total"] = float(total)

        return redirect("order:review_order")

    return render(request, "checkout.html", {
        "profile": profile
    })

def review_order(request):

    customer = request.session.get("checkout_data")
    review_products = request.session.get("review_products", [])
    products = []

    for item in review_products:
        product = get_object_or_404(Product, id=item["product_id"])
        products.append({
            "product": product,
            "name": item["name"],
            "price": item["price"],
            "quantity": item["quantity"],
            "size": item["size"],
            "subtotal": item["subtotal"],
        })

    total = request.session.get("review_total")

    return render(request, "review.html",
        {
            "customer": customer,
            "products": products,
            "total": total,
        }
    )

def confirm_delivery(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user
    )

    if order.status == "out_for_delivery":

        order.status = "delivered"
        order.delivered_at = timezone.now()
        order.save()

        messages.success(request, "Delivery confirmed successfully.")

    return redirect("order:order_details", order.id)

def my_orders(request):

    orders = Order.objects.filter(
        customer=request.user
    ).order_by("-created_at")

    orders_data = []
    for order in orders:

        first_item = order.items.first()
        image = None
        if first_item:

            first_image = first_item.product.productimage_set.first()
            if first_image:
                image = first_image.image.url

        orders_data.append({
            "order": order,
            "image": image,
        })

    return render( request, "my_order.html",
        {
            "orders_data": orders_data
        }
    )

def order_details(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user
    )

    items = OrderItem.objects.filter(
        order=order
    ).select_related("product")

    return render(
        request,
        "order_details.html",
        {
            "order": order,
            "items": items,
        }
    )

def place_order(request):

    if request.method != "POST":
        return redirect("order:review_order")

    customer = request.session.get("checkout_data")
    review_products = request.session.get("review_products", [])
    total = request.session.get("review_total")

    order = Order.objects.create(
        customer=request.user,
        name=customer["name"],
        phone=customer["phone"],
        address=customer["address"],
        total_amount=Decimal(str(total)),
        estimated_delivery=timezone.now().date() + timedelta(days=4),
    )

    for item in review_products:
        product = get_object_or_404( Product, id=item["product_id"])

        OrderItem.objects.create(
            order=order,
            product=product,
            shopkeeper=product.owner,
            quantity=item["quantity"],
            size=item["size"],
            price=product.price,
            subtotal=Decimal(str(item["subtotal"]))
        )

        product.stock -= item["quantity"]
        product.save()

    request.session.pop("cart", None)
    request.session.pop("buy_now", None)
    request.session.pop("checkout_data", None)
    request.session.pop("review_products", None)
    request.session.pop("review_total", None)

    messages.success(request, "Order placed successfully.")
    return redirect("home")