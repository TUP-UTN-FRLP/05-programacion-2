from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from .forms import FormularioEdicionUsuario
from .models import Usuario


class PruebasCrudUsuario(TestCase):
    def setUp(self):
        self.rol_cliente = Group.objects.get(name='Cliente')
        self.administrador = Usuario.objects.create_superuser(
            email='admin@example.com',
            password='ClaveSegura#2026',
            nombre='Camila',
            apellido='Tisera',
            dni='40123456',
            telefono='2215551234',
            fecha_nacimiento='2000-01-15',
        )
        self.administrador.groups.add(Group.objects.get(name='Administrador'))
        self.usuario = Usuario.objects.create_user(
            email='manuel@example.com',
            password='ClaveSegura#2026',
            nombre='Manuel',
            apellido='Lorea',
            dni='39111222',
            telefono='2215555678',
            fecha_nacimiento='1998-06-10',
        )
        self.usuario.groups.add(self.rol_cliente)
        self.client.force_login(self.administrador)

    def datos_usuario(self, **cambios):
        datos = {
            'nombre': 'Joaquin',
            'apellido': 'Tovio',
            'dni': '35123456',
            'telefono': '2215550000',
            'email': 'joaquin@example.com',
            'fecha_nacimiento': '22/03/1999',
            'is_active': 'on',
            'rol': self.rol_cliente.pk,
            'contrasena': 'ClaveSegura#2026',
            'confirmar_contrasena': 'ClaveSegura#2026',
        }
        datos.update(cambios)
        return datos

    def test_lista_usuarios(self):
        respuesta = self.client.get(reverse('usuarios:lista'))

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Lorea, Manuel')

    def test_administracion_muestra_formulario_de_alta(self):
        respuesta = self.client.get('/admin/usuarios/usuario/add/')

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Confirmar contraseña')

    def test_estado_activo_es_el_valor_predeterminado(self):
        self.assertTrue(self.usuario.is_active)

    def test_crear_usuario_con_contrasena_y_rol(self):
        respuesta = self.client.post(reverse('usuarios:crear'), self.datos_usuario())

        self.assertRedirects(respuesta, reverse('usuarios:lista'))
        usuario = Usuario.objects.get(email='joaquin@example.com')
        self.assertTrue(usuario.check_password('ClaveSegura#2026'))
        self.assertTrue(usuario.groups.filter(name='Cliente').exists())

    def test_editar_usuario(self):
        datos = self.datos_usuario(
            nombre='Manuel',
            apellido='Lorea',
            dni='39111222',
            telefono='2215559999',
            email='manuel@example.com',
            fecha_nacimiento='10/06/1998',
        )
        datos.pop('contrasena')
        datos.pop('confirmar_contrasena')
        respuesta = self.client.post(reverse('usuarios:editar', args=[self.usuario.id]), datos)

        self.assertRedirects(respuesta, reverse('usuarios:lista'))
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.telefono, '2215559999')

    def test_eliminar_usuario_requiere_post(self):
        direccion = reverse('usuarios:eliminar', args=[self.usuario.id])
        self.assertEqual(self.client.get(direccion).status_code, 200)
        self.assertTrue(Usuario.objects.filter(pk=self.usuario.id).exists())

        respuesta = self.client.post(direccion)
        self.assertRedirects(respuesta, reverse('usuarios:lista'))
        self.assertFalse(Usuario.objects.filter(pk=self.usuario.id).exists())

    def test_dni_invalido_no_crea_usuario(self):
        respuesta = self.client.post(
            reverse('usuarios:crear'), self.datos_usuario(dni='abc')
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Ingresá un DNI válido de 7 u 8 dígitos.')
        self.assertFalse(Usuario.objects.filter(email='joaquin@example.com').exists())

    def test_telefono_debe_ser_unico(self):
        formulario = FormularioEdicionUsuario({
            'nombre': 'Otra', 'apellido': 'Persona', 'dni': '33123456',
            'telefono': self.usuario.telefono, 'email': 'otra@example.com',
            'fecha_nacimiento': '20/05/1995', 'is_active': 'on',
            'rol': self.rol_cliente.pk,
        })

        self.assertFalse(formulario.is_valid())
        self.assertIn('telefono', formulario.errors)

    def test_fecha_de_nacimiento_debe_usar_dia_mes_anio(self):
        formulario = FormularioEdicionUsuario({
            'nombre': 'Otra', 'apellido': 'Persona', 'dni': '33123456',
            'telefono': '2215550000', 'email': 'otra@example.com',
            'fecha_nacimiento': '1995-05-20', 'is_active': 'on',
            'rol': self.rol_cliente.pk,
        })

        self.assertFalse(formulario.is_valid())
        self.assertIn('fecha_nacimiento', formulario.errors)

    def test_usuarios_no_autorizados_no_acceden_al_crud(self):
        self.client.logout()
        respuesta = self.client.get(reverse('usuarios:lista'))

        self.assertRedirects(respuesta, '/admin/login/?next=/usuarios/')
