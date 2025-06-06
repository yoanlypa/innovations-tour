# innovations-tour
 **Documentación Completa de “Innovations Tours”**

Esta documentación describe en detalle la estructura, componentes y flujo de la aplicación Django “Innovations Tours”. Está escrita en español y cubre modelos, formularios, vistas, plantillas y JavaScript. Debería servir para que cualquier programador entienda el proyecto y pueda añadir o modificar funcionalidades sin equivocarse.

---

## **1\. Resumen y propósito**

“Innovations Tours” es una pequeña aplicación web para gestionar **pedidos de excursiones** (servicios), crear y editar esos pedidos, y asignarles “servicios” (cada servicio incluye excursión, número de pax, emisores, lugar de entrega y bono opcional). Hay dos roles principales:

* **Cliente registrado**: puede crear y editar sus propios pedidos, ver su lista en formato responsive (cards o tabla) y asignar servicios a los pedidos.

* **Staff (admin)**: ve todos los pedidos, puede filtrar, ordenar, cambiar estado vía AJAX, eliminar (individual o masivo) y crear/editar pedidos tanto en vista completa como por modal.

La aplicación está desplegada en Railway, con base de datos PostgreSQL y actualizaciones vía commit/push a GitHub.

---

## **2\. Estructura de carpetas (resumida)**

bash  
CopiarEditar  
`app/`  
`├── control_radioguias/       # Proyecto Django`  
`│   ├── settings.py`  
`│   ├── urls.py`  
`│   └── wsgi.py`  
`├── pedidos/                  # Aplicación principal`  
`│   ├── migrations/`  
`│   ├── static/`  
`│   │   └── pedidos/`  
`│   │       ├── css/`  
`│   │       │   ├── styles.css`  
`│   │       │   └── bootstrap.min.css (si se usa local)`  
`│   │       ├── js/`  
`│   │       │   ├── pedido_form.js`  
`│   │       │   └── edit.js (u otros)`  
`│   │       └── img/           # Imágenes estáticas`  
`│   ├── templates/`  
`│   │   └── pedidos/`  
`│   │       ├── base.html`  
`│   │       ├── base_blank.html`  
`│   │       ├── home.html`  
`│   │       ├── acceso.html`  
`│   │       ├── pedido_nuevo_cliente.html`  
`│   │       ├── pedido_nuevo_cliente_modal.html`  
`│   │       ├── _pedido_form.html`  
`│   │       ├── pedidos_mios.html`  
`│   │       ├── pedidos_lista.html`  
`│   │       ├── tareas.html`  
`│   │       └── …`  
`│   ├── models.py`  
`│   ├── forms.py`  
`│   ├── views.py`  
`│   ├── urls.py`  
`│   ├── serializers.py`  
`│   ├── templatetags/fechas.py`  
`│   └── admin.py`  
`├── manage.py`  
`└── README.md                  # (este documento)`

---

## **3\. Modelos (`pedidos/models.py`)**

A continuación se definen los modelos principales.

### **3.1. `RegistroCliente`**

* **Campos**:

  * `nombre_usuario` (CharField): nombre del usuario registrado.

  * `email` (EmailField)

* **Uso**: cada vez que un visitante se registra, se crea un `RegistroCliente` para llevar un registro en la tabla.

### **3.2. `Pedido`**

* **Campos**:

  * `usuario` (ForeignKey → User): enlaza el pedido con el usuario que lo creó.

  * `empresa` (CharField): nombre de la agencia o empresa cliente (p.ej. “TUI”).

  * `excursion` (CharField, opcional): nombre de la excursión general.

  * `fecha_inicio` (DateField): fecha de inicio del pedido.

  * `fecha_fin` (DateField, opcional): fecha de fin (si aplica).

  * `estado` (CharField con choices):

    1. `pendiente_pago`

    2. `pagado`

    3. `aprobado`

    4. `entregado`

    5. `recogido`

  * `lugar_entrega` (CharField, opcional)

  * `lugar_recogida` (CharField, opcional)

  * `notas` (TextField, opcional)

  * `fecha_creacion` (DateTimeField, auto\_now\_add=True)

* **Related name**:

  * En el `ForeignKey` de `Servicio` (abajo) debe definirse `related_name="servicios"`, para poder hacer `pedido.servicios.all()`.

* **Uso**:

  * Guarda cada pedido.

  * Los estados controlan el flujo de trabajo (cliente primero, luego staff).

### **3.3. `Servicio`**

* **Campos**:

  * `pedido` (ForeignKey → Pedido, on\_delete=CASCADE, related\_name="servicios")

  * `excursion` (CharField): nombre o descripción de la excursión específica.

  * `pax` (IntegerField): cantidad de pasajeros.

  * `emisores` (IntegerField): número de emisores o tickets.

  * `lugar_entrega` (CharField): lugar donde se entrega ese servicio.

  * `bono` (CharField, opcional): código/número de bono (puede quedar vacío).

* **Uso**:

  * Cada registro en `Servicio` representa un “sub-servicio” dentro de un pedido.

  * En la UI se muestran agrupados bajo cada pedido.

### **3.4. `Tarea`**

* **Campos**:

  * `titulo` (CharField)

  * `descripcion` (TextField)

  * `fecha_especifica` (DateField, opcional)

  * `fecha_creacion` (DateTimeField, auto\_now\_add=True)

  * `completada` (BooleanField, default=False)

* **Uso**:

  * Para la sección de “Tareas” únicamente visible al staff.

  * Permite crear/mostrar/editar/eliminar tareas y cambiar su estado via AJAX.

---

## **4\. Formularios (`pedidos/forms.py`)**

### **4.1. `CustomRegisterForm`**

* **Hereda** de `UserCreationForm`.

* Añade validación de email, nombres, contraseñas, etc.

* Al guardar:

  1. Crea un `User`.

  2. Crea un `RegistroCliente` con username/email.

### **4.2. `CustomLoginForm`**

* **Hereda** de `AuthenticationForm`.

* Se usa para login, con validación básica.

