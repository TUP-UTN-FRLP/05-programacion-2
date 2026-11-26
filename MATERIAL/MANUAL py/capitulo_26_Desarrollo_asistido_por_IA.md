# Capítulo 26. Desarrollo asistido por IA: agentes en el flujo de trabajo

*Desarrollar durante el 2026, por ahora.*

## ¿Por qué leemos este capítulo?

Terminaste un manual completo sobre Python y Django. Aprendieron a diseñar
clases, a modelar dominios, a testear, a deployar. Todas habilidades sólidas
y transferibles.

Pero hay algo que cambió en los últimos años y que va a seguir cambiando:
**cómo se programa**. Hasta hace poco, escribir código era una actividad casi
enteramente humana. Uno pensaba, tipeaba, revisaba, corregía. Los editores
ayudaban con autocompletado sintáctico y detección de errores triviales, pero
el pensamiento era 100% del programador.

Hoy, en 2026, esa realidad cambió radicalmente. Los **modelos de lenguaje**
(LLMs) alcanzaron un nivel donde pueden asistir productivamente en tareas de
programación: sugerir código, refactorizar, explicar bugs, escribir tests,
generar documentación. Y los **agentes de código** - sistemas que combinan
modelos con la capacidad de ejecutar tareas, leer archivos, correr comandos -
han transformado la forma en que muchos desarrolladores trabajan día a día.

Este capítulo no es sobre Python ni sobre Django. Es sobre **cómo programar en
2026 y hacia adelante**. Cómo integrar estos asistentes de forma productiva.
Cómo elegir la herramienta adecuada para cada tarea. Cómo trabajar con **datos
sensibles** sin exponerlos a servicios externos. Y - quizás lo más importante
- cómo mantener el criterio propio para no volverse dependiente de algo que a
veces se equivoca con confianza.

Al final del capítulo van a tener una comprensión práctica del panorama de
agentes IA, un stack recomendado para trabajar en proyectos como el banco, y -
clave para un banco real - un stack **100% local** para código que nunca
debería salir de tu computadora.

## Un poco de contexto: modelos vs agentes

Antes de meternos con herramientas, distingamos dos conceptos que se mezclan
mucho:

| Modelo de lenguaje (LLM) | Agente de código |
| --- | --- |
| Es el motor de IA subyacente. Recibe texto, devuelve texto. Ejemplos: **Claude Opus/Sonnet/Haiku** (de Anthropic), **GPT-5 y sus variantes** (de OpenAI), **Gemini** (de Google), **DeepSeek**, **Qwen**, **Llama** (open source). Cada uno con sus fortalezas, costos y limitaciones. | Es la herramienta que integra un modelo con capacidades adicionales - leer tus archivos, ejecutar comandos, ver la salida, iterar hacia un objetivo. Ejemplos: **Claude Code**, **Cursor**, **GitHub Copilot**, **Cline** (antes Continue), **Aider**, **Windsurf**. Un mismo agente puede usar distintos modelos por detrás. |

> **La analogía útil:** El modelo es el motor, el agente es el auto. Podés
> cambiar el motor de tu auto (usar Claude Sonnet en vez de GPT), o cambiar de
> auto manteniendo el motor (pasar de Cursor a Cline usando el mismo modelo).
> Los dos son elecciones importantes.

Otra distinción clave: **completion** vs **chat** vs **agente**.

- **Completion** (autocomplete): sugiere el próximo fragmento de código
  mientras tipeás. Sin conversación, sin contexto amplio. Ejemplo: GitHub
  Copilot autocompletando dentro de una función.
- **Chat**: una conversación con el modelo. Vos preguntás, él responde. Podés
  adjuntar código. El modelo no ejecuta nada - solo sugiere.
- **Agente**: el modelo puede leer archivos de tu proyecto, ejecutar comandos
  (pytest, git, ls), interpretar la salida, y decidir el próximo paso. Puede
  iterar hasta lograr un objetivo sin que le vayas indicando cada paso.

Los tres modos son útiles en distintos momentos. Un buen desarrollador de 2026
los combina fluidamente.

## Panorama de modelos: qué usar para qué

El ecosistema de LLMs cambia rápido. Los modelos que menciono acá pueden estar
obsoletos en un año. Pero los **criterios** para elegir son estables. Vamos
con los criterios primero, después con los modelos actuales.

### Criterios para elegir un modelo

1. **Capacidad**: qué tan bien resuelve tareas complejas de código. Los
   modelos más grandes suelen ser mejores, pero también más lentos y caros.
2. **Contexto**: cuánta información pueden procesar en una sola interacción.
   Se mide en **tokens** (aproximadamente, 1 token ≈ 4 caracteres). Un
   contexto de 200K tokens permite pasarle un proyecto entero mediano. Un
   contexto de 4K tokens apenas te alcanza para una función mediana.
3. **Velocidad**: qué tan rápido responde. Un modelo lento rompe el flujo de
   trabajo.
4. **Costo por token**: los servicios cobran por tokens de entrada (lo que le
   mandás) y salida (lo que responde). La diferencia entre un modelo caro y
   uno barato puede ser 20x.
5. **Especialización**: algunos modelos están específicamente entrenados para
   código, otros son generalistas. Los de código suelen ser más precisos en
   tareas técnicas.
6. **Privacidad**: ¿los datos que le mandás quedan en los servidores del
   proveedor? ¿Se usan para entrenar futuros modelos? Crítico para trabajar
   con código propietario.

## Los grandes proveedores (2026)

#### Anthropic - familia Claude:

- **Claude Opus**: el modelo tope de gama de Anthropic. El más capaz para
  tareas complejas de razonamiento y arquitectura. Caro.
