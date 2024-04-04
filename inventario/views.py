from django.shortcuts import render
from inventario.models import VentaCamiseta
import plotly.express as px
import pandas as pd

from django.shortcuts import render
from inventario.models import VentaCamiseta
import plotly.graph_objs as go
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

    # Generar el gráfico de barras
    grafico = go.Figure()
    grafico.add_trace(go.Bar(
        x=df['marca'],
        y=df['cantidad_camiseta'],
        marker_color='#007bff',  # Color de las barras
    ))

    grafico.update_layout(
        title='Ventas por Marca',
        xaxis=dict(title='Marca'),
        yaxis=dict(title='Cantidad de Camisetas Vendidas'),
        font=dict(family='Arial', size=12, color='#333'),  # Estilos de fuente
        plot_bgcolor='#f8f9fa',  # Color de fondo del gráfico
        paper_bgcolor='#fff',  # Color de fondo del papel
        margin=dict(l=50, r=50, t=50, b=50),  # Márgenes
    )
    grafico_html = grafico.to_html(full_html=False)

    # Generar el gráfico de pastel para método de pago
    porcentaje_metodo_pago = df['metodo_de_pago'].value_counts(normalize=True) * 100
    grafico_metodo_pago = go.Figure(go.Pie(
        labels=porcentaje_metodo_pago.index,
        values=porcentaje_metodo_pago.values,
    ))
    grafico_metodo_pago.update_traces(
        marker=dict(colors=['#007bff', '#28a745', '#dc3545']),  # Colores de las secciones del pastel
        textposition='inside',  # Posición del texto dentro del pastel
    )
    grafico_metodo_pago.update_layout(
        title='Porcentaje de compras por método de pago',
        font=dict(family='Arial', size=12, color='#333'),  # Estilos de fuente
        plot_bgcolor='#f8f9fa',  # Color de fondo del gráfico
        paper_bgcolor='#fff',  # Color de fondo del papel
        margin=dict(l=50, r=50, t=50, b=50),  # Márgenes
    )
    grafico_metodo_pago_html = grafico_metodo_pago.to_html(full_html=False)

    # Marca más vendida
    grafico_marca_mas_vendida = px.bar(
        x=df['marca'].value_counts().values,
        y=df['marca'].value_counts().index,
        orientation='h',
        title='Ventas por marca',
        labels={'x': 'Cantidad de Ventas', 'y': 'Marca'}
    )
    grafico_marca_mas_vendida.update_layout(
        font=dict(family="Arial", size=12, color="#333"),
        plot_bgcolor="#f8f9fa",
        paper_bgcolor="#fff",
        margin=dict(l=50, r=50, t=50, b=50)
    )
    grafico_marca_mas_vendida_html = grafico_marca_mas_vendida.to_html(full_html=False)

    # Calcular el precio total de cada venta
    df['precio_total'] = df['precio_camiseta'] * df['cantidad_camiseta']

    # Obtener la venta más cara
    venta_mas_cara = df[df['precio_total'] == df['precio_total'].max()]
    venta_mas_cara_detalles = venta_mas_cara[['nombre_cliente', 'precio_total']]

    # Obtener los detalles de la venta más cara
    nombre_cliente = venta_mas_cara_detalles['nombre_cliente'].values[0]
    precio_venta = venta_mas_cara_detalles['precio_total'].values[0]


    # Barrio que más compró
    barrio_mas_compras = df['barrio'].value_counts().idxmax()
    grafico_barrio_mas_compras = px.bar(
        x=df['barrio'].value_counts().index,
        y=df['barrio'].value_counts().values,
        title='Compras por barrio',
        labels={'x': 'Barrio', 'y': 'Cantidad de Compras'}
    )
    grafico_barrio_mas_compras.update_traces(marker_color='#28a745')  # Color de las barras
    grafico_barrio_mas_compras.update_layout(
        font=dict(family="Arial", size=12, color="#333"),
        plot_bgcolor="#f8f9fa",
        paper_bgcolor="#fff",
        margin=dict(l=50, r=50, t=50, b=50)
    )
    grafico_barrio_mas_compras_html = grafico_barrio_mas_compras.to_html(full_html=False)

    # Talla más vendida
    talla_mas_vendida = df['talla_camiseta'].value_counts().idxmax()
    grafico_talla_mas_vendida = px.pie(
        names=df['talla_camiseta'].value_counts().index,
        values=df['talla_camiseta'].value_counts().values,
        title='Distribución de ventas por talla'
    )
    grafico_talla_mas_vendida.update_traces(marker=dict(colors=['#007bff', '#28a745', '#dc3545']))  # Colores del pastel
    grafico_talla_mas_vendida.update_layout(
        font=dict(family="Arial", size=12, color="#333"),
        plot_bgcolor="#f8f9fa",
        paper_bgcolor="#fff",
        margin=dict(l=50, r=50, t=50, b=50)
    )
    grafico_talla_mas_vendida_html = grafico_talla_mas_vendida.to_html(full_html=False)

    # Crear el gráfico de violín
    grafico_violin = px.violin(
        df,
        x='marca',
        y='precio_camiseta',
        title='Distribución de precios por marca'
    )
    grafico_violin.update_traces(line_color='#333')  # Color de las líneas
    grafico_violin.update_layout(
        font=dict(family="Arial", size=12, color="#333"),
        plot_bgcolor="#f8f9fa",
        paper_bgcolor="#fff",
        margin=dict(l=50, r=50, t=50, b=50)
    )
    grafico_violin_html = grafico_violin.to_html(full_html=False)

    # Número de ventas por ciudad
    ventas_por_ciudad = df['ciudad'].value_counts().reset_index()
    ventas_por_ciudad.columns = ['ciudad', 'numero_ventas']

    # Crear el gráfico de barras
    grafico_ventas_por_ciudad = px.bar(
    ventas_por_ciudad,
    x='ciudad',
    y='numero_ventas',
    title='Número de Ventas por Ciudad',
    labels={'ciudad': 'Ciudad', 'numero_ventas': 'Número de Ventas'}
    )
    grafico_ventas_por_ciudad.update_traces(marker_color='#dc3545')  # Color de las barras
    grafico_ventas_por_ciudad.update_layout(
    font=dict(family="Arial", size=12, color="#333"),
    plot_bgcolor="#f8f9fa",
    paper_bgcolor="#fff",
    margin=dict(l=50, r=50, t=50, b=50)
    )
    grafico_ventas_por_ciudad_html = grafico_ventas_por_ciudad.to_html(full_html=False)

    # Contexto para pasar a la plantilla
    context = {
        "nombre": "andres",
        "camisetas": ventas,
        "grafica": grafico_html,
        "graficados": grafico_metodo_pago_html,
        "graficatres": grafico_marca_mas_vendida_html,
        "nombre_cliente_venta_mas_cara": nombre_cliente,
        "precio_venta_mas_cara": precio_venta,
        "graficacinco": grafico_barrio_mas_compras_html,
        "graficaseis": grafico_talla_mas_vendida_html,
        "graficasiete": grafico_violin_html,
        "graficaocho": grafico_ventas_por_ciudad_html,
    }

    return render(request, "inventario/index.html", context)
