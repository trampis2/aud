from django.db import models

    
class Recursos(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

class Roles(models.Model):
    nombre = models.CharField(max_length=100)
    # Otros campos del rol
    def __str__(self):
        return self.nombre

class Auditoria(models.Model):
    nombre = models.CharField(max_length=100)
    
    # charlar si se saca este campo (redundancia de datos)
    recursos = models.ManyToManyField('Recursos', related_name='auditorias')

    def __str__(self):    
        return self.nombre
    
class AuditoriaRolesRecursos(models.Model):
    auditoria = models.ForeignKey('Auditoria', on_delete=models.CASCADE)
    recurso = models.ForeignKey('Recursos', on_delete=models.CASCADE)
    rol = models.ForeignKey('Roles', on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.auditoria
    
    class Meta:
        unique_together = ('auditoria', 'recurso')  # Un empleado puede tener un solo rol por auditoría

class Areas(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)
    team = models.ManyToManyField('Teams', related_name='area')

    def __str__(self):
        return self.nombre
    
class Teams(models.Model):
    nombre_team = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)
    recursos = models.ManyToManyField('Recursos',related_name='teams')
    # en principio no se va a usar
    integrantes = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_team
    