- **Claude Sonnet**: equilibrio entre capacidad y costo. El caballo de batalla
  para desarrollo diario. La opción por defecto de muchos profesionales.
- **Claude Haiku**: rápido y barato. Ideal para tareas repetitivas, refactors
  simples, autocompletado.
- **Claude Fable**: modelo de la familia Claude 5 con foco en fluidez para
  tareas más generales y creativas. Buena opción cuando el problema no es
  puramente técnico y hay que combinar código con explicaciones,
  documentación, prompts o interacción conversacional larga.

#### OpenAI - familia GPT:

- **GPT-5 y sus variantes tope**: competencia directa de Claude Opus.
- **GPT-5 mini / o-series**: variantes más rápidas y baratas.

#### Google - familia Gemini:

- **Gemini Pro**: capacidad alta, contexto grande. Fortaleza en tareas
  multimodales (imágenes + código).
- **Gemini Flash**: rápido y barato.

## Open source (para correr local o en tu propia infraestructura):

- **DeepSeek Coder**: especializado en código. Muy buena calidad-precio.
- **Qwen Coder** (de Alibaba): serie de modelos de código. Desde 1.5B (chico,
  para máquinas modestas) hasta 32B+ (potente, requiere GPU seria).
- **Llama** (de Meta): generalista, con variantes especializadas para código.
- **Codestral** (de Mistral): enfocado en código, buena calidad.

Los modelos open source son la base para el **stack local** que vamos a montar
más adelante.

## Estratificación de tareas por modelo

Una regla fundamental para trabajar bien con agentes: **no usar el modelo más
grande para todo**. Es caro, es lento, y muchas veces innecesario. Estratificar
las tareas por complejidad y elegir el modelo adecuado optimiza tiempo y
costos.

### Nivel 1: Tareas triviales (modelos chicos / autocompletado)

**Qué son**: cosas mecánicas que no requieren razonamiento profundo.

- Autocompletado mientras escribís.
- Renombrar variables consistentemente.
- Convertir loops a comprensiones y viceversa.
- Agregar type hints obvios (x: int cuando x claramente es un entero).
- Generar `__str__` a partir de atributos de una clase.
- Traducir comentarios entre idiomas.

**Modelos recomendados**: Claude Haiku, GPT-5 mini, Gemini Flash, Qwen Coder 7B
local, DeepSeek Coder Lite.

**Por qué no usar modelos grandes**: es como usar un colectivo para ir a la
esquina. La respuesta es la misma, pero pagás 10x más y esperás más tiempo.

### Nivel 2: Tareas de desarrollo cotidiano (modelos medianos)

**Qué son**: la mayoría del trabajo diario. Requieren entender contexto, pero
no arquitectura profunda.

- Escribir una función nueva a partir de una descripción.
- Convertir modelos Python a modelos Django (como hicimos en el capítulo 17).
- Escribir tests para una clase existente.
- Refactorizar un método largo en varios más chicos.
- Debuggear un error específico dado el traceback y el código relevante.
- Generar formularios Django a partir de modelos.
- Escribir queries del ORM que respondan preguntas específicas.

**Modelos recomendados**: Claude Sonnet, GPT-5 (versión estándar), Gemini Pro,
Qwen Coder 32B local.

**Por qué son la elección por defecto**: cubren el 80% de las tareas de
programación diaria. La relación calidad/costo es óptima. Casi todos los
agentes de código profesionales usan modelos de este nivel como default.

### Nivel 3: Tareas complejas (modelos tope de gama)

**Qué son**: problemas que requieren razonamiento arquitectural, análisis
profundo, o síntesis de mucha información.

- Diseñar la arquitectura de una app completa.
- Migrar un sistema monolítico a microservicios.
- Debuggear un problema de performance que involucra múltiples capas.
- Reescribir código legacy respetando la funcionalidad completa.
- Análisis de seguridad de una aplicación entera.
- Diseño de esquemas de base de datos complejos con muchas relaciones.
- Traducir un sistema entero de un framework a otro.

**Modelos recomendados**: Claude Opus, GPT-5 tope, Gemini Pro alto.

**Por qué solo para tareas complejas**: son 5-10x más caros que los medianos.
Reservalos para cuando la complejidad lo justifique.

### La regla práctica

En el flujo diario:

1. **Autocompletado**: modelo chico corriendo en el editor.
2. **Chat/agente para tareas normales**: modelo mediano (Claude Sonnet es una
   elección segura).
3. **Solo cuando el mediano no alcanza**: escalar al modelo grande.

Los buenos desarrolladores en 2026 tienen configurados **2 o 3 modelos**
simultáneamente, uno para cada nivel. No usan uno solo para todo.

## Agentes en VSCode

VSCode es el editor más usado por desarrolladores Python en 2026. Hay varias
extensiones para integrar agentes IA. Repaso las principales.

### GitHub Copilot

- **Qué es**: extensión oficial de GitHub. La más popular.
- **Modelo**: usa GPT-5 y variantes por defecto. Podés cambiar entre modelos.
- **Modos**: autocompletado inline, chat, agente ("Copilot Agent Mode").
- **Precio**: suscripción mensual (~$10 USD/mes). Free para estudiantes con
  GitHub Education.
- **Fortalezas**: integración impecable con VSCode, muy rápido, historial de
  usar la interfaz.
- **Debilidades**: código propietario va a servidores de OpenAI/Microsoft.

**Cuándo usarlo**: buena opción por defecto para desarrolladores que ya
trabajan en el ecosistema GitHub. Bueno para proyectos personales, código open
source, cursos.

