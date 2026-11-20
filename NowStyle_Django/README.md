# NowStyle migrado a Django

Esta es una primera migración funcional del backend Spring Boot a Django y de las rutas React a páginas HTML renderizadas por Django. Se conservan los CSS originales, las imágenes y los tres modelos 3D GLB.

## Requisitos
- Python 3.10+
- MySQL 8 (base de datos existente `db_modulo_productos`)
- Node.js ya no es necesario para ejecutar esta versión.

## Instalación en Windows
1. Descomprime el ZIP.
2. Abre una terminal dentro de `NowStyle_Django`.
3. Crea entorno: `py -m venv venv` y actívalo con `venv\Scripts\activate`.
4. Instala: `pip install -r requirements.txt`.
5. Copia `.env.example` a `.env` y completa usuario/contraseña de MySQL.
6. Ejecuta `python manage.py check`.
7. Ejecuta `python manage.py runserver`.
8. Abre `http://127.0.0.1:8000/`.

## Base de datos
Los modelos de `tienda/models.py` usan `managed=False` y apuntan a las tablas existentes `productos`, `usuarios`, `pedidos`, `detalle_pedidos` y `mensajes_pedido`. Django no debe crear ni modificar esas tablas. No se incluyó un dump SQL en el ZIP original, por lo que se mantiene la conexión a `db_modulo_productos`; no se puede verificar desde aquí que tu servidor MySQL tenga exactamente esas columnas. Haz una copia de seguridad antes de probar.

## Rutas convertidas
`/`, `/catalogo/`, `/personalizar-estampado/`, `/historial-pedidos/`, `/login/`, `/register/`, `/recuperar-password/`, `/panel/`, `/panel-empleado/`, `/gestion-usuarios/`, `/crear-producto/`, `/inventario/`.

## APIs Django
- `GET/POST /api/productos/`
- `PUT/DELETE /api/productos/<id>/`
- `GET/POST /api/usuarios/`
- `POST /api/usuarios/login/`
- `GET /api/pedidos/` (opcional `?email=...`)
- `PATCH /api/pedidos/<id>/estado/`
- `GET/POST /api/pedidos/<id>/mensajes/`

## Funcionalidades pendientes de migración completa
El código fuente React contiene pantallas extensas con lógica propia. Esta primera entrega crea equivalentes navegables y funcionalidad base de catálogo, productos, registro/login, listados y visor GLB. Aún requieren migración detallada el editor avanzado de estampados y guardado de diseños, reglas completas de roles/permisos, flujo de pedidos/carrito, recuperación y verificación de correo, reportes exportables y la integración de checkout Mercado Pago. El endpoint de pago Java no se tradujo de forma segura sin validar credenciales y payloads del entorno.

## Seguridad importante
El backend Java original compara contraseñas como texto plano. Esta migración conserva compatibilidad de lectura para poder autenticar cuentas existentes, pero esto no es seguro para producción. Antes de publicar el sistema hay que migrar contraseñas a hash con un proceso controlado y no exponer endpoints de administración sin autenticación/autorización. Configura `DJANGO_DEBUG=False` y una `DJANGO_SECRET_KEY` privada en producción.
