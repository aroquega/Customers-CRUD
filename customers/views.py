from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from . import models
from .models import TipoCliente,Zona,Cliente
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(req):
    return render(req,"customers/index.html")

def show_clientes(req):
    clientes = Cliente.objects.exclude(estado = "*").order_by('nombre')
    return render(req,"customers/clientes_show.html",{'clientes': clientes})

def new(req):
    if(req.method == "GET"):
        id=""
        nombre = ""
        ruc = ""
        tipo = None
        zona = None
        try:
            id = req.GET["id"]
            nombre = req.GET["nombre"]
            ruc = req.GET["ruc"]
            tipo = req.GET["tipo"]
            zona = req.GET["zona"]
            print(zona)
        except:
            print("Edición")
        tipos = TipoCliente.objects.all()
        zonas = Zona.objects.all()
        return render(req,"customers/create.html",{"zonas": zonas,"tipos": tipos, "nombre" : nombre, "ruc": ruc,"tipoget":tipo,"zonaget": zona,"id": id})
    elif (req.method == "POST"):
        tipo_id = req.POST["tipo_id"]
        zona_id = req.POST["zona_id"]
        id = req.POST["id"]
        if( id is ""):
            cliente = Cliente()
        else:
            cliente = Cliente.objects.get(pk=id)
        cliente.nombre = req.POST["nombre"]
        cliente.ruc = req.POST["ruc"]
        cliente.tipo = TipoCliente.objects.get(pk = tipo_id)
        cliente.zona = Zona.objects.get(pk = zona_id )
        cliente.save()
        return redirect(reverse("clientes"))

def del_cliente(req):
    if(req.method == "POST"):
        id = req.POST['id']
        cliente = Cliente.objects.get(pk = id)
        cliente.delete()
        return redirect(reverse("clientes"))

@csrf_exempt
def ajax_del_cliente(req):
    id = req.POST['id']
    cliente = Cliente.objects.get(pk = id)
    if(cliente is not None):
        cliente.delete()
        data = {
            'is_deleted': True
        }
    else:
        data = {
            'is_deleted': False
        }
    return JsonResponse(data)

def toogle_cliente(req):
    if(req.method=="POST"):
        id = req.POST['id']
        option = req.POST['option'] 
        cliente = Cliente.objects.get(pk = id)
        if(option == "ACTIVAR"):
            cliente.estado = 'A'
        elif(option == "INACTIVAR"):
            cliente.estado = "I"
        cliente.save()
        return redirect(reverse("clientes"))

def new_tipo(req):
    if(req.method == 'GET'):
        return render(req,"customers/create_tipo.html")
    elif (req.method == "POST"):
        name = req.POST['name']
        tipo = models.TipoCliente()
        tipo.nombre = name
        tipo.save()
        return redirect(reverse("index"))

def del_tipo(req):
    if(req.method == "POST"):
        id = req.POST['id']
        tipo = TipoCliente.objects.get(pk = id)
        tipo.delete()
        return redirect(reverse("tipos"))

def show_tipos(req):
    tipos = TipoCliente.objects.all()
    return render(req,"customers/tipos_show.html",{"tipos": tipos})

def toogle_zona(req):
    if(req.method=="POST"):
        id = req.POST['id']
        option = req.POST['option'] 
        zona = Zona.objects.get(pk = id)
        if(option == "ACTIVAR"):
            zona.estado = 'A'
        elif(option == "INACTIVAR"):
            zona.estado = "I"
        zona.save()
        return redirect(reverse("zonas"))

def new_zona(req):
    if(req.method == 'GET'):
        id = ""
        nombre = ""
        try:
            id = req.GET["id"]
            nombre = req.GET["nombre"]
        except:
            print(Edición)
        return render(req,"customers/create_zona.html",{"nombre" : nombre, "id" : id})
    elif (req.method == "POST"):
        id = req.POST["id"]
        if( id is ""):
            zona = Zona()
        else:
            zona = Zona.objects.get(pk=id)
        zona.nombre = req.POST["nombre"]
        zona.save()
        return redirect(reverse("zonas"))

def del_zona(req):
    if(req.method == "POST"):
        id = req.POST['id']
        zona = Zona.objects.get(pk = id)
        zona.delete()
        return redirect(reverse("zonas"))

def show_zonas(req):
    zonas = Zona.objects.all()
    return render(req,"customers/zonas_show.html",{"zonas": zonas})