### Claude Code

- **Qué es**: herramienta oficial de Anthropic. Extensión VSCode + CLI.
- **Modelo**: familia Claude (Opus, Sonnet, Haiku).
- **Modos**: fuertemente enfocado en modo agente. Puede leer archivos, correr
  comandos, iterar.
- **Precio**: se paga por uso (pay-per-token) via API de Anthropic, o incluido
  en suscripciones Claude Pro/Team.
- **Fortalezas**: excelente para tareas complejas, muy bueno en refactors
  grandes, entiende bien código Python y web.
- **Debilidades**: código sale a servidores de Anthropic.

**Cuándo usarlo**: cuando la calidad del modelo importa más que la velocidad.
Especialmente útil en refactors, generación de código estructurado, revisión
de código.

### Cline (antes Continue)

- **Qué es**: extensión open source. Muy flexible.
- **Modelo**: **cualquier modelo compatible** - Claude, GPT, Gemini, y también
  modelos locales via Ollama.
- **Modos**: agente, chat, autocompletado.
- **Precio**: la extensión es gratis. Pagás por lo que consumas al modelo que
  elijas.
- **Fortalezas**: flexibilidad máxima. Puede usar un modelo distinto según la
  tarea. Soporta modelos locales para privacidad.
- **Debilidades**: configuración más compleja que Copilot.

**Cuando usarlo**: cuando necesitás flexibilidad, cuando querés combinar
modelos remotos y locales, cuando trabajás con datos sensibles.

### Cursor

- **Qué es**: no es una extensión sino un **editor completo** - un fork de
  VSCode con IA integrada nativamente.
- **Modelo**: Claude, GPT, y otros vía suscripción propia.
- **Modos**: todo integrado profundamente. Cursor Composer para tareas de
  agente sobre múltiples archivos.
- **Precio**: free tier limitado, plan pro ~$20 USD/mes.
- **Fortalezas**: la mejor UX para trabajar con IA. Autocompletado con
  "predicción de múltiples líneas".
- **Debilidades**: es un editor aparte - cambiás VSCode por Cursor. Código
  propietario sale a los servidores de Cursor.

**Cuando usarlo**: si estás dispuesto a cambiar de editor, es la experiencia
más pulida del mercado hoy.

### Aider

- **Qué es**: herramienta de terminal (no extensión de VSCode). Muy popular
  entre power users.
- **Modelo**: cualquiera (Claude, GPT, locales).
- **Modos**: agente en la terminal, con git integrado (cada cambio del agente
  es un commit).
- **Precio**: gratis, pagás por tokens.
- **Fortalezas**: git-first, ideal para cambios grandes revisables commit a
  commit. Muy transparente.
- **Debilidades**: sin GUI, curva de aprendizaje.

**Cuando usarlo**: para desarrolladores cómodos en terminal, en proyectos con
git riguroso.

### Recomendación práctica

Para el estudiante o profesional que arranca con IA en su flujo:

1. **Empezá con Cline en VSCode** - es gratis, flexible, y te permite probar
   múltiples modelos sin cambiar de herramienta.
2. **Configurá dos modelos**: uno rápido para tareas simples (Claude Haiku o
   modelo local) y uno potente para tareas complejas (Claude Sonnet u Opus).
3. **Aprendé el flujo del agente**: cómo le das contexto, cómo revisás sus
   cambios, cuándo aceptar y cuándo rechazar.
4. **Cuando sepas qué necesitás**, evaluá Cursor si querés mejor UX, Claude
   Code si te gusta el ecosistema Anthropic, o Aider si preferís terminal.

## Configurando Cline en VSCode

Vamos a ver la configuración concreta de **Cline**, porque es la opción más
flexible y gratis para empezar.

### Paso 1: instalar la extensión

En VSCode:

1. Abrí el panel de Extensions (Ctrl+Shift+X o Cmd+Shift+X).
2. Buscá **"Cline"**.
3. Instalá la extensión oficial.

Al terminar, aparece un ícono de Cline en la barra lateral.

### Paso 2: elegir un proveedor de modelo

Cline es agnóstico al modelo. Podés conectarlo a:

- **Anthropic** (Claude directo)
- **OpenAI**
- **OpenRouter** (agregador de decenas de modelos con una sola API key)
- **Ollama** (modelos locales)
- **LM Studio** (modelos locales con interfaz)
- Muchos otros

Para arrancar, dos opciones recomendadas:

#### Opción A: Anthropic directo

Andá a https://console.anthropic.com/, creá cuenta, generá una API key. Cargá
crédito ($5-10 USD alcanzan para semanas de uso moderado). Copiá la API key.

#### Opción B: OpenRouter

Andá a https://openrouter.ai/, creá cuenta, cargá crédito. Genera una API key
que te permite acceder a decenas de modelos (Claude, GPT, Gemini, Llama,
DeepSeek) con una sola cuenta. Más flexible.

Por ahora recomendamos **OpenRouter** para empezar, poder cambiar entre
modelos sin cambiar de proveedor es muy práctico.

### Paso 3: configurar Cline

En el ícono de Cline, abrí la configuración. Pegá tu API key. Elegí el modelo
que querés usar por defecto - por ejemplo `anthropic/claude-sonnet-4` en
OpenRouter.

Podés configurar dos modelos:

#### Model for regular tasks

Claude Sonnet o similar.

#### Model for autocomplete

Uno rápido y barato (Haiku, Gemini Flash).

Con eso, Cline usa el modelo adecuado según la tarea automáticamente.

### Paso 4: primera interacción

Abrí el panel de Cline. Vas a ver un prompt para escribir. Empezá con algo
simple:

```text
"Explicame qué hace el archivo banco/models.py"
```

Cline lee el archivo y te devuelve una explicación. Con eso ya estás usando un
agente.

Después, algo más ambicioso:

```text
"Quiero agregar un campo dni opcional a PersonaJuridica. Hacé el cambio en el
modelo, generá la migración y actualizá el admin si es necesario."
```

Cline analiza el código, hace los cambios, te muestra un **diff** para que
revises. Vos aprobás o pedís cambios.

**Este es el flujo básico**: darle contexto, pedirle una tarea concreta,
revisar el diff, aprobar.

### Paso 5: refinando la configuración

En proyectos serios, Cline soporta archivos .clinerules en la raíz del
proyecto donde definís reglas específicas:

`.clinerules`

```text
Este proyecto es un sistema bancario en Django.

Convenciones:
- Modelos en banco/models.py
- Vistas en banco/views.py
- Templates en banco/templates/banco/
- Tests siempre en tests/
- Usar voseo argentino en mensajes al usuario
- Todo el código en español, docstrings en español

Antes de sugerir cambios importantes, preguntá.
```

El agente respeta esas reglas en todas las interacciones del proyecto. Esto
acorta prompts y evita sugerencias que no aplican.

## Trabajando con datos sensibles: el problema

Ahora la parte crítica del capítulo. Todo lo que vimos hasta acá usa **modelos
remotos** - Claude, GPT, Gemini - que se ejecutan en servidores de las
empresas correspondientes. Cuando le mandás código a Claude, ese código:

1. Viaja por internet a servidores de Anthropic.
2. Se procesa en máquinas que no son tuyas.
3. Puede quedar guardado en logs por un tiempo.
4. Según el proveedor y el plan, puede usarse para entrenar futuros modelos.

Para código público o de proyectos personales, esto **no es un problema**. Para
código propietario de una empresa, código con lógica de negocio confidencial,
o código que maneja **datos sensibles reales** (información bancaria, salud,
gobierno), es **inaceptable**.

Ejemplos concretos donde no podés usar modelos remotos:

- Un banco real con datos de clientes.
- Una historia clínica electrónica.
- Un sistema de una agencia estatal.
- Código propietario de una empresa que te prohíbe compartirlo.
- Proyectos con NDA (acuerdo de confidencialidad).

La solución: **modelos locales**. Modelos de IA que corren **enteramente en tu
computadora**, sin comunicación con servidores externos. Nada sale de tu
máquina.

## Stack local: Ollama + modelos open source

**Ollama** es la herramienta más popular para correr modelos locales. Es como
Docker pero para modelos de IA: descargás un modelo, y con un comando lo
ejecutás.

### Instalando Ollama

Andá a https://ollama.com/ y descargá el instalador para tu sistema operativo.
La instalación es un clic.

En Linux también podés usar:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Al terminar, Ollama corre como un servicio en tu máquina, escuchando en
http://localhost:11434.

Verificalo:

```bash
ollama --version
```

### Descargando un modelo

Ollama tiene un catálogo de modelos en https://ollama.com/library. Los
recomendados para código:

**Para máquinas modestas (8-16 GB RAM, sin GPU dedicada):**

- `qwen2.5-coder:7b`: modelo de código de 7 billones de parámetros. Corre en
  CPU con 16 GB RAM. Calidad razonable para tareas simples y medianas.
- `deepseek-coder-v2:16b-lite`: variante liviana de DeepSeek. Buena para
  código.
- `codellama:7b`: Llama 2 optimizado para código. Más viejo pero probado.

**Para máquinas potentes (GPU con 12+ GB VRAM, o Mac con chip M2+/32+ GB RAM
unificada):**

- `qwen2.5-coder:32b`: la mejor calidad open source del momento para código.
  Corre bien en máquinas serias.
- `deepseek-coder-v2:236b`: enorme, solo para máquinas muy potentes o
  servidores dedicados.
- `codestral:22b`: modelo de Mistral especializado en código, muy bueno.

Para descargar:

```bash
ollama pull qwen2.5-coder:7b
```

La descarga es de varios GB. Ollama lo guarda en su caché local. La próxima
vez que lo uses, arranca al instante.

### Probando el modelo

Desde terminal:

```bash
ollama run qwen2.5-coder:7b
```

Se abre un prompt interactivo. Escribí:

```text
Escribí una función Python que calcule el factorial de un número usando recursión
```

El modelo responde con código. Ese código **nunca salió de tu máquina**. Nada
viajó por internet. Ollama corre 100% local.

### Conectando Ollama con Cline

En Cline, en la configuración de proveedores, elegí **Ollama**. Como URL,
http://localhost:11434. Elegí el modelo descargado (`qwen2.5-coder:7b`).

Ahora Cline en VSCode usa ese modelo local. Todo el flujo es idéntico al
remoto - chat, agente, autocompletado - pero **nada sale de tu computadora**.

### LM Studio: alternativa con GUI

