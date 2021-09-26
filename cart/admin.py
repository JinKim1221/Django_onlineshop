import csv 
from django.contrib import admin
from django.http.response import HttpResponse
from .models import Order, OrderItem
# Register your models here.
import datetime

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename={}.csv'.format(opts.verbose_name)  

    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])

    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.naem)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%d-%m-%Y")
            data_row.append(value)
        writer.writerow(data_row)
    return response    

export_to_csv.short_description = 'Export_to_CSV'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

from django.urls import reverse
from django.utils.safestring import mark_safe

def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    html = mark_safe(f"<a href='{url}'>Detail</a>")
    return html
order_detail.short_description = 'Detail' # HEAD in admin page 

def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    html = mark_safe(f"<a href='{url}'>PDF</a>")
    return html
order_pdf.short_description = 'PDF'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', order_detail, order_pdf, 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]

admin.site.register(Order, OrderAdmin)