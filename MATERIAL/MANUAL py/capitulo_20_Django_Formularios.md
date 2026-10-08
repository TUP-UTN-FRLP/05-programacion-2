# Capítulo 20. Django: Formularios

*Recibiendo datos del usuario.*

## ¿Por qué leemos este capítulo?

En el capítulo anterior armamos formularios HTML a mano. Funcionan, pero
tienen varios problemas:

- **Las validaciones viven en la vista**: cada vista repite chequeos (monto
  positivo, cuenta existente, saldo suficiente).
- **No hay feedback en el input**: si el monto es negativo, el usuario ve el
  mensaje de error, pero el formulario se vació.
- **Sin conversiones automáticas**: `request.POST.get('monto')` siempre
  devuelve string hay que convertir a float a mano y capturar errores si el
  valor no es numérico.
- **Duplicación**: los tres formularios (depositar, extraer, transferir)
  tienen HTML casi idéntico.

Django resuelve esto con dos clases: **Form** y **ModelForm**. Se declaran una
vez, se usan desde muchos lugares, y automatizan validación, conversión,
presentación y feedback.

Al final del capítulo, todas las operaciones bancarias van a estar detrás de
formularios Django profesionales. Es el último ladrillo antes de agregar
autenticación en el próximo capítulo.

## Un formulario Django

Un formulario en Django es una **clase** que declara sus campos como
atributos. Se parece mucho a un modelo, pero en vez de mapear a una tabla,
mapea a un formulario HTML.

Vamos con un ejemplo simple: un formulario para depositar en una cuenta. Creá
el archivo `banco/forms.py`:

**`banco/forms.py`**

```python
from django import forms


class DepositoForm(forms.Form):
    monto = forms.DecimalField(
        min_value=0.01,
        max_digits=15,
        decimal_places=2,
        label="Monto a depositar",
    )
    descripcion = forms.CharField(
        max_length=200,
        required=False,
        label="Descripción",
    )
```

Con eso ya tenés:

- **Dos campos declarados**: `monto` (decimal, mínimo 0.01) y `descripcion`
  (texto opcional).
- **Validación automática**: si el usuario ingresa "abc" en `monto`, o un
  número negativo, Django lo rechaza sin que escribas una línea.
- **Conversión automática**: si valida, `form.cleaned_data['monto']` es un
  `Decimal` de Python, no un string.
- **HTML generado**: Django puede renderizar el formulario como HTML
  automáticamente.

### Tipos de campos

Los más comunes:

| Campo | Uso |
|---|---|
| **CharField** | Texto corto |
| **DecimalField** | Números decimales exactos (dinero) |
| **IntegerField** | Enteros |
| **EmailField** | Emails (valida formato) |
| **BooleanField** | Checkbox |
| **DateField** | Fecha |
| **DateTimeField** | Fecha y hora |
| **ChoiceField** | Selección de opciones |
| **ModelChoiceField** | Selección de un objeto de un modelo |

Cada uno acepta parámetros comunes:

- `label`: la etiqueta que se muestra al usuario.
- `required`: si es obligatorio (`True` por defecto).
- `initial`: valor por defecto.
- `help_text`: ayuda debajo del campo.
- `min_value`, `max_value`, `min_length`, `max_length`: restricciones.
- `validators`: lista de funciones de validación adicionales.

## Usando un formulario en una vista

Un formulario tiene **dos estados**: **sin datos** (cuando se muestra por
primera vez) y **con datos enviados** (cuando el usuario presionó submit). El
patrón estándar de una vista es:

```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from banco.models import Cuenta
from banco.forms import DepositoForm


def depositar_en_cuenta(request, numero):
    cuenta = get_object_or_404(Cuenta, numero=numero)

    if request.method == 'POST':
        form = DepositoForm(request.POST)      # form con los datos enviados
        if form.is_valid():
            monto = form.cleaned_data['monto']
            descripcion = form.cleaned_data['descripcion']
            try:
                cuenta.depositar(monto, descripcion=descripcion or "Depósito web")
                messages.success(request, f"Depósito de ${monto} realizado")
                return redirect('banco:detalle_cuenta', numero=numero)
            except Exception as e:
                messages.error(request, f"Error: {e}")
    else:
        form = DepositoForm()                  # form vacío

    return render(request, 'banco/formulario_operacion.html', {
        'cuenta': cuenta,
        'form': form,
        'titulo': 'Depositar',
    })
```

