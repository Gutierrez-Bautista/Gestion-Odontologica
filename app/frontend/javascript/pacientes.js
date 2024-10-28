function darFormatoFecha(fechaConGuiones) {
  let res = fechaConGuiones.split('-')
  if (res[2] && res[1] && res[0]) {
    return `${res[2]}/${res[1]}/${res[0]}`
  }
  return ''
}

// MODAL DE ALTA DE PACIENTE
let modalMode = 'alta'
const modalAgragarPaciente = document.querySelector('.modal-crear-paciente')
const modalCerrarBtn = document.querySelector('.close-modal')
const botonAgregarPaciente = document.querySelector('.add-button')

botonAgregarPaciente.addEventListener('click', () => {
  modalAgragarPaciente.setAttribute('open', '')
})

function cerrarModalAgregar() {
  modalAgragarPaciente.removeAttribute('open')

  modalAgragarPaciente.children[0].children[0].children[0].innerHTML = '<h3>Alta Paciente</h3>'
  const forms = document.getElementsByClassName('modal-body')
  
  for (f of forms) {
    if (f.id === 'cliente-basic-form') {
      f.classList.add('show-form')
    } else {
      f.classList.remove('show-form')
    }
  }
  
  if (modalMode !== 'alta') {
    const inputs = document.querySelectorAll('.modal-body input')
    document.getElementById('estado').setAttribute('required', '')
    inputs.forEach(inp => {
      if (!['obra-social', 'n-afiliado', 'alergias', 'titular', 'parentesco', 'trat-med', 'medicacion', 'alergias-drogas'].includes(inp.getAttribute('name'))) {
        inp.setAttribute('required', '')
      }
    })
  }

  modalMode = 'alta'
  succesText.textContent = ''
  errorText.textContent = ''

  basicFormData = new FormData()
  fichaGeneralData = new FormData()
  fichaPamiData = new FormData()
  anamnesisData = new FormData()
  historialOdontologicoData = new FormData()
}

modalCerrarBtn.addEventListener('click', cerrarModalAgregar)

// FORMULARIOS DE ALTA PACIENTES
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
      // let aux = .split('/')
      const birthDate = new Date(basicFormData.get('fecha_nacimiento'))
      const currentDate = new Date()
      const a = new Date(currentDate - birthDate).getFullYear() - 1970

      basicFormData.append('edad', a)

      const aux = darFormatoFecha(basicFormData.get('fecha_nacimiento'))
      basicFormData.delete('fecha_nacimiento')
      basicFormData.append('fecha_nacimiento', aux)

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

  const fecha = fichaPamiData.get('fecha')
  const fechaFormateada = darFormatoFecha(fecha)
  fichaPamiData.delete('fecha')
  fichaPamiData.append('fecha', fechaFormateada)
  
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

  reqData = new FormData()

  console.log(focusedPacienteInfo)

  if (modalMode !== 'alta') {
    for (const d of basicFormData.entries()) {
      if (d[0] === 'nombre_apellido') {
        if (d[1] === '' || (d[1][0] === ';' || d[1].endsWith(';'))) {
          basicFormData.set('nombre_apellido', focusedPacienteInfo['basic'][0])
        }
      } else if (d[1] === 'NaN') {
        basicFormData.set('edad', focusedPacienteInfo['basic'][3])
        basicFormData.set('fecha_nacimiento', focusedPacienteInfo['basic'][6])
      } else if (d[1] === ''){
        basicFormData.set(d[0], focusedPacienteInfo['basic'][[0, 'telefono', 'email', 0, 'dni', 'domicilio'].indexOf(d[0])])
      }
    }

    if (basicFormData.get('posee_pami') === '0' && focusedPacientePami === 0) {
      let i = 0
      for (const d of fichaGeneralData.entries()) {
        if (d[1] === '') {
          fichaGeneralData.set(d[0], focusedPacienteInfo['ficha'][i])
        }
        i++
      }
    } else if (basicFormData.get('posee_pami') === '1' && focusedPacientePami === 1) {
      let i = 0
      for (const d of fichaPamiData.entries()) {
        if (i === 1) {i++}
        if (d[1] === '' && d[0] !== 'fecha') {
          fichaPamiData.set(d[0], focusedPacienteInfo['ficha'][i])
        } else if (d[1] === '') {
          fichaPamiData.set('fecha', focusedPacienteInfo['ficha'][1])
        }
        i++
      }
      i = 0
      for (const d of anamnesisData.entries()) {
        if (d[1] === '') {
          anamnesisData.set(d[0], focusedPacienteInfo['anamnesis'][i])
        }
        i++
      }
    }

    let i = 0
    for (const d of historialOdontologicoData.entries()) {
      if (d[1] === '') {
        historialOdontologicoData.set(d[0], focusedPacienteInfo['histOdon'][i])
      }
      i++
    }
    
    i = 0
    for (const d of odontogramaData.entries()) {
      if (d[1] === '') {
        odontogramaData.set(d[0], focusedPacienteInfo['odontograma'][i])
      }
      i++
    }
  }

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

  if (modalMode !== 'alta') {
    /*
    Punto en el que estoy:
      # Se cambia la configuracion del modal de alta paciente para que funcione tambien para la modificacion de Ficha. Falta hacerlo en historial odontologico.
      # No esta implementado que al ir a modificar ficha solo te pida cargar los datos basicos, de ficha y del odontograma; lo mismo con el historial odontologico.
    */
    // HACER PETICION AL BACKEND PARA ACTUALIZAR LOS DATOS
    return
  }

  fetch('http://localhost:8000/api/pacientes/alta', {
    method: 'POST',
    body: reqData
  })
    .then(res => res.json())
    .then(response => {
      if (response['message'][2] === 200) {
        succesText.textContent = 'Paciente cargado'
        setTimeout(cerrarModalAgregar, 700)
      } else {
        errorText.textContent = 'No se pudo cargar el paciente'
      }
    })
})

