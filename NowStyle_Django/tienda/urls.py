from django.urls import path
from . import views
urlpatterns=[
 path('',views.inicio,name='inicio'), path('catalogo/',views.catalogo,name='catalogo'), path('login/',views.login_page,name='login'), path('register/',views.registro_page,name='registro'), path('recuperar-password/',views.recuperar_page,name='recuperar'), path('panel/',views.panel,name='panel'), path('panel-empleado/',views.empleado,name='empleado'), path('gestion-usuarios/',views.usuarios_page,name='usuarios'), path('crear-producto/',views.crear_producto_page,name='crear_producto'), path('inventario/',views.inventario,name='inventario'), path('historial-pedidos/',views.reportes,name='reportes'), path('personalizar-estampado/',views.personalizar,name='personalizar'),
 path('api/productos/',views.productos_api),path('api/productos/<int:pk>/',views.producto_detalle_api),path('api/usuarios/',views.usuarios_api),path('api/usuarios/<int:pk>/',views.usuario_detalle_api),path('api/usuarios/login/',views.login_api),path('api/logout/',views.logout_api),path('api/pedidos/',views.pedidos_api),path('api/pedidos/<int:pk>/estado/',views.pedido_estado),path('api/pedidos/<int:pk>/mensajes/',views.mensajes_api),
]