Cinco pasos del patrón:

1. **Si es POST**: creamos el form pasándole `request.POST`. El form queda
   vinculado a esos datos.
2. **`form.is_valid()`**: dispara toda la validación de los campos. Devuelve
   `True` si todo está bien, `False` si hay errores.
3. **Si es válido**: los datos limpios están en `form.cleaned_data`
   (diccionario). Los usamos y redirigimos.
4. **Si no es válido** (o si es GET): renderizamos el template con el form. Si
   tenía errores, el form ya los tiene guardados y el template los va a
   mostrar.
5. **Si es GET**: creamos el form vacío para mostrarlo por primera vez.

Este patrón se repite en toda vista con formulario. Django lo llama el patrón
**"unbound / bound"** - form no vinculado (vacío) vs vinculado a datos.

## Renderizando un formulario

Django puede generar el HTML del formulario automáticamente. Actualizá
`banco/templates/banco/formulario_operacion.html`:

**`banco/templates/banco/formulario_operacion.html`**

```html
{% extends 'banco/base.html' %}


{% block titulo %}{{ titulo }}{% endblock %}


{% block contenido %}
    <h1>{{ titulo }}</h1>
    <p class="text-muted">Cuenta: {{ cuenta.numero }} - Saldo actual: ${{ cuenta.saldo|floatformat:2 }}</p>


    <form method="post" class="mt-4">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-primary">Confirmar</button>
        <a href="{% url 'banco:detalle_cuenta' cuenta.numero %}"
           class="btn btn-secondary">Cancelar</a>
    </form>
{% endblock %}
```

`{{ form.as_p }}` renderiza todos los campos del formulario como párrafos
`<p>`, con sus labels, inputs y mensajes de error si los hubiera. Con una
línea, Django genera el HTML completo.

Otras formas de renderizar:

- `{{ form.as_p }}` - cada campo en un `<p>`.
- `{{ form.as_table }}` - cada campo en una fila de tabla.
- `{{ form.as_ul }}` - cada campo en un `<li>`.

Estas son las formas rápidas, pero no dan mucho control sobre el estilo. Para
diseño más fino, se renderizan campos individualmente:

```html
<div class="mb-3">
    <label for="{{ form.monto.id_for_label }}" class="form-label">
        {{ form.monto.label }}
    </label>
    {{ form.monto }}
    {% if form.monto.errors %}
        <div class="text-danger">{{ form.monto.errors }}</div>
    {% endif %}
    {% if form.monto.help_text %}
        <div class="form-text">{{ form.monto.help_text }}</div>
    {% endif %}
</div>
```

Es verboso, pero permite integrar Bootstrap completamente. Django tiene
librerías como `django-crispy-forms` que hacen esto de forma automática, pero
eso queda para un curso más avanzado.

Para el manual, `{{ form.as_p }}` alcanza, el formulario funciona y se ve
razonable.

### Un template más lindo: renderizado manual

Como práctica de renderizado manual, vamos a mejorar el template para que se
vea mejor con Bootstrap:

**`banco/templates/banco/formulario_operacion.html`**

```html
{% extends 'banco/base.html' %}


{% block titulo %}{{ titulo }}{% endblock %}


{% block contenido %}
    <h1>{{ titulo }}</h1>
    <p class="text-muted">
        Cuenta: {{ cuenta.numero }} - Saldo actual: ${{ cuenta.saldo|floatformat:2 }}
    </p>


    <form method="post" class="mt-4" novalidate>
        {% csrf_token %}

        {% for field in form %}
            <div class="mb-3">
                <label for="{{ field.id_for_label }}" class="form-label">
                    {{ field.label }}
                </label>
                {{ field }}
                {% if field.errors %}
                    <div class="text-danger small">{{ field.errors|join:", " }}</div>
                {% endif %}
                {% if field.help_text %}
                    <div class="form-text">{{ field.help_text }}</div>
                {% endif %}
            </div>
        {% endfor %}

        <button type="submit" class="btn btn-primary">Confirmar</button>
        <a href="{% url 'banco:detalle_cuenta' cuenta.numero %}"
           class="btn btn-secondary">Cancelar</a>
    </form>
{% endblock %}
```

