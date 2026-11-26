from django.urls import path

from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.lista_usuarios, name='lista'),
    path('nuevo/', views.crear_usuario, name='crear'),
    path('<int:usuario_id>/editar/', views.editar_usuario, name='editar'),
    path('<int:usuario_id>/eliminar/', views.eliminar_usuario, name='eliminar'),
]
