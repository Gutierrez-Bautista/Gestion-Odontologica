
// =====================================================
// nombre_apellido,telefono,email,edad,dni,domicilio,fecha_nacimiento,posee_pami
// const d = new FormData()
// d.append('nombre_apellido', 'carlos;juarez')
// d.append('telefono', '123456789')
// d.append('email', 'carlos.ju@gmail.com')
// d.append('edad', 25)
// d.append('dni', '32481294')
// d.append('domicilio', 'calle fantastica Nro 7')
// d.append('fecha_nacimiento', '09/06/1999')
// d.append('posee_pami', 1)


// fetch('http://localhost:8000/api/pacientes/alta', {
//   method: 'POST',
//   body: d
// })
//   .then(res => res.json())
//   .then(response => {console.log(response)})

// =============================
// =============================

function darFormatoFecha(fechaConGuiones) {
  let res = fechaConGuiones.split('-')
  return `${res[2]}/${res[1]}/${res[0]}`
}

const modalAgragarPaciente = document.querySelector('.modal-crear-paciente')
const modalCerrarBtn = document.querySelector('.close-modal')
const botonAgregarPaciente = document.querySelector('.add-button')

botonAgregarPaciente.addEventListener('click', () => {
  modalAgragarPaciente.setAttribute('open', '')
})

modalCerrarBtn.addEventListener('click', () => {
  modalAgragarPaciente.removeAttribute('open')
  const forms = document.getElementsByClassName('modal-body')
  // console.log(forms)

  for (f of forms) {
    if (f.id === 'cliente-basic-form') {
      f.classList.add('show-form')
    } else {
      f.classList.remove('show-form')
    }
  }

  succesText.textContent = ''
  errorText.textContent = ''

  basicFormData = undefined
  fichaGeneralData = undefined
  fichaPamiData = undefined
  anamnesisData = undefined
  historialOdontologicoData = undefined
})

function cambiarFormulario(currentForm, newForm) {
  succesText.textContent = ''
  errorText.textContent = ''
  currentForm.classList.remove('show-form')
  newForm.classList.add('show-form')
}

const clienteBasicForm = document.getElementById('cliente-basic-form')

const clienteFichaGeneralForm = document.getElementById('cliente-fichaGeneral-form')

const clienteFichaPamiForm = document.getElementById('cliente-fichaPami-form')

const clienteAnamnesisForm = document.getElementById('cliente-anamnesis-form')

const clienteHistorialOdontologicoForm = document.getElementById('cliente-historial-odontologico-form')

const clienteOdontogramaForm = document.getElementById('cliente-odontograma-form')

const succesText = document.getElementById('paciente-succes-text')
const errorText = document.getElementById('paciente-error-text')

let basicFormData = new FormData()
let fichaGeneralData = new FormData()
let fichaPamiData = new FormData()
let anamnesisData = new FormData()
let historialOdontologicoData = new FormData()
let odontogramaData = new FormData()

clienteBasicForm.addEventListener('submit', (evt) => {
  evt.preventDefault()

  basicFormData = new FormData(clienteBasicForm)

  const fname = basicFormData.get('firstname')
  const lname = basicFormData.get('lastname')

  if (fname.includes(';') || lname.includes(';')) {
    errorText.textContent = 'El nombre y apellido no pueden tener ";"'
    return
  }

  basicFormData.append('nombre_apellido', fname + ';' + lname)
  basicFormData.delete('firstname')
  basicFormData.delete('lastname')
  
  fetch(`http://localhost:8000/api/pacientes/get?nom_paciente=${basicFormData.get('nombre_apellido')}`)
    .then(res => res.json())
    .then(response => {
      if (response['status'] === 200) {
        errorText.textContent = 'Ya se ha cargado un paciente con ese nombre'
        return
      }

      // calcular edad del paciente
      const birthDate = new Date(basicFormData.get('birthday'))
      const currentDate = new Date()
      const a = new Date(currentDate - birthDate).getFullYear() - 1970
      basicFormData.append('edad', a)

      const aux = basicFormData.get('birthday')
      basicFormData.delete('birthday')
      basicFormData.append('birthday', aux)

      if (basicFormData.get('posee_pami') === '1') {
        cambiarFormulario(clienteBasicForm, clienteFichaPamiForm)
      } else {
        cambiarFormulario(clienteBasicForm, clienteFichaGeneralForm)
      }
    })
})

clienteFichaGeneralForm.addEventListener('submit', (evt) => {
  evt.preventDefault()
  
  fichaGeneralData = new FormData(clienteFichaGeneralForm);

  
  cambiarFormulario(clienteFichaGeneralForm, clienteHistorialOdontologicoForm)
})

clienteFichaPamiForm.addEventListener('submit', (evt) => {
  evt.preventDefault()
  
  fichaPamiData = new FormData(clienteFichaPamiForm)
  
  
  cambiarFormulario(clienteFichaPamiForm, clienteAnamnesisForm)
})

clienteAnamnesisForm.addEventListener('submit', (evt) => {
  evt.preventDefault()
  
  anamnesisData = new FormData(clienteAnamnesisForm)
  
  
  cambiarFormulario(clienteAnamnesisForm, clienteHistorialOdontologicoForm)
})

clienteHistorialOdontologicoForm.addEventListener('submit', (evt) => {
  evt.preventDefault()

  historialOdontologicoData = new FormData(clienteHistorialOdontologicoForm)
  
  cambiarFormulario(clienteHistorialOdontologicoForm, clienteOdontogramaForm)
})

clienteOdontogramaForm.addEventListener('submit', (evt) => {
  evt.preventDefault()
  
  odontogramaData = new FormData(clienteOdontogramaForm)

  console.log(basicFormData)
  console.log(fichaGeneralData)
  console.log(fichaPamiData)
  console.log(anamnesisData)
  console.log(historialOdontologicoData)
  console.log(odontogramaData)
  console.log('===================')

  reqData = new FormData()

  for (const d of basicFormData.entries()) {
    reqData.append(d[0], d[1])
  }
  for (const d of fichaGeneralData.entries()) {
    reqData.append(d[0], d[1])
  }
  for (const d of fichaPamiData.entries()) {
    reqData.append(d[0], d[1])
  }
  for (const d of anamnesisData.entries()) {
    reqData.append(d[0], d[1])
  }
  for (const d of historialOdontologicoData.entries()) {
    reqData.append(d[0], d[1])
  }
  for (const d of odontogramaData.entries()) {
    reqData.append(d[0], d[1])
  }

  console.log(reqData)
})