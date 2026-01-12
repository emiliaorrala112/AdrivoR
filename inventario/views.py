from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q 
from .models import Producto, Categoria
from .carrito import Carrito 
from .forms import RegistroForm

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST) 
        if form.is_valid():
            form.save()
            messages.success(request, "¡Cuenta creada con éxito! Por favor inicia sesión.")
            return redirect('login')
    else:
        form = RegistroForm() 
    return render(request, 'registro.html', {'form': form})

def tienda_home(request):
    query = request.GET.get('q') 
    categorias = Categoria.objects.prefetch_related('subcategorias__tipos').all()
    if query:
        productos = Producto.objects.filter(
            Q(nombre__icontains=query) |
            Q(tipo__nombre__icontains=query) |
            Q(tipo__subcategoria__nombre__icontains=query) |
            Q(tipo__subcategoria__categoria__nombre__icontains=query)
        ).distinct()
    else:
        productos = Producto.objects.all()
    context = {'productos': productos, 'categorias': categorias, 'query': query}
    return render(request, 'home.html', context)

# --- CARRITO ---

def agregar_carrito(request, producto_id):
    carrito = Carrito(request) 
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.agregar(producto=producto) 
    messages.success(request, f'¡{producto.nombre} añadido al carrito! 🛍️')
    return redirect('home')

def ver_carrito(request):
    carrito = Carrito(request)
    return render(request, 'carrito.html', {
        'items': carrito, 
        'total': carrito.get_total_price()
    })

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.restar(producto=producto)
    return redirect('carrito')

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = get_object_or_404(Producto, id=producto_id)
    carrito.eliminar(producto)
    return redirect('carrito')

def sumar_producto(request, producto_id):
    return agregar_carrito(request, producto_id)