from django.shortcuts import render

def saludar(request):
    context = {
        "nombre": "andres"
    }
    return render(request, "inventario/index.html", context)
# Create your views here.
