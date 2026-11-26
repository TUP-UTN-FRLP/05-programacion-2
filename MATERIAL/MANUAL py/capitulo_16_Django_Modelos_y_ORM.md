# Capítulo 16. Django: Modelos y ORM

*Persistiendo objetos como si nada.*

## ¿Por qué leemos este capítulo?

Durante todo el proyecto bancario, tuvimos un problema que fuimos postergando:
cuando el programa termina, todo se pierde. Las cuentas que abrimos, los
movimientos que registramos, los clientes que creamos - todo vive en memoria,
y al cerrar Python desaparece.

Para que la información persista entre ejecuciones, hay que guardarla en algún
lugar externo: un archivo, una base de datos, un servicio de almacenamiento.
En este capítulo vamos a ver cómo Django resuelve este problema con una
elegancia notable: haciendo que los objetos Python se conviertan
automáticamente en filas de una base de datos.

Esto se logra con un ORM (Object-Relational Mapper): una herramienta que
traduce entre dos mundos distintos, el de los objetos (Python) y el de las
tablas relacionales (SQL).

Al final del capítulo, todo el modelo del banco que armamos en el capítulo 15
va a estar migrado a Django, funcionando contra una base de datos real. Y lo
mejor: sin escribir una línea de SQL.

## Qué es un ORM y por qué existe

Antes de los ORMs, para guardar un objeto Python en una base de datos había que
escribir SQL a mano:

```python
# Sin ORM: SQL manual
import sqlite3

conexion = sqlite3.connect("banco.db")
cursor = conexion.cursor()

cursor.execute("""
    INSERT INTO cuentas (numero, titular, saldo, activa)
    VALUES (?, ?, ?, ?)
""", (cuenta.numero, cuenta.titular_id, cuenta.saldo, cuenta.activa))

conexion.commit()
```

Y para leer:

```python
cursor.execute("SELECT * FROM cuentas WHERE numero = ?", (numero,))
fila = cursor.fetchone()
# fila es una tupla: (numero, titular_id, saldo, activa)
# hay que reconstruir manualmente el objeto Cuenta
cuenta = Cuenta(numero=fila[0], titular_id=fila[1], saldo=fila[2])
```

Este código tiene varios problemas:

- **Mezcla dos mundos**: código Python + strings de SQL. Difícil de leer,
  propenso a errores.
- **Manual**: cada operación (INSERT, SELECT, UPDATE, DELETE) es un método
  distinto que hay que escribir.
- **Inseguro si no se hace bien**: concatenar strings con datos de usuario abre
  la puerta a inyección SQL, uno de los ataques más comunes en la web.
- **Dependiente del motor**: si mañana cambiás de SQLite a PostgreSQL, hay
  que revisar todo el SQL.
- **Sin conversión de tipos**: la base de datos devuelve tuplas de strings y
  números, vos tenés que reconstruir los objetos.

Un ORM resuelve todo eso. Definís tus clases Python (llamadas modelos), y el
ORM se encarga automáticamente de:

- Crear las tablas en la base de datos.
- Convertir objetos Python en filas al guardar.
- Convertir filas en objetos al leer.
- Traducir consultas Python en SQL correcto y seguro.
- Manejar cambios de esquema con migraciones.

Django trae su propio ORM, y es uno de los más maduros del ecosistema. Vamos a
verlo.

## De clase Python a modelo Django

Miremos primero la clase Cuenta como la escribimos en el capítulo 15:

```python
class Cuenta:
    def __init__(self, numero, titular, saldo_inicial=0):
        self._numero = numero
        self._titular = titular
        self._saldo = saldo_inicial
        self._movimientos = []
        self._activa = True

    def depositar(self, monto, descripcion=""):
        # ... validaciones ...
        self._saldo += monto
        # ...
```

Ahora la versión Django del mismo concepto:

`banco/models.py`

```python
from django.db import models


class Cuenta(models.Model):
    numero = models.CharField(max_length=20, unique=True)
    titular = models.ForeignKey('Persona', on_delete=models.PROTECT)
    saldo = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    activa = models.BooleanField(default=True)

    def depositar(self, monto, descripcion=""):
        # ... validaciones ...
        self.saldo += monto
        self.save()
```

Compará las dos versiones:

- **La estructura es la misma**: una clase con atributos y métodos.
- **Los atributos ahora son `models.Field`**: `CharField`, `DecimalField`,
  `BooleanField`. Cada tipo de campo se corresponde con un tipo de columna en la
  base de datos.