// MUESTRA DE DATOS PACIENTES
let focusedPacienteId = null
let focusedPacientePami = null
let focusedPacienteInfo = null

function modalInfoClientes(apellido, nombre, id, tel, email, edad, dni, domicilio, fech_nac, pami, div) {
  const datos = [0, -1, tel, email, edad, dni, domicilio, fech_nac, pami]
  const hijos = div.children
  hijos.item(0).textContent = apellido + ' ' + nombre
  hijos.item(1).textContent = id
  for (let i = 2; i < datos.length; i++) {
    hijos.item(i).children.item(0).textContent = datos[i] === null ? 'No cargado' : (datos[i] === 1 || datos[i] === 0 ? (datos[i] === 1 ? 'Si' : 'No') : datos[i])
  }
  focusedPacienteId = id
  focusedPacientePami = pami
}

async function crearBtnPaciente(infoPaciente) {
  const nomApe = infoPaciente[1].split(';')
  const tel = infoPaciente[2] ?? 'No cargado'
  const pami = infoPaciente[8] === 0 ? 'No' : 'Si'
  
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
    focusedPacientePami = infoPaciente[8]
  })

  container.addEventListener('mouseleave', () => {
    if (divInfoBasica.parentElement === container) {
      container.removeChild(divInfoBasica)
      document.body.appendChild(divInfoBasica)
      divInfoBasica.style = 'display: none'
    }
  })

  document.querySelector('.grilla-pacientes').appendChild(container)
}

const btnFicha = document.getElementById('paciente-ficha-btn')
const btnHistoriaClinica = document.getElementById('paciente-historia-clin-btn')
const btnHistoriaOdontologica = document.getElementById('paciente-historia-odon-btn')

const divFichaGeneral = document.getElementById('paciente-ficha-general')
const divFichaPami = document.getElementById('paciente-ficha-pami')
const divHistoriaClinica = document.getElementById('paciente-historia-clinica')
const divHistoriaOdontologica = document.getElementById('paciente-historial-odontologico')
const allInfoDivs = document.querySelectorAll('.div-info-paciente')

const infoFichaGeneral = document.querySelector('#paciente-ficha-general .info')
const infoFichaPami = document.querySelector('#paciente-ficha-pami .info')
const infoHistoriaOdontologica = document.querySelector('#paciente-historial-odontologico .info')
const infoHistoriaClinica = document.querySelector('#paciente-historia-clinica .info')
const allCloseBtns = document.querySelectorAll('.div-info-paciente i')

