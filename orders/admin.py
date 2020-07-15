from django.contrib import admin

from .models import Addition, CartItem, DinnerPlatter, Pasta, RegularPizza, Salad, SicilianPizza, Sub, Topping, Order


# Register your models here.
class RegularPizzaInline(admin.TabularInline):
    model = RegularPizza.toppings.through


class SicilianPizzaInline(admin.TabularInline):
    model = SicilianPizza.toppings.through


class ToppingAdmin(admin.ModelAdmin):
    inlines = [RegularPizzaInline, SicilianPizzaInline]


class SubInline(admin.TabularInline):
    model = Sub.additions.through


class AdditionAdmin(admin.ModelAdmin):
    inlines = [SubInline]


class PizzaAdmin(admin.ModelAdmin):
    filter_horizontal = ("toppings",)


class SubAdmin(admin.ModelAdmin):
    filter_horizontal = ("additions",)


class CartItemAdmin(admin.ModelAdmin):
    readonly_fields = ("content_type", "object_id", "size", "toppings", "additions", "price", "user")


class CartItemInline(admin.TabularInline):
    model = CartItem
    readonly_fields = ("content_type", "size", "toppings", "additions", "price")
    exclude = ["user", "pending", "object_id"]
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]

    def get_queryset(self, request):
        qs = super(OrderAdmin, self).get_queryset(request)
        return qs.filter(complete=False)


admin.site.register(Topping, ToppingAdmin)
admin.site.register(Addition, AdditionAdmin)
admin.site.register(RegularPizza, PizzaAdmin)
admin.site.register(SicilianPizza, PizzaAdmin)
admin.site.register(Sub, SubAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(DinnerPlatter)