- **`ForeignKey`**: la referencia a Persona ya no es un objeto Python cualquiera,
  es una relación entre tablas.
- **La clase hereda de `models.Model`**: eso le da todos los superpoderes
  (guardar, buscar, borrar).
- **Aparece `self.save()`**: guarda el objeto en la base después de modificarlo.

El código de negocio (validaciones, cálculos, reglas) queda igual. Lo único que
cambia es cómo se declaran los atributos y cómo se persiste el estado.

Eso es la promesa del ORM: el modelo del mundo (tu clase) casi no cambia, solo
cambia la infraestructura.

## Tipos de campos

Un modelo Django es una clase Python donde cada atributo declara qué tipo de
columna tiene en la base de datos. Los tipos más comunes:

### Texto

```python
nombre = models.CharField(max_length=100)       # texto corto, longitud limitada
descripcion = models.TextField()                # texto largo, sin límite
email = models.EmailField()                     # texto validado como email
```

`CharField` requiere `max_length` obligatoriamente. Es el equivalente a VARCHAR(N)
en SQL.

### Números

```python
edad = models.IntegerField()                                  # entero
saldo = models.DecimalField(max_digits=15, decimal_places=2)  # decimal exacto
peso = models.FloatField()                                    # decimal aproximado
```

`DecimalField` es clave para dinero: usa aritmética exacta (no de punto
flotante), evitando errores de redondeo. `max_digits` es el total de dígitos,
`decimal_places` los que van después de la coma.
`DecimalField(max_digits=15, decimal_places=2)` acepta hasta 9999999999999.99.

### Booleanos

```python
activa = models.BooleanField(default=True)
```

### Fechas y horas

```python
fecha_nacimiento = models.DateField()
creado_en = models.DateTimeField(auto_now_add=True)
modificado_en = models.DateTimeField(auto_now=True)
```

- `DateField`: solo fecha.
- `DateTimeField`: fecha + hora.
- `auto_now_add=True`: pone la fecha/hora al crear el objeto (no cambia después).
- `auto_now=True`: actualiza la fecha/hora cada vez que se guarda el objeto.

### Opciones especiales

Casi todos los campos aceptan estos parámetros adicionales:

```python
nombre = models.CharField(
    max_length=100,
    unique=True,                # no puede haber dos con el mismo valor
    blank=False,                # no puede estar vacío en formularios
    null=False,                 # no puede ser NULL en la base
    default="Sin nombre",       # valor por defecto
    verbose_name="Nombre completo",           # etiqueta legible
    help_text="Nombre y apellido",            # ayuda en formularios
)
```

Una aclaración importante: `blank` y `null` no son lo mismo.

- `null=True`: la base de datos permite NULL en esa columna.
- `blank=True`: los formularios de Django permiten dejar el campo vacío.

Convención: para campos de texto (`CharField`, `TextField`), usá `blank=True` pero no
`null=True`. Django prefiere guardar el string vacío "" a NULL. Para campos
numéricos o de fecha, si querés opcionalidad, usá ambos.

## Relaciones entre modelos

En POO usamos composición (un objeto tiene otros objetos como atributos). En
bases de datos relacionales, esas mismas relaciones se expresan con claves
foráneas (foreign keys). Django unifica ambos mundos con tres tipos de
relaciones:

### ForeignKey: uno a muchos

Un titular tiene varias cuentas, pero cada cuenta tiene un solo titular:

```python
class Cuenta(models.Model):
    titular = models.ForeignKey('Persona', on_delete=models.PROTECT)
```

- 'Persona' es el nombre de la clase relacionada (como string, para permitir
  referencias adelantadas).
- `on_delete=models.PROTECT` dice qué hacer si se borra la persona. Opciones:

| Opción | Qué hace |
| --- | --- |
| CASCADE | si se borra la persona, se borran sus cuentas. |
| SET_NULL | al borrar la persona, las cuentas quedan con titular = NULL. |
| PROTECT | no permite borrar la persona si tiene cuentas asociadas. |
| SET_DEFAULT | usa el valor default del campo. |

Para un banco, PROTECT es lo más seguro: no querés borrar accidentalmente
clientes que tienen cuentas activas.

### OneToOneField: uno a uno

Cada usuario tiene un perfil, y cada perfil pertenece a un solo usuario:

```python
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20)
```

