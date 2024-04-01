from django.contrib import admin
from inventario.models import VentaCamiseta

class InventarioAdmin(admin.ModelAdmin):
    pass

admin.site.register(VentaCamiseta)
# Register your models here.
