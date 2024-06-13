from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from store.models import Order, OrderItem, Customer, Product
from django.http import JsonResponse


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quantities()
    totals = cart.cart_total()

    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals})


def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty)
        cart_quantity = cart.__len__()

        response = JsonResponse({'qty': cart_quantity})
        return response


def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)

        response = JsonResponse({'qty': product_id})
        return response


def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty': product_qty})
        return response


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quantities()
    totals = cart.cart_total()

    return render(request, "checkout.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals})


def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_products()
        quantities = cart.get_quantities()
        totals = cart.cart_total()

        customer = request.user
        create_order = Order(customer=customer, total_price=totals)
        create_order.save()

        order_id = create_order.pk

        for product in cart_products:
            product_id = product.id
            price = product.price
            for key, value in quantities.items():
                if int(key) == product_id:
                    create_order_item = OrderItem(order_id=order_id, product_id=product_id, customer=customer, quantity=value, price=price)
                    create_order_item.save()

        for key in list(request.session.keys()):
            if key == "session_key":
                del request.session[key]

        return redirect('index')

    else:
        return redirect('index')