### **4.3. `PedidoFormCliente`**

* **Hereda** de `forms.ModelForm` apuntando a `Pedido`.

* **Campos sobrescritos**:

  * `fecha_inicio` \= `DateField` con `widget=DateInput(attrs={'type':'date','class':'form-control'})` y `input_formats=['%Y-%m-%d','%d/%m/%Y']`.

  * `fecha_fin` \= `DateField` (opcional), similar al anterior.

**Meta.fields**:

 python  
CopiarEditar  
`fields = [`  
  `'fecha_inicio','fecha_fin',`  
  `'empresa','excursion','estado',`  
  `'lugar_entrega','lugar_recogida','notas'`  
`]`

*   
* **Validación**:

  * Override de `clean_fecha_fin()` (o `clean()`) para asegurar que `fecha_fin ≥ fecha_inicio`.

### **4.4. `ServicioForm` \+ `ServicioFormSet`**

* **`ServicioForm`**: `forms.ModelForm` para `Servicio`, con widgets:

  * `excursion` → `TextInput(attrs={'class':'form-control'})`

  * `pax` → `NumberInput(attrs={'class':'form-control','min':1})`

  * `emisores` → `NumberInput(attrs={'class':'form-control','min':1})`

  * `lugar_entrega` → `TextInput(attrs={'class':'form-control'})`

  * `bono` → `TextInput(attrs={'class':'form-control'})`

**`ServicioFormSet`**:

 python  
CopiarEditar  
`from django.forms import inlineformset_factory`  
`ServicioFormSet = inlineformset_factory(`  
    `Pedido,`  
    `Servicio,`  
    `form=ServicioForm,`  
    `extra=1,`  
    `can_delete=True`  
`)`

*   
  * **NO** va `prefix` aquí. Ese prefijo se añade en la vista.

### **4.5. `PedidoForm` (para staff)**

* Mismo esquema que `PedidoFormCliente`, pero puede incluir más campos (por ejemplo, asignar a otros usuarios o campos adicionales).

* Debe aceptar `input_formats` idénticos en fechas.

### **4.6. `TareaForm`**

* ModelForm para `Tarea` con:

  * `titulo`

  * `descripcion`

  * `fecha_especifica`

  * `completada`

* Se usa en las vistas CRUD de tareas.

---

## **5\. Vistas (`pedidos/views.py`)**

### **5.1. HomeView (`TemplateView`)**

* **URL**: `/`

* **Lógica**:

  * Si el usuario está autenticado:

    * Si es staff → redirige a `pedidos_lista_view`.

    * Si es cliente → redirige a `pedidos_mios_view`.

  * Si no, muestra `home.html` (landing pública con información general).

### **5.2. Autenticación (`acceso_view`, `logout_view`)**

* **`acceso_view`**:

  * Instancia `CustomLoginForm` y `CustomRegisterForm`.

  * Detecta `mode = request.POST.get('mode','login')`.

    * **login**: valida credenciales; si es staff → `pedidos_lista`; si no → `mis_pedidos`.

    * **register**: valida `register_form`→ guarda usuario \+ `RegistroCliente` \+ `login()` \+ redirect a `mis_pedidos`.

    * **reset**: pendiente lógica “envío de enlace de recuperación”; sólo muestra mensaje.

  * Renderiza `acceso.html` con:

    * `login_form`, `register_form`, `mode`.

* **`logout_view`**:

  * `logout(request)` \+ `redirect('pedidos:acceso')`.

### **5.3. CRUD de Tareas (solo staff)**

* **`TareaListView`** (ListView):

  * Solo staff (`UserPassesTestMixin`).

  * Template: `tareas.html`.

  * Preﬁcha listado ordenado por `fecha_creacion`.

* **`TareaCreateView`, `TareaUpdateView`, `TareaDeleteView`**:

  * CRUD normal con formularios.

  * `TareaCreateView` maneja AJAX: si `X-Requested-With='XMLHttpRequest'`, devuelve JSON con datos de tarea creada.

* **`cambiar_estado_tarea(request, tarea_id)`**:

  * POST AJAX que invierte el booleano `completada` en un `Tarea` y devuelve JSON `{completada, tarea_id}`.

  * URL: `/tareas/cambiar-estado/<tarea_id>/`.

### **5.4. Listar / Crear / Editar / Eliminar Pedidos**

#### **5.4.1. `pedidos_mios_view` (clientes)**

* **URL**: `/mis-pedidos/`

* **Decorador**: `@login_required`

**Query**:

 python  
CopiarEditar  
`pedidos = (Pedido.objects`  
           `.filter(usuario=request.user)`  
           `.prefetch_related('servicios')`  
           `.order_by('-fecha_inicio'))`

*   
* **Renderiza**: `pedidos_mios.html`.

* **Contexto**: `{'pedidos': pedidos}`.

#### **5.4.2. `pedido_nuevo_cliente_view`**

* **URL**: `/mis-pedidos/nuevo/`

* **Decorador**: `@login_required`

* **Lógica**:

  1. Detecta `embed = request.GET.get('embed')=='1' or request.POST.get('embed')=='1'`.

Instancia:

 python  
CopiarEditar  
`form = PedidoFormCliente(request.POST or None)`  
`servicio_formset = ServicioFormSet(request.POST or None, prefix='servicio')`

2.   
   3. Si `POST` y ambos válidos:

      * `pedido = form.save(commit=False); pedido.usuario = request.user; pedido.save()`

Reinstancia el formset con `instance=pedido`:

 python  
CopiarEditar  
`servicio_formset = ServicioFormSet(request.POST, instance=pedido, prefix='servicio')`  
`servicio_formset.save()`

*   
  * Si `embed` → `return HttpResponse("<script>window.parent.location.reload();</script>")`

    * Si no `embed`, `messages.success(...)` \+ `redirect('pedidos:mis_pedidos')`.

  4. Elige plantilla:

     * Si `embed` → `pedido_nuevo_cliente_modal.html`

     * Si no → `pedido_nuevo_cliente.html`

  5. Contexto: `{'form': form, 'formset': servicio_formset, 'es_edicion': False, 'embed': embed}`.