Sirve para "extender" un modelo existente con datos adicionales.

### ManyToManyField: muchos a muchos

Un alumno cursa varias materias, y cada materia tiene varios alumnos:

```python
class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    materias = models.ManyToManyField('Materia')
```

Django crea automáticamente una tabla intermedia para manejar la relación. No
la vas a ver salvo que hagas queries explícitas.

### Acceso desde el otro lado

Django genera automáticamente el "inverso" de cada relación. Si `Cuenta.titular`
es una `ForeignKey` a Persona, entonces desde una persona podés acceder a sus
cuentas con:

```python
ana = Persona.objects.get(dni="12345678")
cuentas_de_ana = ana.cuenta_set.all()    # todas las cuentas de Ana
```

`cuenta_set` es el nombre por defecto (nombre del modelo hijo en minúscula +
`_set`). Podés personalizarlo con `related_name`:

```python
class Cuenta(models.Model):
    titular = models.ForeignKey('Persona', on_delete=models.PROTECT,
                              related_name='cuentas')
```

Ahora `ana.cuentas.all()` te da todas las cuentas - más natural de leer.

## Migraciones: sincronizar código y base

Cuando definís un modelo, es solo código Python. La base de datos todavía no
tiene la tabla. Las migraciones son la forma en que Django sincroniza tu código
con el esquema de la base de datos.

El ciclo tiene dos pasos:

![Diagrama "De cambiar models.py a actualizar la base de datos", con tres cajas apiladas de arriba hacia abajo unidas por flechas. Caja 1 (borde azul), "Editás models.py": "Agregás una clase, un campo o modificás algo", con el ejemplo class Cuenta(models.Model): cbu = models.CharField(max_length=22). Caja 2 (borde verde), "python manage.py makemigrations": "Django compara models.py con el estado previo y genera un archivo describiendo los cambios", con el archivo migrations/0002_agregar_cbu.py. Caja 3 (borde naranja), "python manage.py migrate": "Django ejecuta el SQL correspondiente contra la base de datos", con ALTER TABLE cuenta ADD COLUMN cbu .... Al pie, un recuadro con ícono de documento: "En resumen: primero cambiás el modelo, luego Django crea la migración y finalmente aplica los cambios en la base de datos."](images/cap16-ciclo-models-makemigrations-migrate.jpg)

### Ejemplo del ciclo completo

Supongamos que agregás una clase nueva Persona en `banco/models.py`:

`banco/models.py`

```python
from django.db import models


class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return f"{self.nombre} (DNI {self.dni})"
```

Ejecutás:

```bash
python manage.py makemigrations
```

Django analiza tus modelos, detecta que hay un cambio (el modelo Persona es
nuevo), y crea un archivo en `banco/migrations/`:

```text
Migrations for 'banco':
  banco/migrations/0001_initial.py
    - Create model Persona
```

Ese archivo describe el cambio en Python. Después:

```bash
python manage.py migrate
```

Django ejecuta el SQL necesario contra la base de datos. Con SQLite (que es lo
que estamos usando por defecto), crea el archivo `db.sqlite3` en la raíz del
proyecto y agrega la tabla.

**¿Por qué en dos pasos?** Porque separan "declarar cambio" de "aplicar
cambio". Podés revisar el archivo de migración antes de aplicarlo, versionarlo
con Git (así los cambios de esquema son parte de la historia del proyecto), y
aplicarlo en distintos entornos (desarrollo, staging, producción) de forma
consistente.

Cada vez que modifiques modelos (agregar campos, cambiar tipos, borrar clases)
repetís el ciclo `makemigrations + migrate`.

### Las migraciones iniciales de Django

Cuando arrancás un proyecto, Django ya trae varios modelos internos (usuarios,
sesiones, admin). Antes de agregar los nuestros, corramos las migraciones que
ya existen:

```bash
python manage.py migrate
```

Vas a ver mensajes como:

