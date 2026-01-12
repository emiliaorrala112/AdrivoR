from django.db import models
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError

# ==========================================
# 1. JERARQUÍA DE CATEGORÍAS (Padres)
# ==========================================

# NIVEL 1: CATEGORÍA GIGANTE
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="1. Categoría Principal")
    def __str__(self): return self.nombre
    class Meta: verbose_name_plural = "1. Categorías Principales"

# NIVEL 2: SUBCATEGORÍA
class SubCategoria(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='subcategorias')
    nombre = models.CharField(max_length=100, verbose_name="2. Subcategoría")
    def __str__(self): return f"{self.categoria.nombre} > {self.nombre}"
    class Meta: verbose_name_plural = "2. Subcategorías"

# NIVEL 3: TIPO DE PRODUCTO
class TipoProducto(models.Model):
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE, related_name='tipos')
    nombre = models.CharField(max_length=100, verbose_name="3. Tipo de Producto")
    def __str__(self): return f"{self.subcategoria.nombre} > {self.nombre}"
    class Meta: verbose_name_plural = "3. Tipos"


# ==========================================
# 2. PRODUCTO Y STOCK (Hijos)
# ==========================================

class Producto(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    tipo = models.ForeignKey(TipoProducto, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tipo")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio ($)")
    
    # CONTROL DE STOCK
    stock = models.IntegerField(default=0, verbose_name="Stock Actual")
    stock_minimo = models.IntegerField(default=5, verbose_name="Alerta de Stock Bajo")
    
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True, verbose_name="Foto")
    
    def ver_imagen(self):
        if self.imagen: return mark_safe(f'<img src="{self.imagen.url}" width="50" style="border-radius:5px;"/>')
        return "No img"
    ver_imagen.short_description = "Vista Previa"
    
    def __str__(self): return self.nombre
    class Meta: verbose_name_plural = "🛍️ Productos"


class MovimientoStock(models.Model):
    TIPO_CHOICES = [
        ('entrada', '📥 Entrada (Compra/Devolución)'),
        ('salida', '📤 Salida (Venta/Pérdida)'),
    ]
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Producto")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name="Tipo de Movimiento")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")
    motivo = models.CharField(max_length=200, blank=True, verbose_name="Motivo (Opcional)")

    def save(self, *args, **kwargs):
        if self.pk is None: 
            if self.tipo == 'entrada':
                self.producto.stock += self.cantidad
            else: 
                if self.producto.stock < self.cantidad:
                    raise ValidationError(f"No hay suficiente stock. Tienes {self.producto.stock} y quieres sacar {self.cantidad}.")
                self.producto.stock -= self.cantidad
            
            self.producto.save() 
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo} de {self.cantidad} - {self.producto.nombre}"

    class Meta:
        verbose_name = "Historial de Inventario"
        verbose_name_plural = "📊 Control de Stock (Entradas/Salidas)"