#### **5.4.3. `pedido_editar_cliente_view`**

* **URL**: `/mis-pedidos/editar/<pk>/`

* **Decorador**: `@login_required`

* **Lógica similar a “nuevo”**:

  1. Obtiene `pedido = get_object_or_404(Pedido, pk=pk)` y verifica `pedido.usuario == request.user`; si no, `raise Http404()`.

Instancia:

 python  
CopiarEditar  
`form = PedidoFormCliente(request.POST or None, instance=pedido)`  
`servicio_formset = ServicioFormSet(request.POST or None, instance=pedido, prefix='servicio')`

2.   
   3. Si `POST` y ambos válidos:

      * Guarda el `form` y luego `servicio_formset.save()`.

      * Si `embed` → cierra modal y recarga padre (igual que en “nuevo”).

      * Si no `embed`, `messages.success(...)` \+ `redirect('pedidos:mis_pedidos')`.

   4. Renderiza siempre en `pedidos/pedido_nuevo_cliente.html` (mismo template que “nuevo”), con `es_edicion=True`.

#### **5.4.4. `pedidos_lista_view` (staff)**

* **URL**: `/pedidos/`

* **Decorador**: `@staff_member_required`

**Query**:

 python  
CopiarEditar  
`pedidos = (Pedido.objects`  
           `.all()`  
           `.prefetch_related('servicios')`  
           `.order_by('-fecha_inicio'))`

*   
* **Renderiza**: `pedidos_lista.html`.

* **Contexto**: `{'pedidos': pedidos}`.

#### **5.4.5. Eliminación individual y masiva**

* **Eliminar individual**:

  * En plantilla existe un `<form method="post" action="{% url 'pedidos:pedido_eliminar' p.pk %}">`.

  * Vista `pedido_eliminar(request, pk)` (no mostrado aquí) hace `get_object_or_404` y `pedido.delete()`, `redirect('pedidos:pedidos_lista')`.

* **Eliminar masivo**:

  * Form principal `<form id="mass-delete-form" method="post" action="{% url 'pedidos:pedido_eliminar_masivo' %}">` con checkboxes `name="selected_ids" value="{{ p.pk }}"`.

  * Vista `pedido_eliminar_masivo(request)` lee `ids = request.POST.getlist('selected_ids')`, hace `Pedido.objects.filter(pk__in=ids).delete()`, y redirect.

#### **5.4.6. Cambiar estado vía AJAX (staff)**

Botones en la tabla/card:

 django  
CopiarEditar  
`<button class="btn btn-estado"`  
        `data-pk="{{ p.pk }}"`  
        `data-url="{% url 'pedidos:cambiar_estado' p.pk %}">`  
  `{{ p.get_estado_display }}`  
`</button>`

*   
* **Vista** `cambiar_estado(request, pk)` (POST AJAX):

  1. Obtiene el `pedido = get_object_or_404(Pedido, pk=pk)`.

  2. Avanza al siguiente estado en lista predefinida o altera el valor (según lógica).

  3. `pedido.save()`.

Devuelve JSON con:

 json  
CopiarEditar  
`{`  
  `"display": pedido.get_estado_display,`  
  `"badge_class": "<clase CSS según estado>"`  
`}`

4.   
* El JavaScript captura el click, muestra `sweetalert2` confirmando, lanza `fetch(url,{method:'POST', headers:{'X-CSRFToken':csrftoken}})`. Al recibir la respuesta, actualiza `this.textContent` y `this.className`.

---

## **6\. URLs (`pedidos/urls.py`)**

python  
CopiarEditar  
`from django.urls import path`  
`from . import views`

`app_name = 'pedidos'`

`urlpatterns = [`  
    `# Home`  
    `path('', views.HomeView.as_view(), name='home'),`

    `# Autenticación`  
    `path('acceso/', views.acceso_view, name='acceso'),`  
    `path('logout/', views.logout_view, name='logout'),`

    `# Pedidos – cliente`  
    `path('mis-pedidos/', views.pedidos_mios_view, name='mis_pedidos'),`  
    `path('mis-pedidos/nuevo/', views.pedido_nuevo_cliente_view, name='pedido_nuevo_cliente'),`  
    `path('mis-pedidos/editar/<int:pk>/', views.pedido_editar_cliente_view, name='pedido_editar_cliente'),`  
    `path('mis-pedidos/eliminar/<int:pk>/', views.pedido_eliminar_cliente_view, name='pedido_eliminar_cliente'),`  
    `path('mis-pedidos/eliminar-masivo/', views.pedido_eliminar_masivo, name='pedido_eliminar_masivo'),`

    `# Pedidos – staff`  
    `path('pedidos/', views.pedidos_lista_view, name='pedidos_lista'),`  
    `path('pedidos/nuevo/', views.pedido_nuevo_view, name='pedido_nuevo'),`  
    `path('pedidos/editar/<int:pk>/', views.pedido_editar_view, name='pedido_editar'),`  
    `path('pedidos/eliminar/<int:pk>/', views.pedido_eliminar_view, name='pedido_eliminar'),`  
    `path('pedidos/eliminar-masivo/', views.pedido_eliminar_masivo, name='pedido_eliminar_masivo'),`

    `# AJAX: cargar datos (staff)`  
    `path('pedidos/cargar-datos/', views.cargar_datos_pedido, name='cargar_datos_pedido'),`  
    `# AJAX: cambiar estado`  
    `path('pedidos/cambiar-estado/<int:pk>/', views.cambiar_estado_pedido, name='cambiar_estado'),`

    `# Tareas (staff)`  
    `path('tareas/', views.TareaListView.as_view(), name='tareas'),`  
    `path('tareas/nuevo/', views.TareaCreateView.as_view(), name='tarea_nueva'),`  
    `path('tareas/editar/<int:pk>/', views.TareaUpdateView.as_view(), name='tarea_editar'),`  
    `path('tareas/eliminar/<int:pk>/', views.TareaDeleteView.as_view(), name='tarea_eliminar'),`  
    `path('tareas/cambiar-estado/<int:tarea_id>/', views.cambiar_estado_tarea, name='cambiar_estado_tarea'),`  
