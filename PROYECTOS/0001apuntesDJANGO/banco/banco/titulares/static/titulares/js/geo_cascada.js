// Selects encadenados del admin de Domicilio: Provincia -> Partido -> Localidad.
document.addEventListener('DOMContentLoaded', function () {
  var prov = document.getElementById('id_sel_provincia');
  var depto = document.getElementById('id_sel_departamento');
  var loc = document.getElementById('id_localidad');
  if (!prov || !depto || !loc) { return; }

  function llenar(select, items) {
    select.innerHTML = '';
    var vacio = document.createElement('option');
    vacio.value = '';
    vacio.textContent = '---------';
    select.appendChild(vacio);
    items.forEach(function (it) {
      var o = document.createElement('option');
      o.value = it.id;
      o.textContent = it.nombre;
      select.appendChild(o);
    });
  }

  function cargar(url, parametro, valor, destino) {
    llenar(destino, []);
    if (!valor) { return; }
    fetch(url + '?' + parametro + '=' + encodeURIComponent(valor), {credentials: 'same-origin'})
      .then(function (r) { return r.json(); })
      .then(function (data) { llenar(destino, data.items); });
  }

  prov.addEventListener('change', function () {
    llenar(loc, []);
    cargar(prov.dataset.url, 'provincia', prov.value, depto);
  });
  depto.addEventListener('change', function () {
    cargar(depto.dataset.url, 'departamento', depto.value, loc);
  });
});
