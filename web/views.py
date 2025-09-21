from django.shortcuts import render, get_object_or_404

from .models import Categoria, Producto

# Create your views here.
"""Vistar apra el catalago de productos"""
def index(request):
    listaProductos = Producto.objects.all()
    listaCategorias = Categoria.objects.all()
    context = {
        'productos': listaProductos,
        'categorias': listaCategorias
    }
    return render(request, 'index.html', context)

def productosPorCategoria(request, categoria_id):
    objCategoria = Categoria.objects.get(id=categoria_id)
    listaProductos = objCategoria.producto_set.all()

    listaCategorias = Categoria.objects.all()
    context = {
        'categorias': listaCategorias,
        'productos': listaProductos,
    }
    return render(request, 'index.html', context)

def productosPorNombre(request):
    """lista para filtrar producror pos nombre"""
    nombre = request.POST['nombre']

    listaProductos = Producto.objects.filter(nombre__contains=nombre)
    listaCategorias = Categoria.objects.all()
    context = {
        'categorias': listaCategorias,
        'productos': listaProductos,
    }
    return render(request, 'index.html', context)

def productoDetalle(request, producto_id):
    #vista para el detalle productos

    #objProducto = Producto.objects.get(pk=producto_id)
    objProducto = get_object_or_404(Producto, pk=producto_id)
    context= {
        'producto': objProducto,
    }
    return render(request, 'producto.html', context)