`]`

⚠️ Asegúrate de que los nombres en `name='…'` coincidan exactamente con los que usas en las plantillas.

---

## **7\. Plantillas (HTML)**

### **7.1. Base global: `base.html`**

* Contiene `<head>` con:

  * `<meta charset="utf-8">`

  * `<meta name="viewport" content="width=device-width, initial-scale=1">`

  * Carga de **Bootstrap CSS/JS** (v5.3), jQuery, Flatpickr CSS, SweetAlert2, DataTables CSS/JS si conviene.

  * Carga de `{% static 'pedidos/css/styles.css' %}`.

  * Bloques:

    * `{% block title %}` – Título página.

    * `{% block styles %}` – CSS adicionales.

    * `{% block content %}` – Contenido principal.

    * `{% block scripts %}` – JS adicionales (al pie).

### **7.2. Base minimalista: `base_blank.html`**

* Igual a `base.html` pero sin `<nav>` ni footer.

* Se usa para iframes de creación/edición (modal embed).

* Define bloque `content` y `scripts`.

### **7.3. `acceso.html` (login/registro/reset)**

* Extiende `base.html`.

* Dibuja un contenedor central con fondo degradado.

* Tarjeta centrada (`.form-card`) con:

  * Si `mode=='login'`: muestra `CustomLoginForm`.

  * Si `mode=='register'`: muestra `CustomRegisterForm`.

  * Si `mode=='reset'`: muestra solo un input de email para reset.

* JavaScript: función `cambiarModo(modo)` crea un `<form hidden>` que setea `mode` y hace `submit()` para cambiar entre “login”, “register” o “reset” sin recargar la página.

### **7.4. `home.html`**

* Landing pública informativa.

* Botón o link a “Iniciar Sesión / Registro”.

### **7.5. Parciales de pedido:**

#### **7.5.1. `_pedido_form.html`**

* Se incluye dentro del `<form>` padre.

* Muestra:

  1. Campos de **fecha\_inicio** y **fecha\_fin** (dos columnas en desktop).

  2. Cliente y excursión y estado (tres columnas).

  3. Lugar de entrega / recogida (dos columnas).

  4. Notas (textarea).

  5. Sección **Servicios**:

     * `{{ formset.management_form }}` (inputs ocultos `servicio-TOTAL_FORMS`, etc.).

     * `div#servicios-container` donde en cada iteración (`{% for sf in formset %}`) se dibuja una “card” para el formulario de un servicio:

       * Campos: `sf.excursion`, `sf.pax`, `sf.emisores`, `sf.lugar_entrega`, `sf.bono`.

       * Un botón `btn-close.eliminar-servicio` que marca el `DELETE` y oculta la card.

     * Un botón `#add-servicio` que, vía JS, añade dinámicamente una nueva card e incrementa `servicio-TOTAL_FORMS`.

* No contiene etiquetas `<form>`, `<html>` ni `<body>`.

#### **7.5.2. `pedido_nuevo_cliente.html`**

* Extiende `base_blank.html`.

* Contiene el contenedor centrado con `.card` y, dentro, abre `<form id="pedido-form">`:

  1. `{% csrf_token %}`

  2. `<input type="hidden" name="embed" value="0">` (no modo embed).

  3. `{{ form.as_p }}` (campos principales de pedido).

  4. `{% include "_pedido_form.html" %}`.

  5. Botón único “Guardar pedido”.

* Javascript: al final se la carga `pedido_form.js`.

#### **7.5.3. `pedido_nuevo_cliente_modal.html`**

* Igual que la anterior, pero:

  * El `<form>` lleva `<input type="hidden" name="embed" value="1">`.

  * No necesita contenedor `.card` tan amplio; puede tener `p-4`.

  * Se carga dentro de un `<iframe>`.

#### **7.5.4. `pedidos_mios.html` (clientes)**

* Extiende `base.html`.

* Botón “+” (FAB) para abrir `#modalNuevoPedido`.

* Modal `#modalNuevoPedido`: contiene un `<iframe src="{% url 'pedidos:pedido_nuevo_cliente' %}?embed=1">`.

* Si el usuario **no tiene pedidos**, muestra mensaje y botón “Crear mi primer pedido”.

* Si hay pedidos:

  * Muestra **cards** en móvil (`.d-block .d-md-none`):

    * Tarjetas en fila única con detalles básicos y botón “Editar” (abre modal).

  * Muestra **tabla** en desktop (`.d-none .d-md-block`) con columnas:

    * Checkbox de selección, Fecha inicio, Fecha fin, Empresa, Excursión, Entrega, Recogida, Maletas (hoy: servicios), Estado, Notas, Editar, Eliminar.

Se inicializa DataTables para ordenar/buscar/paginación:

 js  
CopiarEditar  
`$('#tabla-pedidos').DataTable({`  
  `order: [[1, 'desc']],`  
  `dom: 'Bfrtip',`  
  `buttons: [ … ],`  
  `columnDefs: [{ orderable:false, targets:[0,-1] }]`  
`});`

*   
  * Filtros personalizados:

    * Dropdown `#state-filter` filtra la columna “Estado”.

      * Input `#search-box` filtra globalmente.

    * Acciones de “Eliminar seleccionados” y “Cambiar estado” en bulk (usando AJAX y SweetAlert2 para confirmación).

* Cada fila de la tabla incluye:

  * Checkbox `<input class="select-checkbox">`.

  * Botón `<button class="btn-estado" data-url="{% url 'pedidos:cambiar_estado' p.pk %}">`.

    * Usado por JS para cambiar estado vía AJAX con confirmación SweetAlert2.

  * Botón “Editar” abre modal `#modalEditarPedido{{ p.id }}` con un `<iframe>` a `/mis-pedidos/editar/{{ p.id }}?embed=1`.

  * Botón “Eliminar” dispara el form oculto que apunta a la vista de eliminación individual.

