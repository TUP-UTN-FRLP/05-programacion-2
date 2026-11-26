from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404 as obtener_o_404
from django.shortcuts import redirect as redirigir
from django.shortcuts import render as renderizar

from .forms import FormularioAltaUsuario, FormularioEdicionUsuario
from .models import Usuario


@staff_member_required(login_url='/admin/login/')
def lista_usuarios(solicitud):
    usuarios = Usuario.objects.all()
    return renderizar(solicitud, 'usuarios/lista_usuarios.html', {
        'usuarios': usuarios,
    })


@staff_member_required(login_url='/admin/login/')
def crear_usuario(solicitud):
    formulario = FormularioAltaUsuario(solicitud.POST or None)
    if solicitud.method == 'POST' and formulario.is_valid():
        formulario.save()
        return redirigir('usuarios:lista')
    return renderizar(solicitud, 'usuarios/formulario_usuario.html', {
        'formulario': formulario,
        'titulo': 'Nuevo usuario',
        'boton': 'Registrar usuario',
    })


@staff_member_required(login_url='/admin/login/')
def editar_usuario(solicitud, usuario_id):
    usuario = obtener_o_404(Usuario, pk=usuario_id)
    formulario = FormularioEdicionUsuario(solicitud.POST or None, instance=usuario)
    if solicitud.method == 'POST' and formulario.is_valid():
        formulario.save()
        return redirigir('usuarios:lista')
    return renderizar(solicitud, 'usuarios/formulario_usuario.html', {
        'formulario': formulario,
        'titulo': 'Editar usuario',
        'boton': 'Guardar cambios',
        'usuario': usuario,
    })


@staff_member_required(login_url='/admin/login/')
def eliminar_usuario(solicitud, usuario_id):
    usuario = obtener_o_404(Usuario, pk=usuario_id)
    if solicitud.method == 'POST':
        usuario.delete()
        return redirigir('usuarios:lista')
    return renderizar(solicitud, 'usuarios/confirmar_eliminacion.html', {'usuario': usuario})
