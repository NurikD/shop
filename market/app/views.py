from django.shortcuts import render, get_object_or_404, redirect
from .models import * # если товары уже есть в моделях
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

def base(request):
    products = Product.objects.all()[:8]  # Выводим первые 8 товаров
    return render(request, 'base.html', {'products': products})

def home(request):
    products = Product.objects.all()[:8]
    return render(request, 'home.html', {'products': products})

def catalog(request):
    products = Product.objects.all()

    # Фильтрация по цене
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

    if price_min:
        try:
            products = products.filter(price__gte=int(price_min))
        except ValueError:
            pass
    if price_max:
        try:
            products = products.filter(price__lte=int(price_max))
        except ValueError:
            pass

    # Пагинация
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalog.html', {
        'products': page_obj,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    added = request.session.pop('added_to_cart', False)
    return render(request, 'product_detail.html', {
        'product': product,
        'added_to_cart': added,
    })


@require_POST
def add_to_cart(request, pk):
    quantity = int(request.POST.get('quantity', 1))

    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product_id=pk)
        cart_item.quantity += quantity
        cart_item.save()
    else:
        cart = request.session.get('cart', {})
        cart[str(pk)] = cart.get(str(pk), 0) + quantity
        request.session['cart'] = cart

    request.session['added_to_cart'] = True
    return redirect('product_detail', pk=pk)

@require_POST
def update_cart(request, pk):
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity', 1))

    if quantity > 0:
        cart[str(pk)] = quantity
    else:
        cart.pop(str(pk), None)  # удалить если 0

    request.session['cart'] = cart
    return redirect('cart')

def remove_from_cart(request, pk):
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user, product_id=pk).delete()
    else:
        cart = request.session.get('cart', {})
        cart.pop(str(pk), None)
        request.session['cart'] = cart

    return redirect('cart')


def clear_cart(request):
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user).delete()
    else:
        request.session['cart'] = {}

    return redirect('cart')



def cart_view(request):
    if request.user.is_authenticated:
        items = CartItem.objects.filter(user=request.user).select_related('product')
        cart_items = []
        total = 0

        for item in items:
            cart_items.append({
                'product': item.product,
                'quantity': item.quantity,
                'total': item.product.price * item.quantity,
            })
            total += item.product.price * item.quantity
    else:
        cart = request.session.get('cart', {})
        cart_items = []
        total = 0
        for product_id, quantity in cart.items():
            try:
                product = Product.objects.get(pk=product_id)
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'total': product.price * quantity,
                })
                total += product.price * quantity
            except Product.DoesNotExist:
                continue

    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

def base_context(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart = request.session.get('cart', {})
        cart_count = sum(cart.values())

    return {
        'cart_count': cart_count,
        # позже можно добавить 'wishlist_count': ...
    }

