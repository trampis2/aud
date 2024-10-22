# custom_forms.py
from django import forms
from django.contrib.auth.models import Group, Permission

class GroupPermissionForm(forms.ModelForm):
    permissions = forms.ModelChoiceField(
        queryset = Permission.objects.all(),
        widget = forms.SelectMultiple,
        required = False,
        label = 'permisos'
    )















    # permissions = forms.ModelMultipleChoiceField(
    #     queryset=Permission.objects.all(),
    #     widget=forms.SelectMultiple,
    #     required=False,
    #     label="Permisos Disponibles",
    #     help_text="Selecciona los permisos que quieres asignar a este rol."
    # )

    # class Meta:
    #     model = Group
    #     fields = ['name', 'permissions']

    # def __init__(self, *args, **kwargs):
    #     super(GroupPermissionForm, self).__init__(*args, **kwargs)
    #     if self.instance:
    #         self.fields['permissions'].initial = self.instance.permissions.all()

    # # def save(self, *args, **kwargs):
    # #     group = super(GroupPermissionForm, self).save(commit=False)
    # #     group.save()
    # #     group.permissions.set(self.cleaned_data['permissions'])
    # #     return group
