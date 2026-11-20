import json, os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone
from .models import Producto, Usuario, Pedido, MensajePedido

def pagina(request, nombre='catalogo'):
    return render(request, f'tienda/{nombre}.html', {'productos': Producto.objects.all()[:100]})
def inicio(request): return pagina(request, 'inicio')
def catalogo(request): return pagina(request, 'catalogo')
def login_page(request): return pagina(request, 'login')
def registro_page(request): return pagina(request, 'registro')
def recuperar_page(request): return pagina(request, 'recuperar')
def panel(request): return pagina(request, 'panel')
def empleado(request): return pagina(request, 'empleado')
def usuarios_page(request): return pagina(request, 'usuarios')
def inventario(request): return pagina(request, 'inventario')
def crear_producto_page(request): return pagina(request, 'crear_producto')
def reportes(request): return pagina(request, 'reportes')
def personalizar(request): return pagina(request, 'personalizar')

def _json(request):
    try: return json.loads(request.body or '{}')
    except json.JSONDecodeError: return None
def _producto(p): return {'id':p.id,'nombre':p.nombre,'descripcion':p.descripcion,'categoria':p.categoria,'color':p.color,'precio':p.precio,'tallasStock':p.tallas_stock,'imagen':p.imagen}
@csrf_exempt
@require_http_methods(['GET','POST'])
def productos_api(request):
    if request.method=='GET': return JsonResponse([_producto(p) for p in Producto.objects.all()],safe=False)
    d=_json(request)
    if d is None: return HttpResponseBadRequest('JSON inválido')
    p=Producto.objects.create(nombre=d.get('nombre'),descripcion=d.get('descripcion'),categoria=d.get('categoria'),color=d.get('color'),precio=d.get('precio'),tallas_stock=d.get('tallasStock'),imagen=d.get('imagen'))
    return JsonResponse(_producto(p),status=201)
@csrf_exempt
@require_http_methods(['PUT','DELETE'])
def producto_detalle_api(request, pk):
    p=get_object_or_404(Producto,pk=pk)
    if request.method=='DELETE': p.delete(); return JsonResponse({'ok':True})
    d=_json(request) or {}
    for k,attr in [('nombre','nombre'),('descripcion','descripcion'),('categoria','categoria'),('color','color'),('precio','precio'),('tallasStock','tallas_stock'),('imagen','imagen')]:
        if k in d: setattr(p,attr,d[k])
    p.save(); return JsonResponse(_producto(p))
def _usuario(u): return {'id':u.id,'usuario':u.usuario,'email':u.email,'telefono':u.telefono,'rol':u.rol,'activo':u.activo,'foto':u.foto,'cuponPrimeraCompra':u.cupon_primera_compra}
@csrf_exempt
@csrf_exempt
@require_http_methods(['GET','POST'])
def usuarios_api(request):
    if request.method=='GET': return JsonResponse([_usuario(u) for u in Usuario.objects.all()],safe=False)
    d=_json(request) or {}; email=(d.get('email') or '').strip().lower()
    if not d.get('usuario') or len(d['usuario'])<4 or not email.endswith('@gmail.com') or len(d.get('password',''))<8: return JsonResponse({'error':'Verifica usuario, correo Gmail y contraseña (mínimo 8 caracteres).'},status=400)
    if Usuario.objects.filter(email=email).exists(): return JsonResponse({'error':'El correo ya está registrado.'},status=409)
    u=Usuario.objects.create(usuario=d['usuario'],email=email,telefono=d.get('telefono',''),password=d['password'],rol='CLIENTE',activo=True,foto=d.get('foto'),cupon_primera_compra=False)
    return JsonResponse(_usuario(u),status=201)
@csrf_exempt
@require_http_methods(['POST'])
def login_api(request):
    d=_json(request) or {}; ident=d.get('email','')
    u=Usuario.objects.filter(email=ident).first() or Usuario.objects.filter(usuario=ident).first()
    if not u or u.password != d.get('password'): return JsonResponse({'error':'Credenciales incorrectas.'},status=401)
    if u.activo is False: return JsonResponse({'error':'Tu cuenta está inactiva.'},status=403)
    request.session['usuario_id']=u.id; request.session['usuario_email']=u.email; request.session['rol']=u.rol
    return JsonResponse(_usuario(u))
def logout_api(request): request.session.flush(); return JsonResponse({'ok':True})

@csrf_exempt
@require_http_methods(['PUT','PATCH','DELETE'])
def usuario_detalle_api(request,pk):
    u=get_object_or_404(Usuario,pk=pk)
    if request.method=='DELETE': u.delete(); return JsonResponse({'ok':True})
    d=_json(request) or {}
    for key,attr in [('usuario','usuario'),('telefono','telefono'),('foto','foto'),('activo','activo'),('rol','rol')]:
        if key in d: setattr(u,attr,d[key])
    if d.get('password'): u.password=d['password']
    u.save(); return JsonResponse(_usuario(u))

@csrf_exempt
@require_http_methods(['PATCH'])
def pedido_estado(request,pk):
    p=get_object_or_404(Pedido,pk=pk); d=_json(request) or {}; estado=d.get('estado')
    if not estado: return JsonResponse({'error':'El estado es obligatorio'},status=400)
    p.estado=estado.upper(); p.save(update_fields=['estado']); return JsonResponse({'id':p.id,'estado':p.estado})
@csrf_exempt
def pedidos_api(request):
    qs=Pedido.objects.prefetch_related('items').order_by('-fecha')
    email=request.GET.get('email')
    if email: qs=qs.filter(usuario_email=email)
    result=[]
    for p in qs:
        result.append({'id':p.id,'usuarioEmail':p.usuario_email,'direccionEnvio':p.direccion_envio,'ciudadEnvio':p.ciudad_envio,'subtotal':p.subtotal,'descuento':p.descuento,'costoEnvio':p.costo_envio,'total':p.total,'estado':p.estado,'fecha':p.fecha,'items':[{'id':i.id,'productoId':i.producto_id,'nombre':i.nombre,'cantidad':i.cantidad,'talla':i.talla,'precioUnitario':i.precio_unitario,'modelo3d':i.modelo3d,'colorHex':i.color_hex,'categoria':i.categoria,'imagen':i.imagen,'personalizacion':i.personalizacion} for i in p.items.all()]})
    return JsonResponse(result,safe=False)
@csrf_exempt
def mensajes_api(request,pk):
    if request.method=='GET':
        return JsonResponse(list(MensajePedido.objects.filter(pedido_id=pk).order_by('fecha').values()),safe=False)
    if request.method=='POST':
        d=_json(request) or {}; msg=(d.get('mensaje') or '').strip(); img=d.get('imagen')
        if not msg and not img: return JsonResponse({'error':'El mensaje no puede estar vacío'},status=400)
        m=MensajePedido.objects.create(pedido_id=pk,autor_email=d.get('autorEmail',''),rol_autor=d.get('rolAutor','CLIENTE'),mensaje=msg or None,imagen=img,fecha=timezone.now())
        return JsonResponse({'id':m.id,'pedidoId':m.pedido_id,'mensaje':m.mensaje,'imagen':m.imagen,'fecha':m.fecha},status=201)
    return JsonResponse({'error':'Método no permitido'},status=405)
