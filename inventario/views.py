from django.shortcuts import render
from inventario.models import VentaCamiseta
import plotly.express as px
import pandas as pd

def saludar(request):

    ventas = VentaCamiseta.objects.all()

    # Construir el DataFrame usando los datos de ventas
    data = {
        "id_camiseta": [venta.id_camiseta for venta in ventas],
        "marca": [venta.marca for venta in ventas],
        "talla_camiseta": [venta.talla_camiseta for venta in ventas],
        "cantidad_camiseta": [venta.cantidad_camiseta for venta in ventas],
        "precio_camiseta": [venta.precio_camiseta for venta in ventas],
        "nombre_cliente": [venta.nombre_cliente for venta in ventas],
        "metodo_de_pago": [venta.metodo_de_pago for venta in ventas],
        "fecha_de_pago": [venta.fecha_de_pago.strftime('%b. %d, %Y') for venta in ventas],
        "pais": [venta.pais for venta in ventas],
        "ciudad": [venta.ciudad for venta in ventas],
        "barrio": [venta.barrio for venta in ventas],
    }

    df = pd.DataFrame(data)

    # Generar el gráfico de ejemplo
    grafico = px.bar(df, x="marca", y="cantidad_camiseta", color="pais")
    grafico_html = grafico.to_html(full_html=False)

    # Generar grafico de Metodo de pago (PIE)
    porcentaje_metodo_pago = df['metodo_de_pago'].value_counts(normalize=True) * 100
    grafico_metodo_pago = px.pie(names=porcentaje_metodo_pago.index, values=porcentaje_metodo_pago.values, title='Porcentaje de compras por método de pago')
    grafico_metodo_pago_html = grafico_metodo_pago.to_html(full_html=False)

     # Marca más vendida
    marca_mas_vendida = df['marca'].value_counts().idxmax()
    grafico_marca_mas_vendida = px.bar(x=df['marca'].value_counts().index, y=df['marca'].value_counts().values, orientation='h', title='Ventas por marca')
    grafico_marca_mas_vendida_html = grafico_marca_mas_vendida.to_html(full_html=False)

    # Venta más cara y quién la realizó
    venta_mas_cara = df[df['precio_camiseta'] == df['precio_camiseta'].max()]
    venta_mas_cara_detalles = venta_mas_cara[['nombre_cliente', 'precio_camiseta']]
    grafico_venta_mas_cara = px.bar(x=venta_mas_cara_detalles['nombre_cliente'], y=venta_mas_cara_detalles['precio_camiseta'], title='Venta más cara y quién la realizó')
    grafico_venta_mas_cara_html = grafico_venta_mas_cara.to_html(full_html=False)

    # Barrio que más compró
    barrio_mas_compras = df['barrio'].value_counts().idxmax()
    grafico_barrio_mas_compras = px.bar(x=df['barrio'].value_counts().index, y=df['barrio'].value_counts().values, title='Compras por barrio')
    grafico_barrio_mas_compras_html = grafico_barrio_mas_compras.to_html(full_html=False)

    # Talla más vendida
    talla_mas_vendida = df['talla_camiseta'].value_counts().idxmax()
    grafico_talla_mas_vendida = px.pie(names=df['talla_camiseta'].value_counts().index, values=df['talla_camiseta'].value_counts().values, title='Distribución de ventas por talla')
    grafico_talla_mas_vendida_html = grafico_talla_mas_vendida.to_html(full_html=False)

    # Crear el gráfico de violín
    grafico_violin = px.violin(df, x='marca', y='precio_camiseta', title='Distribución de precios de camisetas por marca')

    # Obtener el HTML del gráfico
    grafico_violin_html = grafico_violin.to_html(full_html=False)

    context = {
        "nombre": "andres",
        "camisetas": ventas,
        "grafica": grafico_html,
        "graficados": grafico_metodo_pago_html,
        "graficatres": grafico_marca_mas_vendida_html,
        "graficacuatro": grafico_venta_mas_cara_html,
        "graficacinco": grafico_barrio_mas_compras_html,
        "graficaseis": grafico_talla_mas_vendida_html,
        "graficasiete": grafico_violin_html
    }
    return render(request, "inventario/index.html", context)
