from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import GroupPermissionForm

@login_required
def manage_group_permissions(request):
    if request.method == 'POST':
        form = GroupPermissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_roles')
    else:
        form = GroupPermissionForm()

    return render(request,'manage_roles.html',context={'form':form})

    # if not request.user.is_superuser:
    #     return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

    # # Obtener el grupo seleccionado o el primero de la lista
    # group_id = request.GET.get('group', None)
    # if group_id:
    #     group = get_object_or_404(Group, id=group_id)
    # else:
    #     group = None

    # # Manejo de formulario para permisos del grupo
    # if request.method == 'POST' and group:
    #     form = GroupPermissionForm(request.POST, instance=group)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('manage_roles')  # Redirigir después de guardar
    # else:
    #     form = GroupPermissionForm(instance=group) if group else None

    # # Obtener los permisos ya asignados
    # assigned_permissions = group.permissions.all() if group else Permission.objects.none()

    # # Obtener los permisos no asignados de forma manual
    # all_permissions = Permission.objects.all()
    # assigned_permissions_ids = assigned_permissions.values_list('id', flat=True)
    # unassigned_permissions = all_permissions.exclude(id__in=assigned_permissions_ids)

    # groups = Group.objects.all()  # Listar todos los grupos
    # return render(request, 'manage_roles.html', {
    #     'groups': groups,
    #     'group': group,
    #     'form': form,
    #     'assigned_permissions': assigned_permissions,
    #     'unassigned_permissions': unassigned_permissions,
    # })
