from django.http import HttpResponse
from django.shortcuts import render , redirect
from shopkeeper.models import Category
import json
from shopkeeper.models import Product
from shop.models import feedback
from django.core.paginator import Paginator

def about(request):
    testimonials_list = feedback.objects.all().order_by('-created_at')
    paginator = Paginator(testimonials_list, 5)  # 5 per page
    page_number = request.GET.get('page')
    testimonials = paginator.get_page(page_number)
    if request.method=="POST":
        msg=request.POST.get("msg")

        feedback.objects.create(
            user=request.user,
            msg=msg
        )
        return redirect('about')
    return render(request, 'about.html', {
        'testimonials': testimonials}
    )       

def home(request):
    categories = Category.objects.filter(is_featured=True)[:8]
    products = Product.objects.order_by('-created_at')[:12]

    data = []

    for p in products:
        img = p.productimage_set.first()
    
        if img and img.image:
            image_url = img.image.url
        else:
            image_url = ""   # empty → handled in JS

        data.append({
            "id":p.id,
            "name": p.name,
            "image": image_url
        })

    context = {
        "categories": categories,
        "products_json": json.dumps(data)
    }

    return render(request, "index.html", context)
