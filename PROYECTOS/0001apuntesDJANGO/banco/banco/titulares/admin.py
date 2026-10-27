from django import forms
from django.contrib import admin
from django.http import JsonResponse, HttpResponseForbidden
from django.urls import path, reverse

from geografica.models import Provincia, Departamento, Localidad

from .models import Titular, PersonaFisica, PersonaJuridica, Domicilio


@admin.register(Titular)
class TitularAdmin(admin.ModelAdmin):
    # Necesario para que Domicilio pueda usar autocomplete_fields = ['titular'].
    # Permite buscar por nombre, por DNI (persona fisica) o por CUIT (persona juridica).
    search_fields = ['nombre', 'personafisica__dni', 'personajuridica__cuit']

    def get_queryset(self, request):
        # Evita una consulta por fila al armar el texto "Apellido, Nombre (DNI ...)".
        return super().get_queryset(request).select_related('personafisica', 'personajuridica')


@admin.register(PersonaFisica)
class PersonaFisicaAdmin(admin.ModelAdmin):
    search_fields = ['nombre', 'apellido', 'dni']


@admin.register(PersonaJuridica)
class PersonaJuridicaAdmin(admin.ModelAdmin):
    search_fields = ['nombre', 'cuit']


class DomicilioAdminForm(forms.ModelForm):
    """Selects encadenados: Provincia -> Partido/Departamento -> Localidad.

    sel_provincia y sel_departamento no son campos del modelo: sirven solo para
    filtrar. Lo que se guarda es Domicilio.localidad.
    (No se llama "departamento" porque Domicilio ya tiene un campo
    "departamento" que es la unidad dentro del edificio.)
    """
    sel_provincia = forms.ModelChoiceField(
        queryset=Provincia.objects.all(),
        label='Provincia',
    )
    sel_departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.none(),
        label='Partido / departamento',
    )

    class Meta:
        model = Domicilio
        fields = '__all__'

    class Media:
        js = ('titulares/js/geo_cascada.js',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        provincia_id = departamento_id = None
        if self.is_bound:
            provincia_id = self.data.get(self.add_prefix('sel_provincia')) or None
            departamento_id = self.data.get(self.add_prefix('sel_departamento')) or None
        elif self.instance.pk and self.instance.localidad_id:
            depto = self.instance.localidad.localidad  # FK Localidad -> Departamento
            provincia_id, departamento_id = depto.provincia_id, depto.pk
            self.initial['sel_provincia'] = provincia_id
            self.initial['sel_departamento'] = departamento_id

        try:
            self.fields['sel_departamento'].queryset = (
                Departamento.objects.filter(provincia_id=int(provincia_id))
                if provincia_id else Departamento.objects.none())
            self.fields['localidad'].queryset = (
                Localidad.objects.filter(localidad_id=int(departamento_id))
                if departamento_id else Localidad.objects.none())
        except (TypeError, ValueError):
            self.fields['sel_departamento'].queryset = Departamento.objects.none()
            self.fields['localidad'].queryset = Localidad.objects.none()

        self.fields['localidad'].label = 'Localidad'
        self.fields['sel_provincia'].widget.attrs['data-url'] = reverse(
            'admin:titulares_domicilio_departamentos')
        self.fields['sel_departamento'].widget.attrs['data-url'] = reverse(
            'admin:titulares_domicilio_localidades')


@admin.register(Domicilio)
class DomicilioAdmin(admin.ModelAdmin):
    form = DomicilioAdminForm
    autocomplete_fields = ['titular']  # buscador por nombre / DNI / CUIT
    fields = ('titular', 'sel_provincia', 'sel_departamento', 'localidad',
              'calle', 'altura', 'piso', 'departamento')
    list_display = ('titular', 'calle', 'altura', 'localidad')

    def get_urls(self):
        extra = [
            path('departamentos/',
                 self.admin_site.admin_view(self.departamentos_json),
                 name='titulares_domicilio_departamentos'),
            path('localidades/',
                 self.admin_site.admin_view(self.localidades_json),
                 name='titulares_domicilio_localidades'),
        ]
        return extra + super().get_urls()

    def _json(self, request, queryset):
        if not self.has_view_or_change_permission(request):
            return HttpResponseForbidden()
        return JsonResponse({'items': [{'id': o.pk, 'nombre': o.nombre}
                                       for o in queryset.order_by('nombre')]})

    def departamentos_json(self, request):
        pid = request.GET.get('provincia', '')
        qs = Departamento.objects.filter(provincia_id=pid) if pid.isdigit() else Departamento.objects.none()
        return self._json(request, qs)

    def localidades_json(self, request):
        did = request.GET.get('departamento', '')
        qs = Localidad.objects.filter(localidad_id=did) if did.isdigit() else Localidad.objects.none()
        return self._json(request, qs)
