from django.shortcuts import render
from .models import Product
from .forms import ProductForm
from .models import ProductImage
from .models import Category
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
app_name = "shopkeeper"
# @login_required
def product_view(request):
    categories = Category.objects.all() 
    if request.method=='POST':
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        colour = request.POST.get("colour")
        image = request.FILES.getlist("images")
        selected_sizes = request.POST.getlist("sizes")
        
        category_ids = request.POST.getlist('category') 
    
        product=Product.objects.create(
            name=name,
            description=description,
            price=price,
            colour=colour,
            sizes=selected_sizes,
            owner=request.user       #THIS CONNECTS PRODUCT TO OWNER
        )
        product.category.set(category_ids)


        for img in image:
         ProductImage.objects.create(
         product=product,
         image=img
        ) 
        
        return redirect("shopkeeper:add")
    return render(request,'add.html', {
        'categories': categories})


def upload(request):
    return render(request, 'upload.html')

# @login_required
def product_list(request):
    products = Product.objects.filter(owner=request.user)
    return render(request,'product_list.html',
                  {'products':products})

@login_required
def product_update(request, id):
    product = Product.objects.get(id=id, owner=request.user)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            product = form.save()

            # Handle multiple images
            images = request.FILES.getlist('images')
            for image in images:
                ProductImage.objects.create(product=product, image=image)

            return redirect('shopkeeper:product_list')

    else:
        form = ProductForm(instance=product)

    return render(request, 'update_product.html', {
        'form': form,
        'product': product   # send product for showing existing images
    })

@login_required
def delete_image(request, id):
    image = get_object_or_404(ProductImage, id=id)

    # security check (very important)
    if image.product.owner != request.user:
        return redirect('shopkeeper:product_list')

    image.delete()
    return redirect('shopkeeper:product_update', id=image.product.id)
@login_required
def product_delete(request,id):
    product = Product.objects.get(id=id, owner=request.user)
    if request.method == "POST":
        product.delete()
        return redirect("shopkeeper:product_list")

    return render(request, "confirm_delete.html", {"product": product})

