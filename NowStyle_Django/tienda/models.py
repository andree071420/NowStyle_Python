from django.db import models

# Modelos vinculados a las tablas creadas por Hibernate en db_modulo_productos.
# managed=False evita que Django altere o recree las tablas existentes.
class Producto(models.Model):
    nombre=models.CharField(max_length=255, null=True, blank=True)
    descripcion=models.CharField(max_length=500, null=True, blank=True)
    categoria=models.CharField(max_length=255, null=True, blank=True)
    color=models.CharField(max_length=255, null=True, blank=True)
    precio=models.FloatField(null=True, blank=True)
    tallas_stock=models.TextField(db_column='tallas_stock', null=True, blank=True)
    imagen=models.TextField(null=True, blank=True)
    class Meta: managed=False; db_table='productos'

class Usuario(models.Model):
    usuario=models.CharField(max_length=255, null=True, blank=True)
    email=models.CharField(max_length=255, null=True, blank=True)
    telefono=models.CharField(max_length=255, null=True, blank=True)
    password=models.CharField(max_length=255, null=True, blank=True)
    cupon_primera_compra=models.BooleanField(default=False, null=True, blank=True)
    rol=models.CharField(max_length=255, default='CLIENTE', null=True, blank=True)
    activo=models.BooleanField(default=True, null=True, blank=True)
    foto=models.TextField(null=True, blank=True)
    class Meta: managed=False; db_table='usuarios'

class Pedido(models.Model):
    usuario_email=models.CharField(max_length=255, null=True, blank=True)
    direccion_envio=models.CharField(max_length=255, null=True, blank=True)
    ciudad_envio=models.CharField(max_length=255, null=True, blank=True)
    subtotal=models.FloatField(null=True, blank=True); descuento=models.FloatField(null=True, blank=True)
    costo_envio=models.FloatField(null=True, blank=True); total=models.FloatField(null=True, blank=True)
    estado=models.CharField(max_length=255, default='PENDIENTE', null=True, blank=True)
    mercado_pago_id=models.CharField(max_length=255, null=True, blank=True)
    fecha=models.DateTimeField(null=True, blank=True)
    class Meta: managed=False; db_table='pedidos'

class DetallePedido(models.Model):
    pedido=models.ForeignKey(Pedido, db_column='pedido_id', on_delete=models.DO_NOTHING, related_name='items')
    producto_id=models.BigIntegerField(null=True, blank=True); nombre=models.CharField(max_length=255, null=True, blank=True)
    cantidad=models.IntegerField(null=True, blank=True); talla=models.CharField(max_length=255, null=True, blank=True)
    precio_unitario=models.FloatField(null=True, blank=True); modelo3d=models.CharField(max_length=255, null=True, blank=True)
    color_hex=models.CharField(max_length=255, null=True, blank=True); categoria=models.CharField(max_length=255, null=True, blank=True)
    imagen=models.TextField(null=True, blank=True); personalizacion=models.TextField(null=True, blank=True)
    class Meta: managed=False; db_table='detalle_pedidos'

class MensajePedido(models.Model):
    pedido_id=models.BigIntegerField(null=True, blank=True); autor_email=models.CharField(max_length=255, null=True, blank=True)
    rol_autor=models.CharField(max_length=255, null=True, blank=True); mensaje=models.TextField(null=True, blank=True)
    imagen=models.TextField(null=True, blank=True); fecha=models.DateTimeField(null=True, blank=True)
    class Meta: managed=False; db_table='mensajes_pedido'
