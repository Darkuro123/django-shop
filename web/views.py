from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .models import Categoria, Producto, Cliente
from .carrito import Cart
from .forms import ClienteForm


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

#geston vista clienes y usuarios
def crearUsuario(request):

    if request.method == "POST":
        dataUsuario = request.POST['nuevoUsuario']
        dataPassword = request.POST['nuevoPassword']

        nuevoUsuario = User.objects.create_user(username=dataUsuario,password=dataPassword)
        if nuevoUsuario is not None:
            login(request,nuevoUsuario)
            return redirect("/cuenta")


    return render(request,'login.html') 


def loginUsuario(request):
    paginaDestino = request.GET.get('next', None)

    context = {
        "destino": paginaDestino
    }

    if request.method == "POST":
        dataUsuario = request.POST['usuario']
        dataPassword = request.POST['password']
        dataDestino = request.POST['destino']

        usuarioAuth = authenticate(request, username=dataUsuario, password=dataPassword)
        if usuarioAuth is not None:
            login(request, usuarioAuth)
            if dataDestino != 'None':
                return redirect(dataDestino)
            return redirect("/cuenta")
        else:
            context ={ "mensajeError": "Usuario o contraseña incorrectos"}

    return render(request,'login.html', context)

def logoutUsuario(request):
    logout(request)
    return render(request,"login.html")

def cuentaUsuario(request):
    try:
        clienteEditar = Cliente.objects.get(usuario = request.user)

        dataCliente = {
            "nombre": request.user.first_name,
            "apellido": request.user.last_name,
            "email": request.user.email,
            "dni": clienteEditar.dni,
            "direccion": clienteEditar.direccion,
            "telefono": clienteEditar.telefono,
            "sexo": clienteEditar.sexo,
            "fecha_nacimiento": clienteEditar.fecha_nacimiento,
        }
    except(Exception):
        dataCliente = {
            "nombre": request.user.first_name,
            "apellido": request.user.last_name,
            "email": request.user.email,
        }

    frmCliente = ClienteForm(dataCliente)
    context = {
        'frmClient': frmCliente,
    }


    return render(request,'cuenta.html', context)

def actualizarCliente(request):

    mensaje = ""

    if request.method == "POST":
        frmCliente = ClienteForm(request.POST)
        if frmCliente.is_valid():
            dataCliente = frmCliente.cleaned_data

            ##actualizar usuario
            actUsuario = User.objects.get(pk=request.user.id)
            actUsuario.first_name = dataCliente['nombre']
            actUsuario.last_name = dataCliente['apellido']
            actUsuario.email = dataCliente['email']
            actUsuario.save()

            #registrar al cliente
            nuevoCliente = Cliente()
            nuevoCliente.usuario = actUsuario
            nuevoCliente.dni = dataCliente['dni']
            nuevoCliente.direccion = dataCliente['direccion']
            nuevoCliente.telefono = dataCliente['telefono']
            nuevoCliente.sexo = dataCliente['sexo']
            nuevoCliente.fecha_nacimiento = dataCliente['fecha_nacimiento']
            nuevoCliente.save()
            
            mensaje = "datos actualizado correctamente"

    context = {
        'mensaje': mensaje,
        'frmCliente': frmCliente,
    }
        
    return render(request, 'cuenta.html', context)

#vista para proceso de compra
@login_required(login_url='/login')
def regristrarPedido(request):
    try:
        clienteEditar = Cliente.objects.get(usuario = request.user)

        dataCliente = {
            "nombre": request.user.first_name,
            "apellido": request.user.last_name,
            "email": request.user.email,
            "dni": clienteEditar.dni,
            "direccion": clienteEditar.direccion,
            "telefono": clienteEditar.telefono,
            "sexo": clienteEditar.sexo,
            "fecha_nacimiento": clienteEditar.fecha_nacimiento,
        }
    except(Exception):
        dataCliente = {
            "nombre": request.user.first_name,
            "apellido": request.user.last_name,
            "email": request.user.email,
        }

    frmCliente = ClienteForm(dataCliente)
    context = {
        'frmClient': frmCliente,
    }   

    return render(request, 'pedido.html', context)