```text
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

Al terminar, tenés un archivo `db.sqlite3` en la raíz del proyecto con todas las
tablas internas de Django listas. Ahora sí, podemos agregar las nuestras.

## El shell de Django

Antes de meternos con el banco, hay una herramienta que vale la pena conocer:
el shell interactivo de Django. Es una consola Python especial que ya tiene
todo tu proyecto cargado y listo para explorar.

```bash
python manage.py shell
```

Se abre un intérprete Python normal, pero con Django configurado. Podés
importar tus modelos y probarlos en tiempo real:

```python
>>> from banco.models import Persona
>>> ana = Persona(nombre="Ana Pérez", dni="12345678")
>>> ana.save()
>>> Persona.objects.all()
<QuerySet [<Persona: Ana Pérez (DNI 12345678)>]>
```

Es la mejor forma de aprender el ORM: probar cosas y ver qué pasa. Vamos a
usarlo mucho en este capítulo. Para salir del shell: **`exit()`** o **`Ctrl+D`**.

## El ORM en acción

Con Django, guardar y consultar objetos se ve como código Python normal. No hay
SQL a la vista.

### Crear objetos

Dos formas equivalentes:

```python
# Forma 1: crear en memoria, después guardar
persona = Persona(nombre="Ana Pérez", dni="12345678")
persona.save()

# Forma 2: crear y guardar en una sola línea
persona = Persona.objects.create(nombre="Juan López", dni="87654321")
```

La primera es útil cuando querés hacer validaciones antes de persistir. La
segunda es más común.

### Consultar objetos

Cada modelo tiene un atributo especial `.objects` que es el manager, el punto de
entrada para todas las consultas.

```python
# Traer todas las personas
Persona.objects.all()
# <QuerySet [<Persona: Ana Pérez>, <Persona: Juan López>]>

# Traer una específica por su clave primaria (pk)
Persona.objects.get(pk=1)
# <Persona: Ana Pérez>

# Traer por otro campo
Persona.objects.get(dni="12345678")

# Filtrar (múltiples resultados)
Persona.objects.filter(nombre__startswith="A")
# todas las que empiezan con "A"

# Contar
Persona.objects.count()

# Existencia
Persona.objects.filter(dni="12345678").exists()
```

### Consultas más ricas

Django tiene un lenguaje de consultas expresivo. Se hace con filtros
dobles-subrayado (llamados lookups):

```python
# Personas cuyo nombre contiene "Pérez"
Persona.objects.filter(nombre__contains="Pérez")

# Cuentas con saldo mayor a 10000
Cuenta.objects.filter(saldo__gt=10000)

# Movimientos posteriores a una fecha
Movimiento.objects.filter(fecha__gte=fecha_desde)

# Múltiples filtros (AND)
Cuenta.objects.filter(saldo__gt=10000, activa=True)

# Excluir
Cuenta.objects.exclude(saldo=0)

# Ordenar
Cuenta.objects.all().order_by('-saldo')    # descendente por saldo

# Encadenar
Cuenta.objects.filter(activa=True).order_by('-saldo')[:5]    # top 5 saldos
```

### Los sufijos más comunes:

| Sufijo | Significa |
| --- | --- |
| exact | Igual (default) |
| iexact | Igual, case-insensitive |
| contains | Contiene el texto |
| icontains | Contiene, case-insensitive |
| gt, gte | Mayor, mayor o igual |
| lt, lte | Menor, menor o igual |
| in | Está en la lista |
| startswith, endswith | Empieza/termina con |
| isnull | Es NULL |

### Actualizar

Modificás atributos y guardás:

```python
ana = Persona.objects.get(dni="12345678")
ana.nombre = "Ana María Pérez"
ana.save()
```

O actualizás varios objetos a la vez:

```python
Cuenta.objects.filter(activa=False).update(saldo=0)
```

### Borrar

```python
ana = Persona.objects.get(dni="12345678")
ana.delete()

# O borrar múltiples
Cuenta.objects.filter(saldo=0).delete()
```

## QuerySets: evaluación diferida

Un detalle importante: las consultas de Django son **lazy (perezosas)**. Cuando
escribís `Persona.objects.filter(...)`, no se ejecuta SQL todavía. Solo se
ejecuta cuando iterás, contás, o convertís a lista:

```python
qs = Persona.objects.filter(nombre__startswith="A")    # no ejecuta nada aún

