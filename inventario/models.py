from django.db import models

from django.db import models

class VentaCamiseta(models.Model):
    # Datos de la camiseta
    id_camiseta = models.CharField(max_length=50, unique=True)
    marca = models.CharField(max_length=120)
    talla_camiseta = models.CharField(max_length=20)
    cantidad_camiseta = models.IntegerField()
    precio_camiseta = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Datos del cliente y pago
    nombre_cliente = models.CharField(max_length=100)
    metodo_de_pago = models.CharField(max_length=50)
    fecha_de_pago = models.DateField()
    
    # Datos de ubicación
    pais = models.CharField(max_length=120)
    ciudad = models.CharField(max_length=120)
    barrio = models.CharField(max_length=120)

