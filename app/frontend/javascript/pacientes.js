
// =====================================================
// nombre_apellido,telefono,email,edad,dni,domicilio,fecha_nacimiento,posee_pami
const d = new FormData()
d.append('nombre_apellido', 'carlos;juarez')
d.append('telefono', '123456789')
d.append('email', 'carlos.ju@gmail.com')
d.append('edad', 25)
d.append('dni', '32481294')
d.append('domicilio', 'calle fantastica Nro 7')
d.append('fecha_nacimiento', '09/06/1999')
d.append('posee_pami', 1)


fetch('http://localhost:8000/api/pacientes/alta', {
  method: 'POST',
  body: d
})
  .then(res => res.json())
  .then(response => {console.log(response)})