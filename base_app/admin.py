from django.contrib import admin
from .models import Roles,Recursos,Auditoria,AuditoriaRolesRecursos,Areas,Teams
from .forms import AuditoriaAdminForm

class AuditoriaAdmin(admin.ModelAdmin):
    form = AuditoriaAdminForm


admin.site.register(Roles)
admin.site.register(Recursos)
admin.site.register(AuditoriaRolesRecursos)
admin.site.register(Areas)
admin.site.register(Teams)
admin.site.register(Auditoria, AuditoriaAdmin)



# Create
# crear_rol = Roles.objects.create(nombre='')

# Bulk Create
# crear_roles = Roles.objects.bulk_create([
#     Roles(),
#     Roles(),
#     Roles(),
#     Roles(),
#     Roles(),
# ])

# Read

# roles = Roles.objects.all()
# rol = Roles.objects.get(id=1)
# filtrar_rol = Roles.objects.filter(id__gte=2)

# Update
# rol_update = Roles.objects.get(id=1).update(nombre='RolCambiado')

# Delete
# rol_delete = Roles.objects.get(id=1).delete()

# # CRUD DJANGO pero con SQL
# from django.db import connection

# # Insert
# with connection.cursor() as cursor:
#     cursor.execute("insert into roles (nombre) values (%s)",
#                    ['rol_insert'])
    
# #  Read
# roles = Roles.objects.raw("Select * from roles")
# with connection.cursor() as cursor:
#     cursor.execute("select * from roles")
#     roles = cursor.fetchall()
#     for rol in roles:
#         print(rol)

# # Update
# with connection.cursor() as cursor:
#     cursor.execute("update roles set nombre = %s where id = %s",['rol_update'])

# # Delete
# with connection.cursor() as cursor:
#     cursor.execute("delete from roles where id=%s",[2])