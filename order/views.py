from django.shortcuts import render , redirect , get_object_or_404
from shop.models import UserProfile
from .models import Order
from shopkeeper.models import Product
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

        product = get_object_or_404(
            Product,
            id=item["product_id"]
        )

        products.append({
            "product": product,
            "name": item["name"],
            "price": item["price"],
            "quantity": item["quantity"],
            "size": item["size"],
            "subtotal": item["subtotal"],
        })

    total = request.session.get("review_total")

    return render(
        request,
        "review.html",
        {
            "customer": customer,
            "products": products,
            "total": total,
        }
    )