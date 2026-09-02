from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, CartItem, Order, OrderItem


def cart_count_processor(request):
    if request.user.is_authenticated:
        count = sum(item.quantity for item in CartItem.objects.filter(user=request.user))
    else:
        count = 0
    return {'cart_count': count}


def product_list(request):
    category_slug = request.GET.get('category')
    query = request.GET.get('q')
    categories = Category.objects.all()
    products = Product.objects.all()

    if category_slug:
        products = products.filter(category__slug=category_slug)
    if query:
        products = products.filter(name__icontains=query)

    return render(request, 'product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_slug,
        'query': query
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product_detail.html', {'product': product})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f"Updated quantity for {product.name}.")
        else:
            messages.warning(request, "Cannot exceed available stock.")
    else:
        messages.success(request, f"Added {product.name} to cart.")
        
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))


@login_required
def update_cart(request, item_id, action):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if action == 'increase':
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.warning(request, "Maximum available stock reached.")
    elif action == 'decrease':
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()
    elif action == 'delete':
        cart_item.delete()
        messages.info(request, "Item removed from cart.")
        
    return redirect('cart_view')


@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in items)
    return render(request, 'cart.html', {'items': items, 'total_price': total_price})


@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user)
    if not items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('product_list')

    total_price = sum(item.get_total_price() for item in items)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            address=address,
            city=city,
            postal_code=postal_code,
            total_amount=total_price,
            status='Processing'
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
            item.product.stock -= item.quantity
            item.product.save()

        items.delete()
        return redirect('order_success', order_id=order.id)

    return render(request, 'checkout.html', {'items': items, 'total_price': total_price})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_success.html', {'order': order})


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('product_list')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.info(request, "You have logged out.")
    return redirect('product_list')