#### **7.5.5. `pedidos_lista.html` (staff)**

* Muy similar a `pedidos_mios.html` pero:

  * Solo se muestra si `user.is_staff`; si no, alerta de “No tienes permiso”.

  * NO hay cards para móvil (ya que staff suele usar desktop), pero puede heredarse patrón responsive:

    * Se incluye un **FAB** de “+” para abrir modal de creación (rise a `/pedidos/nuevo?embed=1`).

    * Tabla con checkboxes, filtros, DataTables, botones AJAX de “Cambiar estado” y “Eliminar seleccionado(s)”.

  * Cada fila muestra:

    * Checkbox de selección

    * Fecha Inicio, Fecha Fin, Empresa, Excursión, Lugar Entrega, Lugar Recogida, **Servicios** (lista breve dentro de `<td>`), Estado (con badge CSS), Notas (con tooltip), Editar (link o modal), Eliminar.

#### **7.5.6. `tareas.html`**

* Extiende `base.html`.

* Botón “+” en esquina para abrir modal “Nueva Tarea”.

* Modal conteniendo `<form id="formNuevaTarea" action="{% url 'pedidos:tarea_nueva' %}">` con campos de tarea.

* Agrupa tareas por fecha (`{% regroup tareas by fecha_especifica|date:"d/m/Y" as grouped_tareas %}`).

* Cada grupo es una `<div class="card">` con cabecera “Fecha: 22/05/2025” y listado de tareas.

* Cada tarea tiene un botón con clase `.btn-estado` que, al hacer click, dispara AJAX a `/tareas/cambiar-estado/{{ tarea.id }}/` y actualiza el texto y la clase del botón según `completada`.

---

## **8\. JavaScript y comportamiento en cliente**

### **8.1. `pedido_form.js` (static/pedidos/js/pedido\_form.js)**

* Se ejecuta en el `DOMContentLoaded`.

**Inicializa Flatpickr** en los `<input id="id_fecha_inicio">` y `<input id="id_fecha_fin">`:

 js  
CopiarEditar  
`flatpickr(el, {`  
  `altInput: true,`  
  `altFormat: 'd/m/Y',`  
  `dateFormat: 'Y-m-d',`  
  `allowInput: true`  
`});`

*   
  * Con `altInput=true` el usuario ve `dd/mm/yyyy` pero el `value` real es `YYYY-MM-DD`.

* **Autofocus** en el primer campo de texto o select de formulario.

* **Spinner al enviar**: al submit, desactiva el botón y muestra `<span class="spinner-border"> Guardando…`.

* **Servicios dinámicos**:

  * Obtiene `cont = document.getElementById('servicios-container')` y `total = document.getElementById('id_servicio-TOTAL_FORMS')`.

  * `addBtn = document.getElementById('add-servicio')`.

  * Plantilla en JS para cada card de servicio (cinco campos alineados en desktop).

  * Al “click” en “+ Añadir servicio”:

    * Lee `idx = parseInt(total.value)`.

    * Inserta HTML en `cont.insertAdjacentHTML('beforeend', template(idx))`.

    * Suma `total.value = idx+1`.

  * En el contenedor escucha clicks en `.eliminar-servicio`:

    * Marca el checkbox `name="servicio-<idx>-DELETE"` con `.checked = true`.

    * Oculta la card con `card.style.display='none'`.

* **Cierre del modal embed**:

  * No lo maneja JS directo; la vista retorna un `<script>window.parent.location.reload()</script>` que el navegador ejecuta dentro del iframe.

### **8.2. JS en “Mis Pedidos” y “Pedidos Lista”**

* **DataTables**:

  * Se inicializa `$('#tabla-pedidos').DataTable({...})` con:

    1. `order: [[1,'desc']]` (orden por fecha inicio desc).

    2. `buttons`: “Eliminar seleccionados” y “Cambiar estado” con submenú.

    3. `columnDefs: { orderable:false, targets:[0,-1] }` para no ordenar checkbox ni acciones.

* **Filtros manuales**:

  * `$('#state-filter').on('change', …)`: filtra la columna “Estado”.

  * `$('#search-box').on('keyup', table.search(...).draw())`.

* **Checkbox “Seleccionar todos”**:

  * Al click en `#select-all`: marca/desmarca todas las `.select-checkbox`.

* **Bulk Delete**:

  * Botón “Eliminar seleccionados” dispara `bulkAction('eliminar')`:

    1. Si no hay seleccionados → alert(“Selecciona primero.”)

    2. Si confirma → `$.post("/pedidos/bulk-delete/", {ids, csrfmiddlewaretoken})` → recarga página.

* **Bulk Change Estado**:

  * El usuario abre el dropdown “Cambiar estado” y elige una opción:

    1. Llama `bulkAction('aprobado')`, por ejemplo.

    2. Muestra `Swal.fire({title: ¿Cambiar a “aprobado”?})`; si confirma → `ajaxBulk("/pedidos/bulk-change-estado/", {ids, estado:action})` → recarga.

* **Cambio de estado individual**:

  * Cada botón `.btn-estado` tiene `data-url="{% url 'pedidos:cambiar_estado' p.pk %}"`.

  * Al click:

    1. `event.preventDefault()`

    2. Muestra un `Swal.fire({confirmButton, cancelButton, texto Viejo})`.

    3. Si confirma → `fetch(data-url, {method:'POST', headers:{'X-CSRFToken':csrftoken}})`.

    4. Al recibir JSON `{display, badge_class}` actualiza `this.textContent` y `this.className`.

### **8.3. Flatpickr y localización**

* Se carga `flatpickr/dist/l10n/es.js` en `base_blank.html` (o donde esté).

* Inicializa con `flatpickr.localize(flatpickr.l10ns.es)` si existe.

### **8.4. SweetAlert2**

* Se utiliza para confirmaciones estilizadas:

  * Cambio de estado individual o massivo.

  * Bulk change estado en staff.