allCloseBtns.forEach(e => {
  e.addEventListener('click', () => {
    e.parentElement.parentElement.classList.remove('show-info')
  })
})

async function buscarInfoPaciente() {
  let a
  await fetch(`http://localhost:8000/api/pacientes/get?id_paciente=${focusedPacienteId}`)
    .then(res => res.json())
    .then(data => {a = data})
    .catch(err => {
      console.log(err)
      alert('Error al conectar con el servidor, por favor reiniciar aplicacion')
    })
  focusedPacienteInfo = a['name']
  const basic = [...focusedPacienteInfo['basic']]
  basic.shift()
  const ficha = [...focusedPacienteInfo['ficha']]
  ficha.splice(0, 2)
  const odontograma = [...focusedPacienteInfo['odontograma']]
  odontograma.splice(0, 2)
  const histOdon = [...focusedPacienteInfo['historial_odontologico']]
  histOdon.splice(0, 2)
  let anamnesis

  if (typeof focusedPacienteInfo['anamnesis'] !== 'string') {
    anamnesis = [...focusedPacienteInfo['anamnesis']]
    anamnesis.splice(0, 2)
  } else {
    anamnesis = focusedPacienteInfo['anamnesis']
  }

  focusedPacienteInfo = {
    "basic": basic,
    "ficha": ficha,
    "odontograma": odontograma,
    "histOdon": histOdon,
    "anamnesis": anamnesis
  }
  return a
}

// No esta implementado en el backend
btnHistoriaClinica.addEventListener('click', async () => {
  for (d of allInfoDivs) {
    d.classList.remove('show-info')
  }
  divHistoriaClinica.classList.add('show-info')
  data = await buscarInfoPaciente()
})

// Hecho
btnFicha.addEventListener('click', async () => {
  let data = await buscarInfoPaciente()

  if (data['status'] !== 200) {
    return;
  }

  data = data['name']
  
  for (d of allInfoDivs) {
    d.classList.remove('show-info')
  }

  let infoFicha

  if (focusedPacientePami === 1) {
    divFichaPami.classList.add('show-info')
    infoFicha = infoFichaPami
  } else {
    divFichaGeneral.classList.add('show-info')
    infoFicha = infoFichaGeneral
  }

  const basic = [...data['basic']]
  basic.shift()
  const ficha = [...data['ficha']]
  ficha.splice(0, 2)
  const odontograma = [...data['odontograma']]
  odontograma.splice(0, 2)
  let anamnesis = [...data['anamnesis']]

  let dataInOneArray
  if (focusedPacientePami === 1) {
    anamnesis.splice(0, 2)
    dataInOneArray = [...basic, ...ficha, ...anamnesis, ...odontograma]
  } else {
    dataInOneArray = [...basic, ...ficha, ...odontograma]
  }

  dataIndex = 0
  for (let i = 0; i < infoFicha.children.length; i++) {
    child = infoFicha.children[i]
    if (child.tagName === 'P') {
      const val = dataInOneArray[dataIndex] === null ? 'No cargado' : (dataInOneArray[dataIndex] === 0 || dataInOneArray[dataIndex] === 1 ? (dataInOneArray[dataIndex] === 0 ? 'No' : 'Si') : dataInOneArray[dataIndex])
      child.children[0].textContent = val
      dataIndex++
    } else if (child.tagName === 'H3') {
      const nomApe = dataInOneArray[0].split(';')
      child.textContent = `${nomApe[1]} ${nomApe[0]}`
      dataIndex++
    }
  }
})

