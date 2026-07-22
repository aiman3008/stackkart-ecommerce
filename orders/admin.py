import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.action(description='Export selected orders as CSV')
def export_orders_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'User', 'Status', 'Total', 'Created'])
    for order in queryset:
        writer.writerow([order.id, order.user, order.status, order.total, order.created_at])
    return response

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    actions = [export_orders_csv]
    inlines = [OrderItemInline]
