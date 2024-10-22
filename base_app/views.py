from django.shortcuts import render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden, JsonResponse
from .models import Auditoria, Recursos, Roles, AuditoriaRolesRecursos, Recursos, Areas
# from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
# def is_analyst(user):
#     return user.groups.filter(name='analista').exists()

# Vista protegida solo para usuarios del grupo 'Analista'


def index(request):
    return render(request,'layout.html')

#@login_required
def administrador(request):
    return render(request,'administrador.html')
    # if request.user.groups.filter(name='administrador').exists():
    #     is_admin = request.user.groups.filter(name='administrador').exists()
    #     return render(request,'administrador.html',{'is_admin':is_admin})
    # else:
    #     return HttpResponseForbidden('No tiene permiso para acceder a esta pestaña')
    
def activos(request):
    return render(request,'activos.html')

def actividades(request):
    return render(request,'actividades.html')

def areas(request):
    return render(request,'areas.html')

def calendario(request):
    return render(request,'calendario.html')

def configuracion(request):
    return render(request,'configuracion.html')

def conocimiento_base(request):
    return render(request,'conocimiento_base.html')

def diagramas(request):
    return render(request,'diagramas.html')

def objetivos_de_control(request):
    return render(request,'objetivos_de_control.html')

def pruebas(request):
    return render(request,'pruebas.html')

def planificacion(request):
    return render(request,'planificacion.html')



def auditoria_view(request):
    auditorias = Auditoria.objects.all()
    roles = Roles.objects.all()
    areas = Areas.objects.all()

    asignaciones = AuditoriaRolesRecursos.objects.all()

    context = {
        'auditorias': auditorias,
        'roles': roles,
        'areas': areas,
        'asignaciones': asignaciones,
    }
    
    return render(request, 'auditoria_view.html', context)

def sortabblejs(request):
    # Obtener todas las auditorías, roles y áreas
    auditorias = Auditoria.objects.all()
    roles = Roles.objects.all()
    areas = Areas.objects.prefetch_related('team__recursos').all()

    # Obtener todas las asignaciones y hacer un prefetch para obtener recursos y roles
    asignaciones = AuditoriaRolesRecursos.objects.select_related('auditoria', 'recurso', 'rol')

    auditoria_dict = {}
    for asignacion in asignaciones:
        auditoria_nombre = asignacion.auditoria.nombre
        rol_nombre = asignacion.rol.nombre
        recurso_nombre = asignacion.recurso.nombre
        auditoria_id = asignacion.auditoria.id
        rol_id = asignacion.rol.id
        recurso_id = asignacion.recurso.id


        # Si la auditoría no está en el diccionario, la creamos
        if auditoria_nombre not in auditoria_dict:
            auditoria_dict[auditoria_nombre] = {
                'id': str(auditoria_id), 
                'roles': {}
            }

        # Si el rol no está en la auditoría, lo añadimos
        if rol_nombre not in auditoria_dict[auditoria_nombre]['roles']:
            auditoria_dict[auditoria_nombre]['roles'][rol_nombre] = {
                'id': str(rol_id), 
                'recursos': []
            }

        # Añadimos el recurso con su nombre e id
        auditoria_dict[auditoria_nombre]['roles'][rol_nombre]['recursos'].append({
            'nombre': recurso_nombre,
            'id': str(recurso_id)
        })


    print('\n\n')
    print(auditoria_dict)
    print('\n\n')
    
    context = {
        'auditorias': auditorias,
        'roles': roles,
        'areas': areas,
        'asignaciones': auditoria_dict,  # Cambia a la nueva estructura
    }

    return render(request, 'sortablejs.html', context)

# Crear auditoria y asignar recursos y roles respectivamente
def asignar_recurso_auditoria(request):
    if request.method == 'POST':
        auditoria_id = request.POST.get('auditoria')
        recurso_id = request.POST.get('recurso')
        rol_id = request.POST.get('rol')

        if not (auditoria_id and recurso_id and rol_id):
            return JsonResponse({'status': 'error', 'message': 'Faltan datos'}, status=400)

        try:
            auditoria = Auditoria.objects.get(id=auditoria_id)
            recurso = Recursos.objects.get(id=recurso_id)
            rol = Roles.objects.get(id=rol_id)

            # Crear o actualizar la relación AuditoriaRolesRecursos
            asignacion, created = AuditoriaRolesRecursos.objects.update_or_create(
                auditoria=auditoria,
                recurso=recurso,
                defaults={'rol': rol},
            )
            return JsonResponse({'status': 'success', 'created': created})

        # Si alguno de los elementos no existe que tire excepción
        except (Auditoria.DoesNotExist, Recursos.DoesNotExist, Roles.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Datos inválidos'}, status=400)
        # Cualquier otra excepción que la capture y retorne un mensaje
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    # Si no es ninguno de los anteriores es porque no tiene permisos para ejecutar
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

# Que las auditorías creadas previamente, puedan guardar sus datos.
def reasignar_recurso_auditoria(request):
    if request.method == 'POST':
        auditoria_id = request.POST.get('auditoria')
        recurso_id = request.POST.get('recurso') 
        rol_id = request.POST.get('rol')

        if not (auditoria_id and recurso_id and rol_id):
            return JsonResponse({'status':'error','message':'Faltan datos'}, status=400)
        
        try:
            auditoria = Auditoria.objects.get(id=auditoria_id)
            recurso = Recursos.objects.get(id=recurso_id)
            rol = Roles.objects.get(id=rol_id)

            asignacion,created = AuditoriaRolesRecursos.objects.update_or_create(
                auditoria = auditoria,
                recurso = recurso,
                defaults = {'rol' : rol}
            )
            return JsonResponse({'status': 'success', 'created': created})

        # Si alguno de los elementos no existe que tire excepción
        except (Auditoria.DoesNotExist, Recursos.DoesNotExist, Roles.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Datos inválidos'}, status=400)
        # Cualquier otra excepción que la capture y retorne un mensaje
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    # Si no es ninguno de los anteriores es porque no tiene permisos para ejecutar
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)