Iteramos sobre `form` (cada `field` es un campo). Para cada uno mostramos
label, input, errores y ayuda. **Un solo template sirve para cualquier
formulario del banco** - depósito, extracción, transferencia - porque el HTML
se genera dinámicamente según los campos del Form.

### Widgets: personalizando cómo se ve un input

Un problema visual: los inputs de Django, por defecto, no tienen la clase
`form-control` de Bootstrap. Para que se vean bien, hay que decirle a cada
campo qué clases CSS aplicar. Eso se hace con **widgets**:

**`banco/forms.py`**

```python
class DepositoForm(forms.Form):
    monto = forms.DecimalField(
        min_value=0.01,
        max_digits=15,
        decimal_places=2,
        label="Monto a depositar",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    descripcion = forms.CharField(
        max_length=200,
        required=False,
        label="Descripción",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
```

`widget` controla cómo se renderiza el input. Le pasamos `attrs` con las
clases CSS. Ahora los inputs se ven con estilo Bootstrap automáticamente.

En proyectos reales esto se hace de forma más elegante con un método
`__init__` que aplica clases a todos los campos, o directamente con
`django-crispy-forms`. Para el manual, la forma explícita con widgets es más
didáctica.

## Validación personalizada

Django valida automáticamente por tipo (que el monto sea decimal, que el email
tenga formato, etc.). Pero muchas veces querés reglas de negocio propias. Se
hace con **métodos `clean_<campo>()`** en el form.

Ejemplo: en una extracción, el monto tiene que ser **mayor a cero y menor o
igual al saldo disponible**.

**`banco/forms.py`**

```python
class ExtraccionForm(forms.Form):
    monto = forms.DecimalField(
        min_value=0.01,
        max_digits=15,
        decimal_places=2,
        label="Monto a extraer",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    descripcion = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, cuenta=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.cuenta = cuenta       # guardamos la cuenta para validar contra ella

    def clean_monto(self):
        monto = self.cleaned_data['monto']

        if self.cuenta is None:
            return monto           # sin cuenta no podemos validar contra saldo

        # Si es cuenta corriente, el disponible incluye el descubierto
        if hasattr(self.cuenta, 'cuentacorriente'):
            disponible = self.cuenta.saldo + self.cuenta.cuentacorriente.limite_descubierto
        else:
            disponible = self.cuenta.saldo

        if monto > disponible:
            raise forms.ValidationError(
                f"Monto excede el disponible (${disponible})"
            )

        return monto
```

Puntos clave:

- **`__init__` personalizado**: aceptamos un parámetro extra `cuenta` para
  poder validar contra ella. Django lo permite: recibimos `cuenta`, lo
  guardamos, y llamamos a `super().__init__(...)` para el resto.
- **`clean_monto`**: cualquier método que empiece con `clean_<nombre>` se
  ejecuta durante la validación. Recibe el valor ya validado por tipo, y
  podemos aplicar reglas adicionales.
- **`raise forms.ValidationError(...)`**: la forma de reportar un error.
  Django lo captura y lo asocia al campo `monto`.
- **`return monto`**: si todo está bien, hay que devolver el valor. Es una
  particularidad de los `clean_<campo>` - su retorno reemplaza el valor
  limpio.

Uso desde la vista:

```python
def extraer_de_cuenta(request, numero):
    cuenta = get_object_or_404(Cuenta, numero=numero)

    if request.method == 'POST':
        form = ExtraccionForm(request.POST, cuenta=cuenta)      # le pasamos la cuenta
        if form.is_valid():
            monto = form.cleaned_data['monto']
            descripcion = form.cleaned_data['descripcion']
            try:
                cuenta.extraer(monto, descripcion=descripcion or "Extracción web")
                messages.success(request, f"Extracción de ${monto} realizada")
                return redirect('banco:detalle_cuenta', numero=numero)
            except Exception as e:
                messages.error(request, f"Error: {e}")
    else:
        form = ExtraccionForm(cuenta=cuenta)

    return render(request, 'banco/formulario_operacion.html', {
        'cuenta': cuenta,
        'form': form,
        'titulo': 'Extraer',
    })
```