# Cualquiera de estas dispara el SQL:
list(qs)
qs.count()
for p in qs: ...
qs[0]
```

Esto permite encadenar filtros sin sobrecargar la base:

```python
qs = Cuenta.objects.all()          # nada aún
qs = qs.filter(activa=True)        # nada aún
qs = qs.order_by('-saldo')         # nada aún
qs = qs[:10]                       # nada aún
lista = list(qs)                   # acá recién se ejecuta el SQL
```

Django construye una sola consulta óptima con todos los filtros combinados.

## Métodos personalizados: la lógica del dominio

Un modelo Django no es solo una definición de tabla. Es una clase Python
normal, y puede tener todos los métodos que quieras. Toda la lógica de negocio
que armamos en el capítulo 15 sigue viviendo acá.

Ejemplo:

```python
class Cuenta(models.Model):
    numero = models.CharField(max_length=20, unique=True)
    titular = models.ForeignKey('Persona', on_delete=models.PROTECT,
                              related_name='cuentas')
    saldo = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    activa = models.BooleanField(default=True)

    def depositar(self, monto):
        """Aumenta el saldo (con validación básica)."""
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        self.saldo += monto
        self.save()

    def extraer(self, monto):
        """Reduce el saldo si hay suficiente."""
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        if monto > self.saldo:
            raise ValueError("Saldo insuficiente")
        self.saldo -= monto
        self.save()

    def cerrar(self):
        """Baja lógica."""
        self.activa = False
        self.save()

    def __str__(self):
        return f"Cuenta {self.numero} - {self.titular} - ${self.saldo}"
```

Los métodos son idénticos a los del capítulo 15, salvo por dos diferencias:

- **`self.save()` al final**: persiste el cambio en la base. Sin esto, el objeto
  queda modificado en memoria pero la base no lo sabe.
- **Sin _ (guion bajo) en los atributos**: en Django, los campos del modelo no
  son "privados con guion bajo". El ORM necesita acceso directo.
  Encapsulamiento se hace de otras formas (más adelante).

## Herencia de modelos

En el capítulo 15 tuvimos herencia: Cuenta como clase abstracta, con
`CuentaAhorro`, `CuentaCorriente`, `CuentaSueldo` como subclases. Django ofrece tres
estrategias para modelar esto:

### 1: Abstract base classes: para código compartido sin tabla

Cuando la clase padre no debería existir como tabla propia, solo servir para
compartir código:

```python
class Cuenta(models.Model):
    numero = models.CharField(max_length=20, unique=True)
    titular = models.ForeignKey('Persona', on_delete=models.PROTECT)
    saldo = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    activa = models.BooleanField(default=True)

    def depositar(self, monto):
        ...

    class Meta:
        abstract = True          # esta línea la hace abstracta
```

Con `abstract = True`, Django no crea tabla para Cuenta. Los campos y métodos se
heredan a las subclases, y cada subclase tiene su propia tabla con esos campos
incluidos.

### 2: Multi-table inheritance: para jerarquías reales

Cuando querés que el padre exista como tabla y las hijas también, con relación
entre ellas:

```python
class Cuenta(models.Model):
    numero = models.CharField(max_length=20, unique=True)
    titular = models.ForeignKey('Persona', on_delete=models.PROTECT)
    saldo = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    activa = models.BooleanField(default=True)


class CuentaAhorro(Cuenta):     # sin abstract = True
    tasa_interes_anual = models.DecimalField(max_digits=5, decimal_places=2,
                                           default=5)


class CuentaCorriente(Cuenta):
    limite_descubierto = models.DecimalField(max_digits=15, decimal_places=2,
                                            default=0)
```

Django crea dos tablas por cada subclase: una para Cuenta (con los campos
comunes), y una para `CuentaAhorro`/`CuentaCorriente` (con los específicos). Las
une con un JOIN automático.

| Ventaja | Desventaja |
| --- | --- |
| podés consultar Cuenta.objects.all() y traer todas las cuentas, sin importar el tipo. También podés consultar por subclase específica. | cada operación implica un JOIN, algo más lento en tablas gigantes. |

### 3: Proxy models: el mismo modelo, distintas vistas

Cuando querés reusar la misma tabla con distinto comportamiento en Python
(raro, lo mencionamos para completitud):

```python
class CuentaVIP(Cuenta):
    class Meta:
        proxy = True

    def hacer_algo_especial(self):
        ...
```

No se crea tabla nueva. `CuentaVIP` opera sobre la misma tabla de Cuenta, solo
cambia el comportamiento del modelo Python.

### Elegimos multi-table inheritance

Para el banco, multi-table inheritance es la elección natural. Corresponde uno
a uno con nuestro diseño del capítulo 15 y permite consultas polimórficas.

## Traduciendo el proyecto bancario

Ya tenemos todos los conceptos. Ahora hagamos la traducción real: el sistema
bancario del capítulo 15 se convierte en modelos Django.

`banco/models.py`

```python
"""Modelos del sistema bancario."""

