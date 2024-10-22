
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

  basicFormData = new FormData()
  fichaGeneralData = new FormData()
  fichaPamiData = new FormData()
  anamnesisData = new FormData()
  historialOdontologicoData = new FormData()
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

  fetch('http://localhost:8000/api/pacientes/alta', {
    method: 'POST',
    body: reqData
  })
    .then(res => res.json())
    .then(response => {
      console.log(response)
    })
})

let focusedPacienteId = null

function modalInfoClientes(apellido, nombre, id, tel, email, edad, dni, domicilio, fech_nac, pami, div) {
  const datos = [0, id, tel, email, edad, dni, domicilio, fech_nac, pami]
  const hijos = div.children
  hijos.item(0).textContent = apellido + ' ' + nombre
  for (let i = 1; i < datos.length; i++) {
    hijos.item(i).children.item(0).textContent = datos[i]
  }
}

async function crearBtnPaciente(infoPaciente) {
  const nomApe = infoPaciente[1].split(';')
  const tel = infoPaciente[2]
  const pami = infoPaciente[8] === '0' ? 'No' : 'Si'
  
  console.log(nomApe, tel, pami)
  
  const container = document.createElement('div')
  container.classList.add('paciente')

  const pacienteNom = document.createElement('p')
  pacienteNom.classList.add('paciente-nombre')
  pacienteNom.textContent = `${nomApe[1]} ${nomApe[0]}`

  const pacienteTel = document.createElement('p')
  pacienteTel.classList.add('paciente-telefono')
  pacienteTel.innerHTML = `Tel: <span>${tel}</span>`

  const pacientePami = document.createElement('p')
  pacientePami.classList.add('paciente-pami')
  pacientePami.innerHTML = `PAMI: <span>${pami}</span>`
  
  container.appendChild(pacienteNom)
  container.appendChild(pacienteTel)
  container.appendChild(pacientePami)
  
  divInfoBasica = document.querySelector('.paciente-info-basica')
  container.addEventListener('click', () => {
    // [id, nombre_apellido, telefono, email, edad, dni, domicilio, fecha_nacimiento, posee_pami]

    if (divInfoBasica.parentElement === container) {
      return;
    }
    container.classList.add('paciente-clicked')
    setTimeout(() => {
      container.classList.remove('paciente-clicked')
    }, 200);

    modalInfoClientes(nomApe[1], nomApe[0], infoPaciente[0], infoPaciente[2], infoPaciente[3], infoPaciente[4], infoPaciente[5], infoPaciente[6], infoPaciente[7], infoPaciente[8], divInfoBasica)
    divInfoBasica.style = 'display: block'

    container.appendChild(divInfoBasica)
    focusedPacienteId = infoPaciente[0]
  })
  
  container.addEventListener('mouseleave', () => {
    if (divInfoBasica.parentElement !== null) {
      divInfoBasica.parentElement.removeChild(divInfoBasica)
      focusedPacienteId = null
    }
  })

  document.querySelector('.grilla-pacientes').appendChild(container)
}

const btnFicha = document.getElementById('paciente-ficha-btn')
const btnHistoriaClinica = document.getElementById('paciente-historia-clin-btn')
const btnHistoriaOdontologica = document.getElementById('paciente-historia-odon-btn')

const divFichaGeneral = document.getElementById('paciente-ficha-general')
const divFichaPami = document.getElementById('paciente-ficha-pami')
const divHistoriaClinica = document.getElementById('paciente-historial-odontologico')
const divHistoriaOdontologica = document.getElementById('paciente-historia-clinica')

const infoFichaGeneral = document.querySelector('.paciente-ficha-general .info')
const infoFichaPami = document.querySelector('.paciente-ficha-pami .info')
const infoHistoriaClinica = document.querySelector('.paciente-historial-odontologico .info')
const infoHistoriaOdontologica = document.querySelector('.paciente-historia-clinica .info')

// async function buscarInfoPaciente() {
//   fetch('')
// }

btnHistoriaClinica.addEventListener('click', () => {})

// ================

crearBtnPaciente([1, 'pablo;perez', '1234-56-7890', 'perez.pablo@gmail.com', 20, 24012841, 'calle Juarez Nro 12', '04/02/2004', '1'])
crearBtnPaciente([2, 'carlo;ramirez', '3142-56-9708', 'carlos.ramirez@gmail.com', 18, 27192103, 'calle Juarez Nro 20', '10/07/2006', '0'])
crearBtnPaciente([3, 'pedro;rodriguez', '4132-65-0879', 'rodriguez.pedro@gmail.com', 23, 24012841, 'calle Juarez Nro 7', '15/10/2001', '0'])
