from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Product
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm
from django.conf import settings


def product(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'product.html', {'product': product})


def index(request):
    return render(request, 'index.html', {})


def shop(request):
    category_id = request.GET.get('category', None)
    subcategory_id = request.GET.get('subcategory', None)
    query = request.GET.get('query', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    page_number = request.GET.get('page', 1)

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if subcategory_id:
        products = products.filter(subcategory_id=subcategory_id)
    elif category_id:
        products = products.filter(category_id=category_id)

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop.html', {
        'page_obj': page_obj,
        'products': page_obj.object_list,
    })


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                if not Customer.objects.filter(email=email).exists():
                    form.add_error('email', 'Ten e-mail nie jest zarejestrowany!')
                else:
                    form.add_error('password', 'Nieprawidłowe hasło!')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('index')


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form, 'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY})