// Hecho
btnHistoriaOdontologica.addEventListener('click', async () => {
  for (d of allInfoDivs) {
    d.classList.remove('show-info')
  }
  divHistoriaOdontologica.classList.add('show-info')

  let data = await buscarInfoPaciente()


  if (data['status'] !== 200) {
    return
  }

  nomApe = data['name']['basic'][1].split(';')

  data = data['name']['historial_odontologico']

  infoHistoriaOdontologica.children[2].textContent = `${nomApe[1]} ${nomApe[0]}`

  for (let i = 3; i < infoHistoriaOdontologica.children.length; i++) {
    span = infoHistoriaOdontologica.children[i].children[0]
    if (i === 8) {
      span.textContent = data[i]
    } else {
      span.textContent = data[i] === null ? 'No cargado' : (data[i] === 1 || data[i] === 0 ? (data[i] === 1 ? 'Si' : 'No') : data[i])
    }
  }
})

// CONSULTA POR NOMBRE
function getWeekFromADate(year, month, day) {
  const today = new Date(year, month - 1, day);
  const week = [];

  for (let i = 1; 1 <= 7; i++) {
    let first = today.getDate() - today.getDay() + i;
    const day = new Date(today.setDate(first))
      .toISOString()
      .slice(0, 10)
      .split("-");
    const formatedDay = `${day[2]}/${day[1]}/${day[0]}`;
    week.push(formatedDay);
    if (i === 5) break;
  }
  // monday_day_number = week[0].split('/')[0]
  // monday_date = week[0]
  // friday_date = week[4]
  return [week[0], week[4]];
}

window.addEventListener('DOMContentLoaded', async () => {
  const today = new Date()
  currentWeek = getWeekFromADate(
    today.getFullYear(),
    today.getMonth() + 1,
    today.getDate()
  );

  const fetchBodyData = new FormData()
  fetchBodyData.append("fecha_turno1", currentWeek[0])
  fetchBodyData.append("fecha_turno2", currentWeek[1])
  
  fetch("http://localhost:8000/api/turnos/get", {
    method: "POST",
    body: fetchBodyData,
  })
    .then((res) => res.json())
    .then(response => {
      if (response['status'] !== 200) {
        alert('No se cargaron turno para esta semana por lo que no se muestran pacientes')
        return
      }

      const data = response['message']
      for (t of data) {
        fetch(`http://localhost:8000/api/pacientes/get?id_paciente=${t[1]}`)
          .then(res => res.json())
          .then(response => {
            crearBtnPaciente(response['name']['basic'])
          })
      }
    })
})

const formBuscar = document.getElementById('form-buscar-paciente')

formBuscar.addEventListener('submit', evt => {
  evt.preventDefault()

  const reqData = new FormData(formBuscar)

  fetch(`http://localhost:8000/api/pacientes/get?nom_paciente=${reqData.get('busqueda-paciente')}`)
    .then(res => res.json())
    .then(response => {
      if (response['status'] !== 200) {
        alert(`No hay pacientes cuyo nombre o apellido comience con: "${reqData.get('busqueda-paciente')}"`)
        return
      }
      document.querySelector('.grilla-pacientes').innerHTML = ''
      const data = response['name']

      data.forEach(element => {
        crearBtnPaciente(element)
      });
    })
})

// MODIFICACION
const modificarFichaGenBtn = document.getElementById('modif-ficha-general')
const modificarFichaPamiBtn = document.getElementById('modif-ficha-pami')
const modificarHistorialOdontologicoBtn = document.getElementById('modif-hist-odon')
const modificarHistoriaClinicaBtn = document.getElementById('modif-hist-clinica')

function fichaModify() {
  modalMode = 'modificacion-ficha'

  const inputs = document.querySelectorAll('.modal-body input')
  inputs.forEach(inp => {
    if (!['obra-social', 'n-afiliado', 'alergias', 'titular', 'parentesco', 'trat-med', 'medicacion', 'alergias-drogas'].includes(inp.getAttribute('name'))) {
      inp.removeAttribute('required')
    }
  })

  modalAgragarPaciente.children[0].children[0].children[0].innerHTML = '<h3>Modificar Pacientes</h3><span>(Dejar en blanco lo que no se quiera modificar)</span>'

  modalAgragarPaciente.setAttribute('open', '')
}

modificarFichaGenBtn.addEventListener('click', () => {
  fichaModify()

  divFichaGeneral.classList.remove('show-info')
})

modificarFichaPamiBtn.addEventListener('click', () => {
  fichaModify()

  divFichaPami.classList.remove('show-info')
})