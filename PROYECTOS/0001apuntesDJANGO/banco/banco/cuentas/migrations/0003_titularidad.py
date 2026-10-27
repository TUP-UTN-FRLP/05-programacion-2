from django.db import migrations, models
import django.db.models.deletion


def copiar_titulares(apps, schema_editor):
    """Pasa las relaciones existentes (tabla M2M automatica) a Titularidad."""
    Cuenta = apps.get_model('cuentas', 'Cuenta')
    Titularidad = apps.get_model('cuentas', 'Titularidad')
    Antigua = Cuenta.titular.through
    for fila in Antigua.objects.all():
        Titularidad.objects.create(cuenta_id=fila.cuenta_id,
                                   titular_id=fila.titular_id)


def sin_accion(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0002_remove_cuenta_titular_cuenta_titular'),
        ('titulares', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Titularidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_alta', models.DateField(auto_now_add=True)),
                ('es_principal', models.BooleanField(default=False)),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='titularidades', to='cuentas.cuenta')),
                ('titular', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='titularidades', to='titulares.titular')),
            ],
            options={
                'verbose_name': 'titularidad',
                'verbose_name_plural': 'titularidades',
            },
        ),
        migrations.AddConstraint(
            model_name='titularidad',
            constraint=models.UniqueConstraint(fields=('cuenta', 'titular'), name='uniq_cuenta_titular'),
        ),
        migrations.RunPython(copiar_titulares, sin_accion),
        migrations.RemoveField(
            model_name='cuenta',
            name='titular',
        ),
        migrations.AddField(
            model_name='cuenta',
            name='titular',
            field=models.ManyToManyField(related_name='cuentas', through='cuentas.Titularidad', to='titulares.titular'),
        ),
    ]
