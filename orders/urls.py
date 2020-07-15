from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("check", views.check, name="check"),
    path("login", views.login_view, name="login_view"),
    path("logout", views.logout_view, name="logout_view"),
    path("add_to_cart", views.add_to_cart, name="add_to_cart"),
    path("cart", views.cart, name="cart"),
    path("stripe_session", views.stripe_session, name="stripe_session"),
    path("checkout", views.checkout, name="checkout"),
    path("orders", views.orders, name="orders")
]
