from django.shortcuts import render
from inventario.models import VentaCamiseta
import plotly.express as px
import pandas as pd



def saludar(request):

    ventas = VentaCamiseta.objects.all()

    df = pd.DataFrame({
        "id_camiseta":["OVRS_Tr","OVRS_Jr","OVRS_Ind"],
        "marca":["Nike","Adidas","Lacoste"],
        "talla_camiseta":["M","L","XL"],
        "cantidad_camiseta":["1","2","3"],
        "precio_camiseta":["55000.00","53000.00","52000.00"],
        "nombre_cliente":["Andres Felipe López Anaya", "Juan Sebastian Camacho Dueñas", "Juan Rosales Gonzales"],
        "metodo_de_pago":["Efectivo", "Tarjeta", "Transferencia"],
        "fecha_de_pago":["Jan. 18, 2024", "Jun. 18, 2024", "Jul. 18, 2024"],
        "pais":["Colombia", "Mexico", "USA"],
        "ciudad":["Bogotá D.C", "Cali", "New York"],
        "barrio":["Bosa", "El retiro", "Dominic"],
    })

    grafico = px.bar(df, x = "marca", y = "cantidad_camiseta", color = "pais")

    mihtml = grafico.to_html(full_html = False)

    context = {
        "nombre": "andres",
        "camisetas": ventas,
        "grafica": mihtml
    }
    return render(request, "inventario/index.html", context)
# Create your views here.