from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError


class Persona(models.Model):
    """Titular de una o más cuentas bancarias.

    Padre abstracto: cada persona real es PersonaFisica o PersonaJuridica.
    """
    nombre = models.CharField(max_length=100)
    creado_en = models.DateTimeField(auto_now_add=True)

    def identificacion(self):
        raise NotImplementedError("Las subclases deben implementar esto")

    def __str__(self):
        return f"{self.nombre} ({self.identificacion()})"


class PersonaFisica(Persona):
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, unique=True)
    edad = models.IntegerField()

    class Meta:
        verbose_name = "Persona Física"
        verbose_name_plural = "Personas Físicas"

    def identificacion(self):
        return f"DNI {self.dni}"

    def nombre_completo(self):
        return f"{self.apellido}, {self.nombre}"


class PersonaJuridica(Persona):
    cuit = models.CharField(max_length=13, unique=True)     # con guiones

    class Meta:
        verbose_name = "Persona Jurídica"
        verbose_name_plural = "Personas Jurídicas"

    @property
    def razon_social(self):
        return self.nombre

    def identificacion(self):
        return f"CUIT {self.cuit}"


class Cuenta(models.Model):
    """Cuenta bancaria genérica.

    Padre multi-table para CuentaAhorro, CuentaCorriente, CuentaSueldo.
    """
    numero = models.CharField(max_length=20, unique=True)
    titular = models.ForeignKey(
        Persona,
        on_delete=models.PROTECT,
        related_name='cuentas'
    )
    cbu = models.CharField(max_length=22, unique=True)
    saldo = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    activa = models.BooleanField(default=True)
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"

    def depositar(self, monto, descripcion=""):
        if not self.activa:
            raise ValidationError("La cuenta está inactiva")
        if monto <= 0:
            raise ValidationError("El monto debe ser positivo")

        self.saldo += Decimal(monto)
        self.save()

        Movimiento.objects.create(
            cuenta=self,
            tipo="deposito",
            monto=monto,
            saldo_posterior=self.saldo,
            descripcion=descripcion,
        )

    def extraer(self, monto, descripcion=""):
        if not self.activa:
            raise ValidationError("La cuenta está inactiva")
        if monto <= 0:
            raise ValidationError("El monto debe ser positivo")
        if monto > self.saldo:
            raise ValidationError(
                f"Saldo insuficiente. Disponible: ${self.saldo}"
            )

        self.saldo -= Decimal(monto)
        self.save()

        Movimiento.objects.create(
            cuenta=self,
            tipo="extraccion",
            monto=monto,
            saldo_posterior=self.saldo,
            descripcion=descripcion,
        )

    def cerrar(self):
        self.activa = False
        self.save()

    def __str__(self):
        estado = "" if self.activa else " [INACTIVA]"
        return f"Cuenta {self.numero} - {self.titular} - ${self.saldo}{estado}"


class CuentaAhorro(Cuenta):
    tasa_interes_anual = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=5
    )

    class Meta:
        verbose_name = "Cuenta de Ahorro"
        verbose_name_plural = "Cuentas de Ahorro"

    def acreditar_intereses(self):
        if not self.activa:
            raise ValidationError("La cuenta está inactiva")

        interes = self.saldo * self.tasa_interes_anual / 100 / 12
        self.saldo += interes
        self.save()

        Movimiento.objects.create(
            cuenta=self,
            tipo="interes",
            monto=interes,
            saldo_posterior=self.saldo,
            descripcion="Interés mensual",
        )


class CuentaCorriente(Cuenta):
    limite_descubierto = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    class Meta:
        verbose_name = "Cuenta Corriente"
        verbose_name_plural = "Cuentas Corrientes"

    def extraer(self, monto, descripcion=""):
        """Permite descubierto hasta el límite."""
        if not self.activa:
            raise ValidationError("La cuenta está inactiva")
        if monto <= 0:
            raise ValidationError("El monto debe ser positivo")

        disponible = self.saldo + self.limite_descubierto
        if monto > disponible:
            raise ValidationError(
                f"Se excede el límite. Disponible: ${disponible}"
            )

        self.saldo -= Decimal(monto)
        self.save()

        Movimiento.objects.create(
            cuenta=self,
            tipo="extraccion",
            monto=monto,
            saldo_posterior=self.saldo,
            descripcion=descripcion,
        )


