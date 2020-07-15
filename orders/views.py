import os
import re

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import stripe

from .models import Addition, CartItem, DinnerPlatter, Order, Pasta, RegularPizza, Salad, SicilianPizza, Sub, Topping

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
DOMAIN = os.getenv("DOMAIN")

stripe.api_key = STRIPE_SECRET_KEY


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login_view"))

    regular_pizzas = RegularPizza.objects.all()
    sicilian_pizzas = SicilianPizza.objects.all()
    subs = Sub.objects.all()
    pasta = Pasta.objects.all()
    salads = Salad.objects.all()
    dinner_platters = DinnerPlatter.objects.all()
    cart_items = CartItem.objects.filter(
        user=request.user,
        pending=False
    )

    return render(request, "orders/index.html", {
        "regular_pizzas": regular_pizzas,
        "sicilian_pizzas": sicilian_pizzas,
        "subs": subs,
        "pasta": pasta,
        "salads": salads,
        "dinner_platters": dinner_platters,
        "cart_items": cart_items
    })

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        pattern = re.compile(r'\d.*?[A-Z].*?[a-z].*[^\da-zA-Z]')

        if not first_name:
            messages.error(request, "First Name may not be left blank.")
            return render(request, "orders/register.html")
        elif not last_name:
            messages.error(request, "Last Name may not be left blank.")
            return render(request, "orders/register.html")
        elif not username:
            messages.error(request, "Username may not be left blank.")
            return render(request, "orders/register.html")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username is unavailabe.")
            return render(request, "orders/register.html")
        elif not email:
            messages.error(request, "Email may not be left blank.")
            return render(request, "orders/register.html")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "User with this email already exists.")
            return render(request, "orders/register.html")
        elif not password:
            messages.error(request, "Password may not be left blank.")
            return render(request, "orders/register.html")
        elif pattern.search(password) and len(password) >= 8:
            messages.error(request, "Password must be at least 8 characters; must contain at least one lowercase letter, one uppercase letter, one numeric digit, and one special character.")
            return render(request, "register.html")
        elif not confirmation:
            messages.error(request, "Confirm Password may not be left blank.")
            return render(request, "orders/register.html")
        elif password != confirmation:
            messages.error(request, "Passwords must match.")
            return render(request, "register.html")

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        login(request, user)

        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "orders/register.html")

def check(request):
    username = request.GET.get("username")
    email = request.GET.get("email")

    if username and User.objects.filter(username=username).exists():
        return JsonResponse(False, safe=False)

    if email and User.objects.filter(email=email).exists():
        return JsonResponse(False, safe=False)

    return JsonResponse(True, safe=False)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username:
            messages.error(request, "Username may not be left blank.")
            return render(request, "orders/login.html")
        elif not password:
            messages.error(request, "Password may not be left blank.")
            return render(request, "orders/login.html")

        user = authenticate(request, username=username, password=password)

        if not user:
            messages.error(request, "Invalid username and/or password.")
            return render(request, "orders/login.html")

        login(request, user)

        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "orders/login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out.")

    return HttpResponseRedirect(reverse("login_view"))

