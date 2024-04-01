from django.contrib import admin
from inventario.models import VentaCamiseta

class InventarioAdmin(admin.ModelAdmin):
    list_display = ["id_camiseta","marca","talla_camiseta","cantidad_camiseta","precio_camiseta","nombre_cliente","metodo_de_pago", "fecha_de_pago", "pais", "ciudad", "barrio"]

admin.site.register(VentaCamiseta, InventarioAdmin)
# Register your models here.