Ahora si el usuario intenta extraer más que su saldo, el error aparece
**debajo del campo `monto`**, en rojo, sin que la vista tenga que hacer nada
especial. **Toda la lógica de validación vive en el form.**

### Doble capa de validación

Fijate un detalle importante: **tenemos validación en el form Y en el
modelo**. El modelo `Cuenta.extraer()` lanza `ValidationError` si el monto
excede el saldo. El form también lo valida. **¿No es redundante?**

**No, es la práctica recomendada.** Ambas capas cumplen roles distintos:

- **El form valida antes de intentar la operación.** Da mejor UX: el error
  aparece asociado al campo específico, sin que el modelo se llegue a
  ejecutar.
- **El modelo valida siempre.** Es la última línea de defensa. Si alguien crea
  un objeto desde el shell, desde otro form, o desde una API, la validación
  del modelo protege la integridad.

> **Regla mental:** El form protege al usuario, el modelo protege al sistema.

## Validación cruzada: `clean()`

Cuando la validación involucra **varios campos**, no cabe en `clean_<campo>`.
Ahí se usa el método `clean()` general.

Ejemplo: en una transferencia, tenemos monto y cuenta destino. La cuenta
destino tiene que existir y ser distinta del origen.

```python
class TransferenciaForm(forms.Form):
    numero_destino = forms.CharField(
        max_length=20,
        label="Cuenta destino",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    monto = forms.DecimalField(
        min_value=0.01,
        max_digits=15,
        decimal_places=2,
        label="Monto",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    descripcion = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, cuenta_origen=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.cuenta_origen = cuenta_origen

    def clean_numero_destino(self):
        """Valida que la cuenta destino exista."""
        numero = self.cleaned_data['numero_destino'].strip()
        try:
            self.cuenta_destino = Cuenta.objects.get(numero=numero)
        except Cuenta.DoesNotExist:
            raise forms.ValidationError(f"La cuenta {numero} no existe")

        if self.cuenta_origen and self.cuenta_destino.numero == self.cuenta_origen.numero:
            raise forms.ValidationError("No podés transferir a la misma cuenta")

        return numero

    def clean(self):
        """Valida contra el saldo del origen (requiere que ambos campos sean válidos)."""
        cleaned = super().clean()
        monto = cleaned.get('monto')

        if self.cuenta_origen and monto:
            # Similar lógica que en Extracción
            if hasattr(self.cuenta_origen, 'cuentacorriente'):
                disponible = (self.cuenta_origen.saldo
                              + self.cuenta_origen.cuentacorriente.limite_descubierto)
            else:
                disponible = self.cuenta_origen.saldo

            if monto > disponible:
                raise forms.ValidationError(
                    f"El monto excede el disponible (${disponible})"
                )

        return cleaned
```

### Diferencia clave:

- `clean_<campo>` valida **un campo individual**. Si otro campo también tiene
  error, cada uno reporta el suyo.
- `clean()` valida **el formulario completo**. Se ejecuta después de que todos
  los campos individuales hayan sido validados. Los errores acá van al
  formulario en general, no a un campo específico (aunque también podés
  asociarlos a un campo con `self.add_error(campo, mensaje)`).

Los `clean_<campo>` en el ejemplo también guardan la cuenta destino en
`self.cuenta_destino`. Eso deja la vista todavía más limpia:

```python
def transferir_desde_cuenta(request, numero):
    origen = get_object_or_404(Cuenta, numero=numero)

    if request.method == 'POST':
        form = TransferenciaForm(request.POST, cuenta_origen=origen)
        if form.is_valid():
            destino = form.cuenta_destino     # ya cargada en el form
            monto = form.cleaned_data['monto']
            descripcion = form.cleaned_data['descripcion']
            try:
                origen.extraer(monto, descripcion=f"Transferencia a {destino.numero}")
                destino.depositar(monto, descripcion=f"Transferencia de {origen.numero}")
                messages.success(request, f"Transferencia de ${monto} realizada")
                return redirect('banco:detalle_cuenta', numero=numero)
            except Exception as e:
                messages.error(request, f"Error: {e}")
    else:
        form = TransferenciaForm(cuenta_origen=origen)

    return render(request, 'banco/formulario_operacion.html', {
        'cuenta': origen,
        'form': form,
        'titulo': 'Transferir',
    })
```