def add_to_cart(request):
    item = request.POST.get("item")
    size = request.POST.get("size")
    toppings = request.POST.getlist("topping_ids")
    additions = request.POST.getlist("addition_ids")

    try:
        item_id = item.split("-")[-1]
        if item.startswith("reg-pizza"):
            item = RegularPizza.objects.get(pk=item_id)
        elif item.startswith("sic-pizza"):
            item = SicilianPizza.objects.get(pk=item_id)
        elif item.startswith("sub"):
            item = Sub.objects.get(pk=item_id)
        elif item.startswith("pasta"):
            item = Pasta.objects.get(pk=item_id)
        elif item.startswith("salad"):
            item = Salad.objects.get(pk=item_id)
        elif item.startswith("dinner-platter"):
            item = DinnerPlatter.objects.get(pk=item_id)
        else:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        messages.error(request, "Invalid Data.")
        return HttpResponseRedirect(reverse("index"))

    if getattr(item, "sm_price", False):
        if size == "Small":
            price = item.sm_price
        elif size == "Large":
            price = item.lg_price
        else:
            messages.error(request, "Please choose a size.")
            return HttpResponseRedirect(reverse("index"))
    else:
        if size is None:
            price = item.price
        else:
            messages.error(request, "Invalid Data.")
            return HttpResponseRedirect(reverse("index"))

    if getattr(item, "toppings", False):
        expected_toppings = 0
        if item.name in ("1 topping", "1 item"):
            expected_toppings = 1
        elif item.name in ("2 toppings", "2 items"):
            expected_toppings = 2
        elif item.name in ("3 toppings", "3 items"):
            expected_toppings = 3
        elif item.name == "Special":
            expected_toppings = 4

        num_toppings = min(4, len(toppings))
        if expected_toppings != num_toppings:
            messages.error(request, "Please select the correct number of toppings.")
            return HttpResponseRedirect(reverse("index"))

        for i, topping_id in enumerate(toppings):
            try:
                toppings[i] = Topping.objects.get(pk=topping_id)
                if toppings[i] not in item.toppings.all():
                    raise ObjectDoesNotExist

            except ObjectDoesNotExist:
                messages.error(request, "Invalid Data.")
                return HttpResponseRedirect(reverse("index"))

    else:
        if len(toppings) > 0:
            messages.error(request, "Invalid Data.")
            return HttpResponseRedirect(reverse("index"))

    if getattr(item, "additions", False):
        for i, addition_id in enumerate(additions):
            try:
                additions[i] = Addition.objects.get(pk=addition_id)
                if additions[i] in item.additions.all():
                    price += additions[i].price
                else:
                    raise ObjectDoesNotExist

            except ObjectDoesNotExist:
                messages.error(request, "Invalid Data.")
                return HttpResponseRedirect(reverse("index"))
    else:
        if len(additions) > 0:
            messages.error(request, "Invalid Data.")
            return HttpResponseRedirect(reverse("index"))

    cart_item = CartItem(
        item=item,
        size=size,
        price=price,
        user=request.user
    )
    cart_item.save()
    cart_item.toppings.set(toppings)
    cart_item.additions.set(additions)
    cart_item.save()

    return HttpResponseRedirect(reverse("index"))

def cart(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get("cart_item_id")

        try:
            cart_item = CartItem.objects.get(pk=cart_item_id)
        except ObjectDoesNotExist:
            messages.error(request, "Invalid Data.")
            return HttpResponseRedirect(reverse("index"))

        cart_item.delete()

        return HttpResponseRedirect(reverse("cart"))

    else:
        cart_items = CartItem.objects.filter(
            user=request.user,
            pending=False
        )
        total_price = sum([cart_item.price for cart_item in cart_items])

        return render(request, "orders/cart.html", {
            "cart_items": cart_items,
            "total_price": total_price
        })

def stripe_session(request):
    cart_items = CartItem.objects.filter(
        user=request.user,
        pending=False
    )
    total_price = sum([cart_item.price for cart_item in cart_items])

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": "Pinocchio's Pizza & Subs",
                },
                "unit_amount": int(total_price * 100),
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=f"{DOMAIN}{HttpResponseRedirect(reverse('checkout')).url}?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{DOMAIN}{HttpResponseRedirect(reverse('cart')).url}"
    )

    return JsonResponse({
        "session_id": session.id,
        "stripe_public_key": STRIPE_PUBLIC_KEY
    })

def checkout(request):
    cart_items = CartItem.objects.filter(
        user=request.user,
        pending=False
    )
    total_price = sum([cart_item.price for cart_item in cart_items])

    order = Order(
        user=request.user,
        total_price=total_price
    )
    order.save()

    for cart_item in cart_items:
        cart_item.order = order
        cart_item.pending = True
        cart_item.save()

    messages.success(request, "Order successfully submitted!")

    return HttpResponseRedirect(reverse("index"))

def orders(request):
    cart_items = CartItem.objects.filter(
        user=request.user,
        pending=False
    )
    current_orders = Order.objects.filter(
        user=request.user,
        complete=False
    )
    past_orders = Order.objects.filter(
        user=request.user,
        complete=True
    )

    return render(request, "orders/orders.html", {
        "cart_items": cart_items,
        "current_orders": current_orders,
        "past_orders": past_orders
    })
