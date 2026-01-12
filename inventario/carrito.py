from decimal import Decimal
from django.conf import settings
from .models import Producto

class Carrito:
    def __init__(self, request):
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            # Si no hay carrito, creamos uno vacío en la sesión
            carrito = self.session["carrito"] = {}
        self.carrito = carrito

    def agregar(self, producto):
        id = str(producto.id)
        if id not in self.carrito:
            self.carrito[id] = {
                "producto_id": producto.id,
                "nombre": producto.nombre,
                "precio": str(producto.precio),
                "cantidad": 0,
                "imagen": producto.imagen.url if producto.imagen else ""
            }
        
        # Aquí sumamos 1 a la cantidad
        self.carrito[id]["cantidad"] += 1
        self.guardar()

    def restar(self, producto):
        id = str(producto.id)
        if id in self.carrito:
            self.carrito[id]["cantidad"] -= 1
            # Si llega a 0, lo eliminamos
            if self.carrito[id]["cantidad"] <= 0:
                self.eliminar(producto)
            self.guardar()

    def eliminar(self, producto):
        id = str(producto.id)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar()

    def guardar(self):
        self.session.modified = True

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True

    def __iter__(self):
        """
        Este método es mágico: permite recorrer los productos en el HTML
        y traer los datos frescos de la base de datos.
        """
        ids_productos = self.carrito.keys()
        # Traemos los productos reales de la base de datos
        productos = Producto.objects.filter(id__in=ids_productos)
        carrito_copia = self.carrito.copy()

        for producto in productos:
            carrito_copia[str(producto.id)]["producto"] = producto

        for item in carrito_copia.values():
            item["precio"] = Decimal(item["precio"])
            item["subtotal"] = item["precio"] * item["cantidad"]
            yield item

    def __len__(self):
        # Cuenta cuántos productos hay en total
        return sum(item["cantidad"] for item in self.carrito.values())

    def get_total_price(self):
        # Calcula el precio total de todo el carrito
        return sum(Decimal(item["precio"]) * item["cantidad"] for item in self.carrito.values())