La vista queda **prácticamente igual** a las de depositar y extraer. Todo el
conocimiento específico de "transferencia" vive en `TransferenciaForm`. Es un
ejemplo del principio de responsabilidad única aplicado a la capa de
formularios.

## ModelForm: formularios a partir de modelos

Cuando el formulario **mapea directamente a un modelo** (para crear o editar
una instancia), Django ofrece un atajo aún mejor: **ModelForm**. En vez de
declarar cada campo, le decimos a Django *"tomá este modelo y generá el form
correspondiente"*.

Ejemplo: un formulario para dar de alta una persona física.

**`banco/forms.py`**

```python
from django import forms
from banco.models import PersonaFisica


class PersonaFisicaForm(forms.ModelForm):
    class Meta:
        model = PersonaFisica
        fields = ['nombre', 'apellido', 'dni', 'edad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'dni': 'DNI',
        }
```

Con la clase `Meta`, Django genera el form automáticamente:

- `model`: el modelo del que salen los campos.
- `fields`: qué campos incluir (podés poner `'__all__'` para todos, o listar
  los que quieras).
- `widgets`: personalización visual de cada campo.
- `labels`: etiquetas personalizadas.

Y la vista:

```python
from banco.forms import PersonaFisicaForm


def crear_persona(request):
    if request.method == 'POST':
        form = PersonaFisicaForm(request.POST)
        if form.is_valid():
            persona = form.save()                     # guarda automáticamente
            messages.success(request, f"Persona {persona} creada")
            return redirect('banco:listar_personas')
    else:
        form = PersonaFisicaForm()

    return render(request, 'banco/formulario_operacion.html', {
        'form': form,
        'titulo': 'Nueva persona física',
    })
```

`form.save()` **crea la instancia del modelo y la guarda en la base de
datos**. En una sola llamada.

Notá algo interesante: **las validaciones del modelo se ejecutan
automáticamente**. Si `PersonaFisica.dni` tiene `unique=True`, y el usuario
ingresa un DNI que ya existe, `form.is_valid()` devuelve `False` y el error
aparece asociado al campo `dni`. **Sin escribir una línea de código extra**.

Esto explica por qué el capítulo 15 valió la pena: las validaciones en
`clean()` del modelo se aprovechan automáticamente en cualquier form que
herede de `ModelForm`. **El diseño OO paga en Django**.

### Editar una instancia

Para editar en vez de crear, se le pasa una instancia al form:

```python
def editar_persona(request, persona_id):
    persona = get_object_or_404(PersonaFisica, id=persona_id)

    if request.method == 'POST':
        form = PersonaFisicaForm(request.POST, instance=persona)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos actualizados")
            return redirect('banco:detalle_persona', persona_id=persona.id)
    else:
        form = PersonaFisicaForm(instance=persona)

    return render(request, 'banco/formulario_operacion.html', {
        'form': form,
        'titulo': f'Editar {persona.nombre_completo()}',
    })
```

`instance=persona` **precarga el formulario con los datos actuales**. Cuando
el usuario guarda, Django actualiza el objeto existente en lugar de crear uno
nuevo. La misma vista, el mismo template, dos operaciones distintas.

### Alta de personas jurídicas

Mismo patrón:

**`banco/forms.py`**

```python
class PersonaJuridicaForm(forms.ModelForm):
    class Meta:
        model = PersonaJuridica
        fields = ['nombre', 'cuit']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cuit': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Razón social',
            'cuit': 'CUIT',
        }
```

**`banco/views.py`**

```python
def crear_persona_juridica(request):
    if request.method == 'POST':
        form = PersonaJuridicaForm(request.POST)
        if form.is_valid():
            empresa = form.save()
            messages.success(request, f"Empresa {empresa} creada")
            return redirect('banco:listar_personas')
    else:
        form = PersonaJuridicaForm()

    return render(request, 'banco/formulario_operacion.html', {
        'form': form,
        'titulo': 'Nueva persona jurídica',
    })
```

