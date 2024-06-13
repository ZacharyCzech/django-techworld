from django.contrib import admin
from .models import Category, Subcategory, Customer, Product, Order, OrderItem, CustomerManager
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _


class CustomerAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ()}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    fields = ["customer", "total_price", "date_ordered"]
    inlines = [OrderItemInline]


admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)