Si preferís interfaz gráfica en vez de terminal, **LM Studio**
(https://lmstudio.ai/) hace lo mismo que Ollama con una GUI amigable.
Descargás modelos, los ejecutás, y también expone un servidor local al que
Cline se puede conectar.

Para elegir entre Ollama y LM Studio:

| Ollama | LM Studio |
| --- | --- |
| Más liviano, mejor para servidores y scripting, es la opción más adoptada. | Mejor para quien quiere una interfaz visual, buena para explorar y probar modelos. |

Ambos son gratuitos y open source.

## Comparando modelos locales vs remotos

Es importante ser realista sobre las limitaciones. Los modelos locales de
código abierto han mejorado enormemente, pero **todavía están por detrás de
los mejores modelos remotos** en tareas complejas.

Un comparativo aproximado en 2026:

| Modelo | Ambiente | Calidad para código | Velocidad | Costo |
| --- | --- | --- | --- | --- |
| **Claude Opus** | Remoto | ★★★★★ | Media | Alto |
| **Claude Sonnet** | Remoto | ★★★★☆ | Alta | Medio |
| **GPT-5** | Remoto | ★★★★★ | Media | Alto |
| **Gemini Pro** | Remoto | ★★★★☆ | Alta | Medio |
| **Qwen Coder 32B** | Local (GPU seria) | ★★★★☆ | Media | Cero |
| **Qwen Coder 7B** | Local (CPU) | ★★★☆☆ | Baja | Cero |
| **DeepSeek Coder** | Local (GPU) | ★★★★☆ | Media | Cero |
| **Codestral** | Local (GPU) | ★★★★☆ | Media | Cero |

### Interpretación práctica:

- Los modelos locales pequeños (7B) sirven bien para autocompletado, refactors
  simples, generación de código estándar. Para tareas complejas quedan cortos.
- Los modelos locales grandes (32B+) alcanzan calidad comparable a modelos
  remotos medianos como Claude Sonnet. Requieren hardware serio.
- Los mejores modelos remotos (Opus, GPT-5 tope) siguen siendo superiores para
  razonamiento complejo y tareas arquitecturales grandes.

La brecha se está achicando cada año. En 2027-2028 es probable que los modelos
locales alcancen paridad con los remotos actuales.

## Estrategia híbrida: lo mejor de ambos mundos

La estrategia más práctica para proyectos serios: **usar ambos, según el tipo
de tarea y sensibilidad del código**. **Reglas de asignación:**

### Modelo local (Ollama) para:

- Autocompletado durante el desarrollo diario.
- Refactors de código sensible que no puede salir de la máquina.
- Consultas sobre lógica de negocio proprietaria.
- Cualquier código que caiga bajo NDA o confidencialidad.
- Prototipos donde no querés gastar tokens.

### Modelo remoto (Claude/GPT/Gemini) para:

- Código público o de proyectos personales.
- Consultas conceptuales sin exponer código específico.
- Tareas complejas donde la calidad importa más.
- Debugging complicado que un modelo pequeño no puede resolver.
- Documentación general.

### Configurando ambos en Cline

Cline permite configurar múltiples perfiles. Podés tener:

| Perfil "local" | Perfil "cloud" |
| --- | --- |
| Apunta a Ollama con qwen2.5-coder. | Apunta a Anthropic con Claude Sonnet. |

Y **cambiar entre ellos con un click** según la tarea del momento. Ese cambio
consciente - antes de meter código sensible en el chat, verificar qué modelo
está seleccionado - es la disciplina que separa a profesionales cuidadosos de
la mayoría.

### Ejemplo aplicado al banco

Imaginate que tenés el banco de este manual funcionando en producción con
clientes reales. Tenés que hacer un refactor:

**Caso 1**: agregar un campo email_alternativo a PersonaFisica. Es un cambio
genérico, sin exponer datos.

- ➡ Modelo remoto está bien. Es rápido y de calidad alta.

**Caso 2**: optimizar el cálculo de intereses porque estás viendo lentitud en
producción. Necesitás pasarle datos reales de la tabla para que analice.

- ➡ Modelo local obligatorio. Esos datos no pueden salir.

**Caso 3**: entender por qué un test específico falla intermitentemente. Solo
involucra el código del test, no datos de clientes.

- ➡ Cualquiera de los dos, pero si el debugging es difícil, remoto para mejor
  calidad.

> **La regla mental:** Antes de pegar código o datos en un chat con un modelo
> IA, preguntate *"¿me sentiría cómodo si esto se hiciera público?"*. Si la
> respuesta es "no", modelo local.

## Buenas prácticas al usar agentes

Con los agentes IA hay una tentación fuerte de aceptar sus sugerencias sin
revisar. Es un error grave. Los agentes fallan de formas sutiles: código que
funciona en el caso obvio pero rompe en el borde, imports mal, versiones
incorrectas de librerías, lógica de negocio invertida.

### 1. Revisá cada diff

Antes de aceptar un cambio del agente, **leelo entero**. No aceptes ciego. Los
agentes escriben con confianza aunque estén equivocados. La responsabilidad
última del código es tuya.

### 2. Corré tests después de cada cambio

Si el proyecto tiene tests (como el banco después del capítulo 23), corré
python manage.py test después de cada modificación importante del agente. Si
algo se rompió, el agente lo ve y puede corregir. Sin tests, los bugs se
acumulan silenciosamente.

### 3. Commits pequeños y frecuentes

Cuando trabajás con un agente, commiteá seguido. Cada cambio significativo en
un commit propio. Si algo rompe algo, git log te muestra exactamente qué
cambio lo causó. Sin commits granulares, un bug puede volverse imposible de
rastrear.

Aider tiene esta filosofía por diseño - cada cambio del agente es un commit
automáticamente.

### 4. No delegues lo que no entendés

Si el agente te devuelve un patrón que no reconocés, **paralo y estudialo
antes de aceptarlo**. Copiar código que no entendés te vuelve dependiente del
agente y te bloquea cuando el agente falla.

Regla mental: *"si mañana no tengo IA, ¿puedo mantener este código?"*. Si no,
es momento de aprender.

### 5. Cuidado con las alucinaciones

Los modelos a veces **inventan** funciones, imports, API calls, opciones de
configuración que no existen. Se llama "alucinación" y es un problema real.

Ejemplos comunes:

- Inventar métodos del ORM (Cuenta.objects.reset_all() no existe pero suena
  razonable).
- Sugerir librerías con nombres levemente distintos (django-money cuando
  querías django-price-field).
- Poner opciones de settings que nunca existieron en Django.

Verificá siempre contra la documentación oficial antes de asumir que algo
existe.

### 6. Contexto explícito

Los agentes trabajan mejor con contexto explícito. En vez de:

```text
"arreglá el bug en la vista"
```

Preferí:

```text
"En banco/views.py, la vista transferir_desde_cuenta, cuando el monto es mayor al
saldo disponible, no está mostrando el mensaje de error correcto. Debería usar la
excepción SaldoInsuficienteError como en las otras vistas."
```

Cuanto más específico el prompt, mejor la respuesta. Los buenos prompts son un
skill que se practica.

### 7. Un agente no reemplaza aprender

Este es quizás el punto más importante para estudiantes. Los agentes son
excelentes acelerando tareas que ya sabés hacer. Son terribles cuando los usás
para saltearte el aprendizaje.

Si estás aprendiendo Django, resolver los ejercicios pidiéndole al agente que
los haga es contraproducente. El aprendizaje viene de la lucha, de trabar, de
mirar la documentación, de entender por qué algo falla. El agente te da la
respuesta sin el aprendizaje.

> **Regla para estudiantes:** Primero resolvé sin agente. Después usá el
> agente para comparar tu solución, entender alternativas, o refinar. En ese
> orden.

### 8. La conversación importa

Un agente moderno mantiene contexto en una conversación larga. Aprovechalo:

1. Empezá con contexto general del proyecto.
2. Pedile una tarea concreta.
3. Cuando te devuelva algo, no lo aceptes automáticamente - hacé preguntas:
   *"¿por qué elegiste este approach?"*, *"¿hay una forma más simple?"*,
   *"¿esto es compatible con Django 5.2?"*.
4. Iterá hasta llegar a algo que entiendas y aceptes.

La conversación es donde el agente muestra su valor real. Usarlo como caja
negra que te tira código es desperdiciar el 80% de su potencial.

## Aplicando agentes al proyecto del banco

Repasemos el manual entero pensando dónde los agentes hubieran acelerado el
trabajo y dónde no.

### Donde los agentes son excelentes

**Migración de POO a modelos Django (capítulo 17)**: dado el código Python del
capítulo 15, un agente puede traducirlo a modelos Django en minutos. Es una
tarea mecánica de mapeo. Los agentes son fantásticos en esto.

**Configuración del admin (capítulo 18)**: dados los modelos, un agente genera
ModelAdmin con list_display, search_fields, list_filter razonables. Ahorra
tiempo de escribir código repetitivo.

**Templates HTML/Bootstrap (capítulo 20)**: crear templates con Bootstrap es
tedioso. Un agente los genera rápido y consistente.

**Migración a Docker (capítulo 26)**: dados los requerimientos, un agente
puede generar Dockerfile y docker-compose.yml que funcionen. Después ajustás.

**Escribir tests (capítulo 23)**: dado el modelo CuentaAhorro, un agente puede
generar una batería de tests que cubren casos comunes. Vos revisás y ajustás.

**Donde los agentes son útiles pero requieren revisión**

**Diseño de POO (capítulos 10-14)**: un agente puede sugerir jerarquías, pero
el pensamiento arquitectural es tuyo. Si le pedís *"diseñá el sistema
bancario"*, va a proponer algo razonable, pero puede que no sea óptimo para tu
caso específico.

**Validaciones de dominio (validaciones.py)**: puede generar validaciones
estándar (formato DNI, CUIT), pero la validación del dígito verificador de
CUIT tenía sutilezas argentinas que un modelo genérico puede errar.

**Vistas con lógica de negocio compleja**: para vistas simples (CRUD básico),
los agentes son perfectos. Para vistas con lógica específica del banco
(transferencias con validación cruzada, permisos por titularidad), requieren
guía cuidadosa.

### Donde los agentes **NO** deberían usarse (para aprender)

**Los primeros capítulos (1-9)**: si estás aprendiendo Python, resolver los
ejercicios con un agente destruye el aprendizaje. Programación es una
habilidad que se construye con esfuerzo - no hay atajos.

**Ejercicios de teoría de conjuntos y POO**: entender por qué la herencia
funciona, cómo se relaciona con subconjuntos, qué es LSP - es pensamiento
matemático y arquitectural. Un agente puede responder qué es LSP, pero
entenderlo profundamente requiere trabajar con las ideas uno mismo.

**Debugging inicial**: cuando arrancás, aprender a leer un traceback y
encontrar el bug es una habilidad crítica. Pedirle a un agente que arregle el
bug sin entenderlo te deja incapaz cuando el agente no está disponible.

### La regla para estudiantes

| Etapa de aprendizaje | Etapa de trabajo profesional |
| --- | --- |
| Resolver sin agente. Usar agente solo para comparar soluciones, entender alternativas, refinar. | Usar agente productivamente. Aceleración masiva de tareas mecánicas. Focalizar tu tiempo humano en lo arquitectural y en los detalles críticos del negocio. |

Cuando pasás de una etapa a la otra depende de vos. Como referencia: cuando
podés escribir código del nivel del capítulo 15 (POO completo con SOLID) sin
ayuda, ya estás listo para incorporar agentes en tareas de framework como
Django.

## El costo real de los agentes remotos

Un tema práctico que muchos ignoran: **cuánto se gasta en tokens** al usar
agentes remotos.

Los proveedores cobran por millones de tokens. Precios aproximados (2026):

- Claude Sonnet: ~$3 USD por millón de tokens de entrada, ~$15 por millón de
  salida.
- Claude Opus: ~$15 USD por millón de entrada, ~$75 por millón de salida.
- GPT-5: rangos similares a Claude.

### ¿Qué implica en la práctica?

Una sesión típica de trabajo con Cline usando Claude Sonnet:

- Le pasás 5-10 archivos como contexto: ~20K tokens de entrada.
- Le pedís tres tareas iterativas: cada respuesta ~2K tokens de salida.
- Total sesión: ~50K entrada + 10K salida.
- **Costo**: ~$0.30 USD por sesión.

Trabajando así 4 sesiones por día, 5 días por semana:

- ~$6 USD por semana = ~$25 USD por mes.
- Con Claude Opus el costo sería 5x, ~$125/mes.
- Con Haiku, ~$3-5/mes.

### Optimizaciones:

- Usar el modelo adecuado para cada tarea (Haiku para simples, Sonnet para
  normales, Opus solo cuando es necesario).
- Reducir contexto: no pasar archivos que no son relevantes.
- Cachear respuestas: si vas a preguntar lo mismo dos veces, guardarlo la
  primera.

**Para desarrolladores profesionales**, $25-100/mes en modelos IA es una
inversión razonable si multiplican productividad. Para estudiantes o proyectos
personales, alternativas gratuitas son válidas:

- **Modelo local** (Ollama): $0.
- **OpenRouter con créditos free periódicos**.
- **Copilot for Students** (gratis con GitHub Education).
- **Claude Pro** ($20 USD/mes ilimitado hasta cuota razonable, más barato que
  API por uso intensivo).

## Un panorama de tres años a futuro

El campo de LLMs para código cambia trimestre a trimestre. Predecir con
precisión es imposible, pero podemos identificar tendencias probables:

**Modelos locales alcanzando paridad**: los modelos open source (Qwen,
DeepSeek, Llama) mejoran ~2-3x por año. En 2027-2028, un modelo local va a ser
comparable en calidad a un Claude Sonnet actual. La ventaja de privacidad va a
ser gratis en calidad también.

**Contextos más grandes**: en 2024 un contexto de 128K tokens era caro y raro.
En 2026, 1M tokens es común. En 2028, probablemente proyectos enteros de
decenas de megabytes van a caber en contexto único.

**Agentes más autónomos**: los agentes actuales requieren supervisión
(aprobar cada diff). Los agentes de 2027-2028 van a ejecutar tareas completas
semi-supervisadamente - *"agregá este feature al sistema, corré los tests, y
hacé un pull request cuando esté listo"* - y volver con el resultado
terminado.

**Especialización creciente**: modelos específicos para debugging, para
refactoring, para arquitectura, para tests, para migraciones. Cada uno mejor
que un generalista en su tarea.

**Integración más profunda en editores**: la separación entre "editor" y "IA"
se va a borrar. El código, el chat, la ejecución, el debugging, todo va a ser
una experiencia integrada.

**Regulaciones y controles**: es probable que aparezcan regulaciones sobre
datos que pueden procesarse en modelos remotos (especialmente en salud,
finanzas, gobierno). Los modelos locales van a ser una necesidad legal, no
solo una preferencia.

**Democratización de hardware**: chips especializados en IA (NPUs) integrados
en laptops estándar van a permitir correr modelos serios sin GPU dedicada. Los
Mac con chips M ya lo hacen, próximas generaciones de Intel/AMD también.

**Un mundo donde todo desarrollador usa agentes**: para 2028-2030, no usar
asistencia de IA para programar va a ser tan raro como no usar autocompletado
o linters hoy. La conversación va a ser sobre **cómo** usarlos bien, no si
usarlos.

## Reflexión: la habilidad que sí importa

Con toda esta ola de asistencia IA, aparece una pregunta natural: **¿tiene
sentido aprender a programar en profundidad si un agente puede escribir el
código?**

La respuesta corta: **sí, más que nunca**.

Los agentes son excelentes generando código plausible. Son mediocres
identificando cuándo su código está mal, cuándo el enfoque es incorrecto,
cuándo el diseño rompe algo importante que no es visible en el fragmento
actual. **Esa evaluación crítica es lo que un buen programador aporta.**

La habilidad valiosa en 2026 y hacia adelante no es *"escribir código"* - los
agentes lo hacen razonablemente bien. Es:

- **Diseñar sistemas**: pensar la arquitectura, elegir qué tecnologías usar,
  cómo dividir responsabilidades.
- **Evaluar código**: leer una sugerencia del agente y saber si está bien, si
  tiene sutiles bugs, si va a escalar.
- **Contextualizar**: entender el negocio, los usuarios, las restricciones. Un
  agente no sabe que tu banco necesita cumplir regulaciones locales
  específicas.
- **Debuggear**: cuando algo rompe, aislar la causa, entenderla, corregirla.
  Los agentes son mediocres en debugging profundo.
- **Comunicar**: explicar el sistema a otros humanos - compañeros, clientes,
  usuarios. Los agentes no reemplazan la comunicación.

**Ninguna de esas habilidades se aprende dejando que el agente escriba el
código por vos**. Se aprenden haciendo - como hicieron en este manual. Cada
ejercicio resuelto sin ayuda es un ladrillo de esas habilidades.

Los agentes son multiplicadores. Multiplican por 10 a un desarrollador
competente. **Multiplican por cero a alguien que no sabe programar** - porque
no puede evaluar lo que el agente le devuelve.

El manual les dio los fundamentos. Los agentes van a acelerar todo lo que
hagan a partir de ahora. Pero los fundamentos son suyos, y son intransferibles.

## Recomendaciones prácticas de cierre

Para incorporar agentes IA en tu trabajo, hoja de ruta pragmática:

### Etapa 1 - Familiarización (primera semana):

- Instalá Cline en VSCode.
- Conectalo a un modelo remoto (Claude Sonnet vía OpenRouter, o Claude Pro con
  Anthropic).
- Trabajá con proyectos personales o del manual. Aprendé el flujo del agente.
- Focalizá en tareas de aceleración: templates, tests estándar, refactors.

### Etapa 2 - Refinamiento (segunda semana en adelante):

- Configurá modelos por nivel: Haiku para autocompletado, Sonnet para lo
  normal, Opus para complejo.
- Aprendé a escribir prompts efectivos.
- Empezá a diferenciar dónde el agente aporta y dónde no.
- Instalá Ollama con Qwen Coder 7B o similar como respaldo.

### Etapa 3 - Uso profesional:

- Definí protocolos para código sensible: modelo local siempre.
- Integrá agentes en el flujo del equipo: convenciones de prompts,
  .clinerules, etc.
- Aprendé Aider para grandes refactors con git-first.
- Considerá Cursor si valorás UX pulida.

### Etapa 4 - Contribución al ecosistema:

- Compartí prompts útiles con la comunidad.
- Reportá alucinaciones o problemas a los proveedores.
- Si trabajás con datos muy sensibles, considerá alojar modelos locales en
  servidores dedicados de la empresa.

## Reflexiones

Terminaron un manual largo. Un año de contenido denso. Vale la pena parar y
mirar hacia atrás.

**Empezaron en el capítulo 1** con el ecosistema de Python, sin saber qué era
un intérprete. **Terminan en el capítulo 25** hablando de arquitecturas de
microservicios y machine learning. Ese salto no es trivial. Se hace paso a
paso, y no siempre se ve el progreso - hasta que mirás para atrás.

Algunas cosas para tener presentes:

1. **El aprendizaje no termina acá.** Un profesional serio sigue aprendiendo
   toda su vida. La tecnología cambia, los problemas cambian, las mejores
   prácticas cambian. Lo que aprendieron en el manual **no es el techo, es el
   piso**.
2. **Los fundamentos importan más que las herramientas.** Django, PostgreSQL,
   DRF - todas esas son herramientas específicas. Van a cambiar. Lo que no
   cambia son los fundamentos: pensamiento orientado a objetos, buenas
   prácticas de código, entender qué es un buen diseño. Esos fundamentos son
   transferibles a cualquier tecnología.
3. **El código legible vale más que el código clever.** En sus futuras
   carreras, van a leer código ajeno mucho más que a escribir el propio.
   Escriban pensando en la persona que va a leer su código en 6 meses -
   probablemente sean ustedes mismos y no van a recordar por qué escribieron
   lo que escribieron.
4. **Los bugs son parte del trabajo.** No son un signo de incompetencia. Los
   mejores desarrolladores del mundo escriben bugs todos los días. La
   habilidad no está en evitarlos, sino en **detectarlos rápido** (tests) y
   **corregirlos con precisión** (debugging metódico).
5. **La curiosidad se recompensa.** Cuando aparezca un concepto nuevo - async,
   GraphQL, containers, cualquier cosa - dedicarle un rato aunque no lo
   necesiten ese día. La gente que se sostiene en carreras técnicas largas es
   la que sigue teniendo hambre de entender cómo funcionan las cosas.
6. **Compartan lo que aprenden.** Escriban blogs, contesten preguntas en
   foros, ayuden a compañeros. Enseñar es la mejor forma de consolidar el
   aprendizaje propio. Y la comunidad Python es especialmente amigable con
   quienes contribuyen.
7. **El código es medio, no fin.** Al final del día, escribimos código para
   resolver problemas reales de personas reales. No para hacer arquitecturas
   impresionantes, no para usar la última tecnología de moda. **Lo que importa
   es que el sistema resuelva bien lo que se propuso resolver.** Todo lo demás
   es medios para ese fin.

## ¿Un cierre?

Con este capítulo termina el manual. Terminamos con el tema que va a definir
tu carrera como desarrollador de acá a los próximos años.

**Programar en 2026 es una actividad híbrida: humano + IA.**

El humano aporta juicio, contexto, diseño, comunicación. La IA aporta
velocidad, memoria, generación de código plausible, sugerencias. Los dos son
necesarios, ninguno es suficiente solo.

Los que se adapten a este nuevo modo van a ser 5-10x más productivos que en la
era pre-IA. Los que no se adapten van a quedar rezagados. Y los que confíen
ciegamente en la IA sin criterio propio van a producir código que se rompe
silenciosamente.

**La forma correcta de trabajar con agentes IA es tratándolos como colegas talentosos pero falibles.**

Escuchá sus sugerencias. Cuestionalas. Aprobá lo que entendés. Rechazá lo que
no. Aprendé de sus enfoques cuando son buenos. Corregí sus errores cuando los
ves.

Y sobre todo:

**nunca dejes de pensar por vos mismo.**

La habilidad de razonar sobre problemas de software es la habilidad humana más
valiosa que existe en esta industria. Los agentes son herramientas para
amplificar esa habilidad, no para reemplazarla.

**Ya no sos "un estudiante que están aprendiendo a programar".**

Sos un desarrollador capaz de construir sistemas web completos, deployarlos,
mantenerlos, y trabajar productivamente con las herramientas del estado del
arte.

Bienvenidos al oficio.

**Nos vemos donde el código nos lleve.**