Un ModelForm por modelo, una vista por modelo. Todo el ABM del banco desde el
frontend termina siendo pocas líneas de código, todas con el mismo patrón.

## `ModelChoiceField`: seleccionar objetos relacionados

Un caso frecuente: en un formulario, un campo referencia un objeto de otro
modelo. Ejemplo: al abrir una cuenta, hay que seleccionar el titular.

Con ModelForm sobre `Cuenta`, Django genera esto automáticamente. Pero para
verlo en detalle, hagamos un form manual:

**`banco/forms.py`**

```python
class AperturaCuentaAhorroForm(forms.Form):
    titular = forms.ModelChoiceField(
        queryset=PersonaFisica.objects.all(),
        label="Titular",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    saldo_inicial = forms.DecimalField(
        min_value=0,
        max_digits=15,
        decimal_places=2,
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    tasa_interes_anual = forms.DecimalField(
        min_value=0,
        max_digits=5,
        decimal_places=2,
        initial=5,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
```

`ModelChoiceField` genera un `<select>` con las opciones del queryset. Cada
opción es un objeto del modelo, su representación textual es lo que devuelve
`__str__`.

Cuando `form.is_valid()` es `True`, `form.cleaned_data['titular']` es
directamente un **objeto `PersonaFisica`**, no un ID que hay que buscar
después. Django resuelve la conversión automáticamente.

## Formularios y modelos: cuándo cada uno

Regla práctica para decidir entre Form y ModelForm.

**Usá ModelForm cuando:**

- El formulario crea o edita instancias de un modelo directamente.
- Los campos del formulario corresponden a campos del modelo.

**Usá Form cuando:**

- El formulario recibe datos que no se guardan en un modelo (por ejemplo, un
  buscador).
- Los datos se procesan de forma custom (como nuestras operaciones bancarias:
  depositar y extraer no crean ni actualizan directamente, sino que ejecutan
  lógica).
- Necesitás campos que no corresponden a nada del modelo (por ejemplo, un
  campo "confirmación de contraseña").

Para el banco:

| Vista | Tipo de form | Motivo |
|---|---|---|
| **Alta de PersonaFisica** | ModelForm | Crear objeto directo |
| **Alta de CuentaAhorro** | ModelForm | Crear objeto directo |
| **Depositar** | Form | No crea nada, ejecuta `cuenta.depositar()` |
| **Extraer** | Form | Ídem depositar |
| **Transferir** | Form | Involucra dos objetos, no un create |

## Un cierre de formularios

Con todo lo visto, el patrón general para cualquier operación con formulario
en Django es:

```python
def mi_vista(request):
    if request.method == 'POST':
        form = MiForm(request.POST)          # bind con datos
        if form.is_valid():
            # usar form.cleaned_data
            # hacer la operación
            messages.success(request, "OK")
            return redirect(...)
    else:
        form = MiForm()                      # form vacío

    return render(request, 'template.html', {'form': form})
```

Este esqueleto se repite en cada vista con formulario. Con la práctica se
escribe automáticamente.

Y lo mejor: **cada formulario encapsula sus reglas**. Si mañana cambia una
validación (aumenta el mínimo de una operación, se restringe un tipo de
cuenta), se toca **el form**. Las vistas y templates quedan intactos.

## Buenas prácticas resumidas

1. **Un archivo `forms.py` por app.** Todos los forms juntos, importables desde
   donde se necesiten.
2. **Un form por operación conceptual.** No reutilices un mismo form para casos
   distintos si tienen validaciones diferentes.
3. **La validación de negocio vive en el form.** La vista solo coordina, no
   valida. **Los métodos del modelo siguen siendo el "sótano".** El form
   protege al usuario, el modelo protege al sistema. Ambos validan.
4. **ModelForm para CRUD sobre modelos, Form para operaciones lógicas.** No
   forzar ModelForm en casos donde no corresponde.
5. **Pasar contexto al form via `__init__`.** Cuando el form necesita datos
   externos (una cuenta, un usuario), pasarlos por constructor y guardarlos
   como atributos.
6. **Devolver el valor en `clean_<campo>`.** Es fácil olvidarse. Si no
   devolvés nada, `cleaned_data[campo]` queda en `None`.
