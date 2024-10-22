from django import forms
from .models import Auditoria


class AuditoriaAdminForm(forms.ModelForm):
    class Meta:
        model=Auditoria
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super(AuditoriaAdminForm,self).__init__(*args,**kwargs)
        self.fields['recursos'].required = False