---

## **9\. Flujo general de uso**

1. **Inicio / Home**:

   * Usuario no autenticado ve `home.html` con información de la empresa.

   * Click en “Iniciar sesión” → va a `/acceso/`.

2. **Acceso**:

   * Si elige “Registro”, rellena datos, contraseña, crea cuenta.

   * Si elige “Login”, ingresa credenciales.

   * Después de login, se redirige:

     * Staff → `/pedidos/` (lista de todos los pedidos).

     * Cliente → `/mis-pedidos/` (sus pedidos).

3. **Cliente → `/mis-pedidos/`**:

   * Panel responsive:

     * Móvil → cards.

     * Desktop → tabla con DataTables, filtros y acciones.

   * Botón “+” abre modal para crear nuevo pedido (`?embed=1`).

   * Cada pedido:

     * Muestra servicios guardados.

     * Botón “Editar” abre modal de edición.

     * Botón “Eliminar” borra con confirm.

   * Al guardar/editar:

     * Se envía con `embed=1` → vista devuelve `<script>window.parent.location.reload()</script>`.

     * El iframe en la modal ejecuta este script → cierra modal y recarga `/mis-pedidos/`.

4. **Staff → `/pedidos/`**:

   * Panel similar a clientes (cards opcional, tabla principal):

     * Puede ver pedidos de todos.

     * Filtros de estado, búsqueda, orden.

     * Bulk actions: eliminar, cambiar estado.

     * Botones “Editar” abren modal con iframe a `/pedidos/editar/<pk>?embed=1`.

     * Botón “+” abre modal para crear pedido como staff.

   * AJAX:

     * Cambiar estado individual con confirm SweetAlert2 → recibe JSON, actualiza botón.

   * Bulk delete y bulk change estado via AJAX \+ recarga.

5. **Tareas** (staff) → `/tareas/`:

   * Panel de tareas agrupadas por fecha.

   * Botón “+” abre modal con formulario para crear nueva tarea.

   * Al guardarla, se inserta vía AJAX en la lista (o se recarga la vista).

   * Botones “Realizada”/“Pendiente” invierten estado vía AJAX y actualizan la UI en línea.

---

## **10\. Consideraciones técnicas**

* **Zona horaria**: Django está en “USE\_TZ \= True”. Por eso se recomendó cambiar `DateTimeField` a `DateField` para evitar “naive datetime” warnings.

* **Prefetch\_related**: en las vistas de lista es importante usar `.prefetch_related('servicios')` (mismo `related_name` del modelo) para evitar N+1.

* **CSRF**: todos los formularios (`<form method="POST">`) llevan `{% csrf_token %}`. En peticiones AJAX se envía el header `X-CSRFToken`.

* **Dependencias**:

  * Django 4.x

  * Python 3.12

  * Bootstrap 5.3

  * jQuery 3.6.0

  * Flatpickr \+ locale ES

  * SweetAlert2

  * DataTables (+ Buttons)

* **Archivos estáticos**:

  * `static/pedidos/css/styles.css`: estilos propios (colores de marca, espaciados, badges, etc.).

  * `static/pedidos/js/pedido_form.js`: inicialización de Flatpickr, lógica de servicios dinámicos y spinner.

  * `static/pedidos/js/edit.js`: (puede contener lógica de edición de pedidos si se usa).

---

## **11\. Índice rápido de archivos clave**

| Archivo | Descripción |
| ----- | ----- |
| `models.py` | Define `Pedido`, `Servicio`, `RegistroCliente`, `Tarea`, etc. |
| `forms.py` | `PedidoFormCliente`, `ServicioForm`, `ServicioFormSet`, `TareaForm` |
| `views.py` | Lógica de control: CRUD pedidos (cliente/staff), tareas, auth. |
| `urls.py` | Rutas de la aplicación con nombres (`name='…'`). |
| `templates/pedidos/base.html` | Layout principal con `<head>`, CSS/JS globales y bloques. |
| `templates/pedidos/base_blank.html` | Layout minimal para iframes (modal embed). |
| `templates/pedidos/acceso.html` | Login/Registro/Reset. |
| `templates/pedidos/home.html` | Landing pública. |
| `templates/pedidos/_pedido_form.html` | Parcial para los campos de “Servicios” dentro del form. |
| `templates/pedidos/pedido_nuevo_cliente.html` | Página completa de creación/edición para cliente (sin modal). |
| `templates/pedidos/pedido_nuevo_cliente_modal.html` | Mismo form, pero para modal iframe (solo HTML del form). |
| `templates/pedidos/pedidos_mios.html` | Lista de pedidos cliente (cards \+ tabla). |
| `templates/pedidos/pedidos_lista.html` | Lista de pedidos staff (tabla con bulk actions). |
| `templates/pedidos/tareas.html` | Panel de tareas del staff. |
| `static/pedidos/css/styles.css` | Estilos personalizados: temas de color, badges, margenes. |
| `static/pedidos/js/pedido_form.js` | Flatpickr \+ lógica de formset de servicios \+ spinner. |
| `static/pedidos/js/edit.js` | (Opcional) comportamientos extra de edición. |
| `admin.py` | Configuración en Django Admin (list\_display, actions masivas). |

---

## **12\. Flujo al agregar código nuevo**

1. **Modelos**: si añades un nuevo campo a `Pedido` o `Servicio`, crea y corre migraciones (`makemigrations`, `migrate`).

2. **Forms**: actualiza o crea un `ModelForm` que incluya el nuevo campo, definiendo `widget=…` si es fecha u otro tipo especial.

3. **Views**:

   * Si el campo va en pedidos cliente → modifica `PedidoFormCliente` y las vistas “nuevo”/“editar” para incluirlo.

   * Si el campo va en servicios → modifica `ServicioForm` y el formset, y revisa el parcial para acomodarlo (en `_pedido_form.html`).