class CuentaSueldo(Cuenta):
    tope_sin_retencion = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=1000000
    )

    class Meta:
        verbose_name = "Cuenta Sueldo"
        verbose_name_plural = "Cuentas Sueldo"


class Movimiento(models.Model):
    """Registro de una operación sobre una cuenta."""

    TIPOS = [
        ('deposito', 'Depósito'),
        ('extraccion', 'Extracción'),
        ('interes', 'Interés'),
        ('transferencia', 'Transferencia'),
        ('apertura', 'Apertura'),
    ]

    cuenta = models.ForeignKey(
        Cuenta,
        on_delete=models.CASCADE,
        related_name='movimientos'
    )
    tipo = models.CharField(max_length=20, choices=TIPOS)
    monto = models.DecimalField(max_digits=15, decimal_places=2)
    saldo_posterior = models.DecimalField(max_digits=15, decimal_places=2)
    descripcion = models.CharField(max_length=200, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Movimiento"
        verbose_name_plural = "Movimientos"
        ordering = ['-fecha']       # por defecto, más recientes primero

    def __str__(self):
        signo = "+" if self.tipo in ("deposito", "interes", "apertura") else "-"
        return f"{self.fecha:%d/%m/%Y %H:%M} | {self.tipo} | {signo}${self.monto}"
```

Ese archivo entero es equivalente a todos los archivos `personas.py`, `cuentas.py`,
`movimientos.py` del capítulo 15, más las validaciones. Los cambios respecto de
la versión Python pura:

- Los campos son `models.Field` en vez de asignaciones en `__init__`.
- Las validaciones usan `ValidationError` en vez de excepciones personalizadas.
  Es la excepción idiomática de Django, y el admin/formularios la detectan
  automáticamente.
- Los movimientos se crean con `Movimiento.objects.create(...)` en vez de
  `list.append(...)`. Cada movimiento se guarda automáticamente en la base.
- Cada operación que modifica el estado llama `self.save()` para persistir.
- Uso de `Decimal` al hacer aritmética con `DecimalField`. Este es un detalle
  importante: `DecimalField` guarda decimales exactos, y hacer `self.saldo += 100`
  puede fallar si 100 es un int. Convertir explícitamente con `Decimal(monto)`
  evita problemas.
- Aparece `Meta` con `verbose_name`, `verbose_name_plural` y `ordering`. Esta clase
  interna configura metadatos del modelo, cómo lo llama Django en la interfaz,
  cómo se ordena por defecto, entre otras cosas.
- `TIPOS` en Movimiento: los `choices` restringen los valores permitidos y le dan
  un nombre legible para mostrar en el admin.

## Aplicar los cambios

Con el archivo listo, ejecutamos el ciclo de migraciones:

```bash
python manage.py makemigrations
```

Vas a ver algo como:

```text
Migrations for 'banco':
  banco/migrations/0001_initial.py
    - Create model Persona
    - Create model PersonaFisica
    - Create model PersonaJuridica
    - Create model Cuenta
    - Create model CuentaAhorro
    - Create model CuentaCorriente
    - Create model CuentaSueldo
    - Create model Movimiento
```

Después:

```bash
python manage.py migrate
```

Y las tablas quedan creadas en `db.sqlite3`. Podés verificarlo con un cliente de
SQLite (o desde el admin, en el próximo capítulo).

## Probando desde el shell

Ahora sí, entramos al shell y probamos todo:

```bash
python manage.py shell
```

```python
>>> from banco.models import PersonaFisica, PersonaJuridica, CuentaAhorro, CuentaCorriente

# Crear un titular
>>> ana = PersonaFisica.objects.create(
...     nombre="Ana",
...     apellido="Pérez",
...     dni="12345678",
...     edad=32
... )
>>> ana
<PersonaFisica: Ana (DNI 12345678)>

# Crear una cuenta para Ana
>>> cta = CuentaAhorro.objects.create(
...     numero="001-100",
...     titular=ana,
...     cbu="0170123456789012345678",
...     saldo=50000,
...     tasa_interes_anual=8
... )

# Operar
>>> cta.depositar(15000, "Depósito de prueba")
>>> cta.saldo
Decimal('65000.00')

# Ver el historial
>>> cta.movimientos.all()
<QuerySet [<Movimiento: 26/07/2026 15:42 | deposito | +$15000>,
           <Movimiento: 26/07/2026 15:41 | apertura | +$50000>]>

# Consulta: todas las cuentas de Ana
>>> ana.cuentas.all()
<QuerySet [<CuentaAhorro: Cuenta 001-100 - Ana (DNI 12345678) - $65000.00>]>

# Intentar algo que rompe la validación
>>> cta.extraer(1000000)
ValidationError: ['Saldo insuficiente. Disponible: $65000.00']

# Filtrar cuentas con saldo mayor a 30000
>>> from banco.models import Cuenta
>>> Cuenta.objects.filter(saldo__gt=30000)
<QuerySet [<Cuenta: Cuenta 001-100 - Ana (DNI 12345678) - $65000.00>]>
```

Todo funciona. Los datos persisten entre ejecuciones: si cerrás el shell y
volvés a entrar, `PersonaFisica.objects.get(dni="12345678")` te devuelve a Ana
con sus datos intactos.

## Preguntas frecuentes al empezar

Cuando arrancan con el ORM, aparecen las mismas dudas. Anticipamos las
principales:

### ¿Por qué objects.create y no save() a secas?

Podés hacer las dos cosas:

```python
# Forma explícita
p = Persona(nombre="Ana", dni="123")
p.save()

# Forma corta
p = Persona.objects.create(nombre="Ana", dni="123")
```

create hace las dos cosas en una sola llamada. Es más común, pero si necesitás
manipular el objeto antes de guardar (validar algo, calcular campos), la forma
explícita es más flexible.

### ¿Cómo hago validaciones antes de guardar?

Usá `clean()` en el modelo (Django lo llama automáticamente en formularios y en
el admin):

```python
class Persona(models.Model):
    dni = models.CharField(max_length=8, unique=True)

    def clean(self):
        if not self.dni.isdigit():
            raise ValidationError({"dni": "El DNI debe ser numérico"})
        if len(self.dni) not in (7, 8):
            raise ValidationError({"dni": "El DNI debe tener 7 u 8 dígitos"})
```

Vamos a profundizar en `clean()` en el capítulo de formularios.

### ¿Cómo pongo funciones de validación como las de validaciones.py?

En Django, esas funciones se llaman `validators` y se pasan a los campos:

```python
from banco.validaciones import es_dni_valido    # nuestra función del cap 15

class Persona(models.Model):
    dni = models.CharField(
        max_length=8,
        validators=[es_dni_valido]      # se ejecuta en formularios y clean()
    )
```

Todo lo que hicimos en `validaciones.py` sigue vivo - solo se conecta al modelo
de otra forma.

### ¿Y el archivo errores.py?

Django trae su propia jerarquía de excepciones (`ValidationError`,
`IntegrityError`, `DoesNotExist`, etc.) que el framework entiende naturalmente.
Nuestras excepciones personalizadas del capítulo 15 (`SaldoInsuficienteError`,
etc.) las podés seguir usando, pero es más pythónico en Django lanzar
`ValidationError` con un mensaje claro. El admin y los formularios saben cómo
mostrarlo.

### ¿Se puede usar el ORM sin Django?

Sí. Existen ORMs de Python independientes: SQLAlchemy es el más popular. Pero
el ORM de Django es especialmente ergonómico cuando trabajás con Django, y es
el estándar para proyectos Django. Si más adelante hacen microservicios o APIs,
SQLAlchemy puede ser una buena elección alternativa.

## Mirando lo hecho

Con este capítulo, el sistema bancario ya vive en una base de datos real. Los
datos persisten entre ejecuciones. Podemos consultar, filtrar, ordenar,
agrupar. Las relaciones entre modelos funcionan automáticamente.

¡Y ni una línea de SQL!

Todavía no hay interfaz gráfica: solo shell. En el próximo capítulo, El Admin
de Django, vamos a ver la promesa que veníamos haciendo desde el capítulo 12:
con 3 líneas de código, Django genera una interfaz web completa de ABM para
todos nuestros modelos. Alta, consulta, modificación, baja, búsqueda, filtros.
Todo listo, sin escribir vistas ni templates.

Ese momento, cuando ves que el mismo trabajo del capítulo 12 se resuelve con
`admin.site.register(Cuenta)`, es cuando entienden por qué Django tiene el
prestigio que tiene. Y por qué todo el capítulo 15, con sus SOLID y clases
abstractas, no fue en vano: el ORM les pide exactamente el mismo tipo de
pensamiento OO que ya aprendieron.
