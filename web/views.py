from django.shortcuts import render, get_object_or_404, redirect

from .models import Categoria, Producto
from .carrito import Cart


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

#vistar para el carrito de compras

def carrito(request):
    return render(request, 'carrito.html')


def agregarCarrito(request, producto_id):
    if request.method == 'POST':
        cantidad = request.POST['cantidad']
    else:
        cantidad = 1
    
    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.add(objProducto, cantidad)

    # print(request.session.get("cart"))
    if request.method == "GET":
        return redirect("/")

    return render(request, 'carrito.html')

def eliminarProductoCarrito(request, producto_id):
    objprocuto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.delete(objprocuto)

    return render(request, 'carrito.html')

def limpiarCarrito(request):
    carritoProducto = Cart(request)
    carritoProducto.clear()

    return render(request, 'carrito.html')