4. **Templates**:

   * Actualiza el parcial `_pedido_form.html` para desplegar el nuevo campo dentro del bloque de servicios o pedidos.

   * Si el nuevo campo forma parte de la tabla/card, modifica `pedidos_mios.html` y `pedidos_lista.html`.

   * Asegúrate de mantener dentro del `<form>` padre solo un submit y poner el `management_form`.

5. **JavaScript**:

   * Si agregas campos de fecha nuevos, inicialízalos en `pedido_form.js`.

   * Si añades lógica de confirmaciones o AJAX, integra en los bloques `$(document).ready()` o `DOMContentLoaded`.

6. **Routes/URLs**:

   * Si creas nuevas vistas, registra las rutas en `pedidos/urls.py` y dales un `name='…'` consistente.

   * Usa `{% url 'pedidos:…' %}` en las plantillas siempre que llames a esas vistas.

7. **Pruebas**:

   * Prueba creación, edición, eliminación de pedidos y servicios tanto en modo normal como modal (`embed=1`).

   * Verifica que el modal cierra con `<script>window.parent.location.reload();</script>` en el iframe.

   * Asegúrate de que el DataTables se recarga tras crear o editar un pedido.

   * Al cambiar el estado vía AJAX, revisa la consola para errores.

---

## **13\. Buenas prácticas y consejos**

1. **Un solo `<form>` por página/iframe**: nunca anides formularios ni dupliques `<button type="submit">`.

2. **Siempre incluir** `{{ formset.management_form }}` dentro del formulario principal antes de iterar los formsets.

3. **Usar `altInput` en Flatpickr** para separar la vista del valor real que envía Django (`YYYY-MM-DD`).

4. **Evitar scripts “focus/blur”** que conviertan manualmente fechas, pues pueden chocar con Flatpickr.

5. **`related_name` en ForeignKey**: especifica siempre `related_name` en `Servicio.pedido` para poder usar `.prefetch_related('servicios')`.

6. **Manejar `embed=1` tanto en GET como en POST** en las vistas de creación/edición para que el iframe cierre y recargue.

7. **Mantén separados** los bloques de CSS/JS en `base.html` y añade `{{ block.super }}` solo en plantillas hijas (no en la base).

8. **Reutiliza parciales** (`_pedido_form.html`) para evitar duplicar markup: si cambias un campo, solo editas el parcial.

9. **Nombres de rutas coherentes**: p. ej. `pedido_nuevo_cliente`, `pedido_editar_cliente`, `pedidos_lista`, `cambiar_estado`, etc.

10. **Documenta cada función compleja** con un comentario breve al inicio de la vista o método.

---

## **14\. Resumen rápido de cada archivo**

### **`models.py`**

python  
CopiarEditar  
`from django.db import models`  
`from django.contrib.auth.models import User`

`class RegistroCliente(models.Model):`  
    `nombre_usuario = models.CharField(max_length=150)`  
    `email = models.EmailField()`

`class Pedido(models.Model):`  
    `usuario = models.ForeignKey(User, on_delete=models.CASCADE)`  
    `empresa = models.CharField(max_length=150)`  
    `excursion = models.CharField(max_length=150, blank=True)`  
    `fecha_inicio = models.DateField()`  
    `fecha_fin = models.DateField(blank=True, null=True)`  
    `ESTADOS = [`  
        `('pendiente_pago','Pendiente de pago'),`  
        `('pagado','Pagado'),`  
        `('aprobado','Aprobado'),`  
        `('entregado','Entregado'),`  
        `('recogido','Recogido'),`  
    `]`  
    `estado = models.CharField(max_length=20, choices=ESTADOS, default='pagado')`  
    `lugar_entrega = models.CharField(max_length=150, blank=True)`  
    `lugar_recogida = models.CharField(max_length=150, blank=True)`  
    `notas = models.TextField(blank=True)`  
    `fecha_creacion = models.DateTimeField(auto_now_add=True)`

`class Servicio(models.Model):`  
    `pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='servicios')`  
    `excursion = models.CharField(max_length=150)`  
    `pax = models.PositiveIntegerField()`  
    `emisores = models.PositiveIntegerField()`  
    `lugar_entrega = models.CharField(max_length=150, blank=True)`  
    `bono = models.CharField(max_length=100, blank=True)`

`class Tarea(models.Model):`  
    `titulo = models.CharField(max_length=150)`  
    `descripcion = models.TextField(blank=True)`  
    `fecha_especifica = models.DateField(blank=True, null=True)`  
    `fecha_creacion = models.DateTimeField(auto_now_add=True)`  
    `completada = models.BooleanField(default=False)`

---

### **`forms.py`**

python  
CopiarEditar  
`from django import forms`  
`from django.forms import inlineformset_factory`  
`from .models import Pedido, Servicio, Tarea`

`class CustomRegisterForm(UserCreationForm):`  
    `# ... campos extra de email, etc.`  
    `pass`

`class CustomLoginForm(AuthenticationForm):`  
    `pass`

`class PedidoFormCliente(forms.ModelForm):`  
    `fecha_inicio = forms.DateField(`  
        `input_formats=['%Y-%m-%d','%d/%m/%Y'],`  
        `widget=forms.DateInput(attrs={'class':'form-control','type':'date'})`  
    `)`  
    `fecha_fin = forms.DateField(`  
        `required=False,`  
        `input_formats=['%Y-%m-%d','%d/%m/%Y'],`  
        `widget=forms.DateInput(attrs={'class':'form-control','type':'date'})`  
    `)`  
    `class Meta:`  
        `model = Pedido`  
        `fields = [`  
            `'fecha_inicio','fecha_fin',`  
            `'empresa','excursion','estado',`  
            `'lugar_entrega','lugar_recogida','notas'`  
        `]`  
    `def clean(self):`  
        `cleaned = super().clean()`  
        `fi = cleaned.get('fecha_inicio')`  
        `ff = cleaned.get('fecha_fin')`  
        `if fi and ff and ff < fi:`  
            `self.add_error('fecha_fin','La fecha fin debe ser ≥ fecha inicio.')`  
        `return cleaned`

