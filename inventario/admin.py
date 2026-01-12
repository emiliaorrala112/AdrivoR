from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, SubCategoria, TipoProducto, Producto, MovimientoStock

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'mostrar_stock', 'tipo', 'ver_imagen')
    list_filter = ('tipo',)
    search_fields = ('nombre',)
    def mostrar_stock(self, obj):
        if obj.stock <= 0:
            color = "red"
            mensaje = "AGOTADO 🚫"
        elif obj.stock <= obj.stock_minimo:
            color = "orange"
            mensaje = f"{obj.stock} (Bajo) ⚠️"
        else:
            color = "green"
            mensaje = f"{obj.stock} (OK) ✅"
            
        return format_html(
            '<b style="color:{}; font-size:1.1em;">{}</b>', 
            color, mensaje
        )
    mostrar_stock.short_description = "Estado del Stock"

class MovimientoStockAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'tipo_color', 'producto', 'cantidad', 'motivo')
    list_filter = ('tipo', 'fecha')
    search_fields = ('producto__nombre',)
    
    def tipo_color(self, obj):
        if obj.tipo == 'entrada':
            return format_html('<span style="color:green;">⬇ INGRESO</span>')
        return format_html('<span style="color:red;">⬆ SALIDA</span>')
    tipo_color.short_description = "Tipo"

admin.site.register(Categoria)
admin.site.register(SubCategoria)
admin.site.register(TipoProducto)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(MovimientoStock, MovimientoStockAdmin)