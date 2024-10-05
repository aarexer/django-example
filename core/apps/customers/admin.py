from django.contrib import admin

from core.apps.customers.models.customers import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'created_at')
    search_fields = ('phone',)