`class ServicioForm(forms.ModelForm):`  
    `class Meta:`  
        `model = Servicio`  
        `fields = ['excursion','pax','emisores','lugar_entrega','bono']`  
        `widgets = {`  
            `'excursion': forms.TextInput(attrs={'class':'form-control'}),`  
            `'pax': forms.NumberInput(attrs={'class':'form-control','min':1}),`  
            `'emisores': forms.NumberInput(attrs={'class':'form-control','min':1}),`  
            `'lugar_entrega': forms.TextInput(attrs={'class':'form-control'}),`  
            `'bono': forms.TextInput(attrs={'class':'form-control'}),`  
        `}`

`ServicioFormSet = inlineformset_factory(`  
    `Pedido,`  
    `Servicio,`  
    `form=ServicioForm,`  
    `extra=1,`  
    `can_delete=True`  
`)`

`class TareaForm(forms.ModelForm):`  
    `fecha_especifica = forms.DateField(`  
        `required=False,`  
        `widget=forms.DateInput(attrs={'class':'form-control','type':'date'})`  
    `)`  
    `class Meta:`  
        `model = Tarea`  
        `fields = ['titulo','descripcion','fecha_especifica','completada']`

---

### **`views.py` (fragmento clave de cliente)**

python  
CopiarEditar  
`from django.shortcuts import render, redirect, get_object_or_404`  
`from django.http import HttpResponse`  
`from django.contrib.auth.decorators import login_required`  
`from django.contrib import messages`  
`from .forms import PedidoFormCliente, ServicioFormSet`  
`from .models import Pedido`

`@login_required`  
`def pedido_nuevo_cliente_view(request):`  
    `embed = request.GET.get('embed')=='1' or request.POST.get('embed')=='1'`  
    `form = PedidoFormCliente(request.POST or None)`  
    `servicio_formset = ServicioFormSet(request.POST or None, prefix='servicio')`

    `if request.method == 'POST':`  
        `if form.is_valid() and servicio_formset.is_valid():`  
            `pedido = form.save(commit=False)`  
            `pedido.usuario = request.user`  
            `pedido.save()`

            `servicio_formset = ServicioFormSet(`  
                `request.POST,`  
                `instance=pedido,`  
                `prefix='servicio'`  
            `)`  
            `servicio_formset.save()`

            `if embed:`  
                `return HttpResponse("<script>window.parent.location.reload();</script>")`

            `messages.success(request, "✅ Pedido creado correctamente.")`  
            `return redirect('pedidos:mis_pedidos')`

        `messages.error(request, "Por favor corrige los errores.")`

    `template = "pedidos/pedido_nuevo_cliente_modal.html" if embed else "pedidos/pedido_nuevo_cliente.html"`  
    `return render(request, template, {`  
        `'form': form,`  
        `'formset': servicio_formset,`  
        `'es_edicion': False,`  
        `'embed': embed,`  
    `})`

---

## **15\. Pasos para desplegar/poner en marcha**

**Clona el repositorio** y activa tu entorno virtual:

 bash  
CopiarEditar  
`git clone <tu_repo_url>`  
`cd control_radioguias`  
`python -m venv venv`  
`source venv/bin/activate     # Linux/Mac`  
`venv\Scripts\activate        # Windows`  
`pip install -r requirements.txt`

1.   
2. **Configura variables de entorno**:

   * `DEBUG=False`

   * `SECRET_KEY=<tu_secret_key>`

   * `DATABASE_URL=<postgres://…>`

   * `ALLOWED_HOSTS=innovations-tour-production.up.railway.app`

**Migraciones**:

 bash  
CopiarEditar  
`python manage.py makemigrations`  
`python manage.py migrate`

3. 

**Crea un superusuario** (opcional para staff):

 bash  
CopiarEditar  
`python manage.py createsuperuser`

4. 

**Corre el servidor local** para pruebas:

 bash  
CopiarEditar  
`python manage.py runserver`

5.   
6. **Despliegue en Railway**:

   * Commit & push a GitHub.

   * Railway detecta el cambio y redeploy.

   * Asegúrate de que en Railway estén configuradas las mismas variables de entorno.

---

## **16\. Resumen final**

* El proyecto gestiona **pedidos** y dentro de ellos **servicios**.

* La parte de **autenticación** permite a un cliente crear/editar sus pedidos en modales (embed), y al staff ver/controlar todos los pedidos.

* Los estados de los pedidos se manejan via AJAX en la vista staff, con confirmaciones SweetAlert2.

* Las fechas usan Flatpickr con `altInput` para separar el formato visible (`d/m/Y`) del envío real (`Y-m-d`).

* Los **formsets de servicios** funcionan con `inlineformset_factory(Pedido,Servicio)` y tienen un prefijo `servicio` que actualiza el `TOTAL_FORMS` cada vez que añades o eliminas un servicio.

* Las plantillas usan **Bootstrap 5** para un diseño responsive, con cards en móviles y tablas en desktop.

* Los **modales** (iframe) en `mis_pedidos` y `pedidos_lista` se abren con `?embed=1`, y al hacer submit la vista detecta `embed` y devuelve un pequeño script para recargar la página padre y cerrar el modal.

Con esta guía, cualquier desarrollador podrá conocer:

1. Estructura de archivos y carpetas.

2. Definición y relaciones entre modelos.

3. Formularios (hooks de validación y widgets).

4. Vistas y lógica de negocio (clases/basadas en función).

5. Rutas URL y nombres.

6. Plantillas y cómo se organizan (layouts, parciales, bloques).

7. JavaScript crítico para:

   * Flatpickr (fechas).

   * Formsets dinámicos de servicios.

   * AJAX de cambio de estado.

   * DataTables y bulk actions.

8. Flujo completo de uso (cliente y staff).

9. Reglas para añadir nuevo código sin romper el sistema (mantener un solo form, incluir management\_form, usar embed correctamente, mantener DataTables, etc.).

Si surge cualquier duda puntual, revisando el código con esta documentación en mano el programador sabrá dónde buscar cada sección y cómo extender o modificar la funcionalidad sin errores.

