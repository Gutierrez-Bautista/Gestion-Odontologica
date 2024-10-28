const turnero = document.querySelector(".turnero");

const HOURS_ARRAY = [
  "08:00",
  "08:30",
  "09:00",
  "09:30",
  "10:00",
  "10:30",
  "11:00",
  "11:30",
  "12:00",
  "12:30",
  "13:00",
  "13:30",
  "14:00",
  "14:30",
];

const WEEK_DAYS_ARRAY = ["lunes", "martes", "miercoles", "jueves", "viernes"];

// https://stackoverflow.com/questions/242608/disable-browsers-vertical-and-horizontal-scrollbars

let monday_day_number
let monday_date
let friday_date

function setTurneroHeaders(mondayDate) {
  const monthNumber = parseInt(mondayDate.split('/')[1]) - 1

  document.querySelector('.turnero-month').textContent = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'][monthNumber]

  let dia = monday_day_number
  document.querySelectorAll('.turnero-dia-number').forEach(element => {
    if (monthNumber === 1 && dia > 28) {
      dia = 1
    } else if ([0, 2, 4, 6, 7, 9, 11].includes(monthNumber)) {
      if (dia > 31) {dia = 1}
    } else {
      if (dia > 30) {dia = 1}
    }
    element.textContent = dia
    dia++
  })

  document.querySelector('.turnero-semana > span').textContent = Math.round(monday_day_number / 7)
}

async function mostrarTurno(infoTurno, diaSemana) {
  const div = document.createElement("div");
  div.classList.add("turnos");

  apellidoNombrePaciente = infoTurno[5].split(';')

  const text = document.createTextNode(`${apellidoNombrePaciente[1]} ${apellidoNombrePaciente[0]}`);
  div.appendChild(text);

  const row = HOURS_ARRAY.indexOf(infoTurno[3]) + 3;
  const col = WEEK_DAYS_ARRAY.indexOf(diaSemana) + 2;

  div.style = `grid-row: ${row} / ${row + 1};grid-column: ${col} / ${col + 1}`;

  div.addEventListener('click', (evt) => {funcionalidadTurnosClickeables(infoTurno, evt.currentTarget)})

  turnero.appendChild(div);
}

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
  monday_day_number = week[0].split('/')[0]
  monday_date = week[0]
  friday_date = week[4]
  return [week[0], week[4]];
}

let currentWeek = []

window.addEventListener("DOMContentLoaded", () => {
  const today = new Date();
  currentWeek = getWeekFromADate(
    today.getFullYear(),
    today.getMonth() + 1,
    today.getDate()
  );
  setTurneroHeaders(currentWeek[0])
  actualizarTurnero(currentWeek[0], currentWeek[1]);
});

function actualizarTurnero(fechaLunes, fechaViernes) {
  document.querySelectorAll(".turnos").forEach((t) => {
    turnero.removeChild(t);
  });

  // No devuelve los turnos de la semana, creo que es porque el lunes y el viernes forman parte de distinto mes
  const fetchBodyData = new FormData();
  console.log(fetchBodyData)
  console.log(fechaLunes, fechaViernes)
  fetchBodyData.append("fecha_turno1", fechaLunes);
  fetchBodyData.append("fecha_turno2", fechaViernes);
  
  fetch("http://localhost:8000/api/turnos/get", {
    method: "POST",
    body: fetchBodyData,
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data)
      const frag = document.createDocumentFragment();

      if (data['name'] === 'dataFound') {
        for (t of data['message']) {
          const day_number = t[2].split('/')[0]

          mostrarTurno(t, WEEK_DAYS_ARRAY[parseInt(day_number) - monday_day_number])
        }
      }
      else if (data['name'] === 'dataBaseError') {
        console.error(data)
        alert('Error al recuperar los turnos de la base de datos')
      }
      else {
        alert(`No se han cargado turnos para la semana del lunes ${fechaLunes}`)
      }
    })
    .catch(err => {
      console.error(err);
      alert('Error al recuperar los turnos de la base de datos')
    })
}

const addTurnoButton = document.getElementById("add-turno-button-id");
const addTurnoModal = document.querySelector(".modal-crear-turno");
const closeModalButton = document.querySelector(".close-modal");

const addTurnoForm = document.getElementById("add-turno-form");
const addTurnoError = document.getElementById("add-turno-error");
const addTurnoSucces = document.getElementById("add-turno-succes");

const hourSelect = document.getElementById("select-hour");
const minuteSelect = document.getElementById("select-minute");

addTurnoButton.addEventListener("click", () => {
  addTurnoModal.setAttribute("open", "");
  document.documentElement.style.overflow = "hidden";
});

closeModalButton.addEventListener("click", () => {
  addTurnoModal.removeAttribute("open");
  addTurnoSucces.textContent = ''
  addTurnoError.textContent = ''
  document.documentElement.style.overflow = "visible";
});

const validateHour = () => {
  if (hourSelect.value == "15" && minuteSelect.value == "30") {minuteSelect.value = "00"};
};

hourSelect.addEventListener("input", validateHour);

minuteSelect.addEventListener("input", validateHour);

addTurnoForm.addEventListener("submit", (evt) => {
  evt.preventDefault();
  addTurnoError.textContent = "";
  addTurnoSucces.textContent = "";

  const data = new FormData(addTurnoForm);

  if (data.get("date") === "") {
    addTurnoError.textContent = "No se ha seleccionado el dia";
    return;
  }

  if (data.get("name") === "" || data.get("lastname") === "") {
    addTurnoError.textContent = "Ingrese nombre y apellido";
    return;
  }

  const dateObj = new Date(data.get("date").split("-"));
  const dayIndex = dateObj.getDay() - 1;

  if (dayIndex === 5 || dayIndex === -1) {
    addTurnoError.textContent = "No se atiende los sabados y domingos";
    return;
  }

  data.append('fullname', data.get('firstname') + ';' + data.get('lastname'))
  data.delete('firstname')
  data.delete('lastname')

  let aux = data.get('date').split('-')
  aux = `${aux[2]}/${aux[1]}/${aux[0]}`
  data.delete('date')
  data.append('date', aux)

  console.log(data)

  // Agregar el turno a la base de datos
  fetch('http://localhost:8000/api/turnos/upload', {
    method: 'POST',
    body: data
  })
    .then(res => res.json())
    .then(response => {
      if (response['status'] === 500) {
        addTurnoError.textContent = 'Ocurrio un error al intentar cargar el turno'
        console.log(response[0])
      } else if (response['name'] === 'dataNoUpload') {
        addTurnoError.textContent = `El horario "${data.get('hour')}:${data.get('minute')}" del dia "${aux}" ya esta ocupado`
      } else {
        addTurnoSucces.textContent = 'Turno agregado'
        if (currentWeek.includes(aux)) {
            // mostrar_turno([-, -, -, hour, -, apellidoNombre], day)
            mostrarTurno([0, 0, 0, `${data.get('hour')}:${data.get('minute')}`, 0, data.get('fullname')], WEEK_DAYS_ARRAY[(parseInt(aux.split('/')[0]) - monday_day_number)])
          }
      }
    })
    .catch(err => {
      addTurnoError.textContent = 'Error al conectar con el servidor'
      console.log(err)
    })
});

const turnoInformation = document.querySelector('.modal-turno-information')

async function funcionalidadTurnosClickeables(turnoInfo, turno) {
  if (turno.childNodes.length !== 1) {
    return
  }

  turno.classList.add('turnos-active')
  setTimeout(() => {turno.classList.remove('turnos-active')}, 200)

  const div = document.createElement('div')
  div.classList.add('turno-info')
  
  const title = document.createElement('h3')
  title.textContent = 'Informacion del Turno'
  
  const parrafosDia = document.createElement('p')
  parrafosDia.innerHTML = `Dia: <span>${turnoInfo[2]}</sapn>`
  
  const parrafosHorario = document.createElement('p')
  parrafosHorario.innerHTML = `Hora: <span>${turnoInfo[3]}</span>`
  
  const parrafosPaciente = document.createElement('p')
  parrafosPaciente.innerHTML = `Paciente: <span>${turnoInfo[5].split(';')[1]} ${turnoInfo[5].split(';')[0]}</span>`
  
  const parrafosMotivo = document.createElement('p')
  parrafosMotivo.innerHTML = `Motivo: <span>${turnoInfo[4]}</span>`
  parrafosMotivo.style = 'max-height: 3.6rem; text-wrap: pretty; overflow: scroll'

  const masInfoBtn = document.createElement('button')
  masInfoBtn.textContent = 'Info del paciente'
  masInfoBtn.classList.add('infoPacienteBtn')

  const divModDelBtns = document.createElement('div')
  divModDelBtns.classList.add('edit-delete-container')

  const modBtn = document.createElement('span')
  modBtn.classList.add('modificar-turno-btn')
  const delBtn = document.createElement('span')
  delBtn.classList.add('eliminar-turno-btn')

  modBtn.innerHTML = `<i class='bx bx-pencil'></i> editar`
  delBtn.innerHTML = `<i class='bx bxs-trash'></i> eliminar`

  delBtn.addEventListener('click', () => {
    d = new FormData()
    d.append('hour', turnoInfo[3])
    d.append('day', turnoInfo[2])
    fetch('http://localhost:8000/api/turnos/delete', {
      method: 'DELETE',
      body: d
    })
      .then(res => res.json())
      .then(response => {
        if (response['status'] === 200) {
          turnero.removeChild(turno)
        }
      })
  })

  modBtn.addEventListener('click', () => {crearModalModificarTurno(turnoInfo, turno, div)})

  divModDelBtns.appendChild(modBtn)
  divModDelBtns.appendChild(delBtn)

  div.appendChild(divModDelBtns)
  div.appendChild(title)
  div.appendChild(parrafosDia)
  div.appendChild(parrafosHorario)
  div.appendChild(parrafosPaciente)
  div.appendChild(parrafosMotivo)
  div.appendChild(masInfoBtn)
  
  turno.appendChild(div)

  turno.addEventListener('mouseleave', (evt) => {
    if (div.hasChildNodes()) {
      turno.removeChild(div)
    }
  })
}

function crearModalModificarTurno(infoTurnoActual, turno, modalInfo) {
  const div = document.createElement('div')
  div.classList.add('turno-info')
  
  const title = document.createElement('h3')
  title.textContent = 'Modificacion del Turno'

  const inputDia = document.createElement('input')
  inputDia.setAttribute('type', 'date')
  inputDia.setAttribute('name', "date")
  inputDia.setAttribute('title', `nueva fecha (actual: ${infoTurnoActual[2]})`)
  
  const inputHorarioText = document.createElement('p')
  inputHorarioText.textContent = `Nuevo horario (actual: ${infoTurnoActual[3]})`
  inputHorarioText.style.fontWeight = 'normal'
  const inputHorario = document.createElement('div')
  inputHorario.classList.add('select-hour-container')
  inputHorario.innerHTML = `
              <select name="hour" id="select-hour">
                <option value="08">08</option>
                <option value="09">09</option>
                <option value="10">10</option>
                <option value="11">11</option>
                <option value="12">12</option>
                <option value="13">13</option>
                <option value="14">14</option>
              </select>
              <p>:</p>
              <select name="minute" id="select-minute">
                <option value="00">00</option>
                <option value="30">30</option>
              </select>`
  inputHorario.children[0].value = '-'
  inputHorario.children[2].value = '-'
  
  
  const inputMotivo = document.createElement('textarea')
  inputMotivo.classList.add('textarea')
  inputMotivo.setAttribute('name', 'motivo')
  inputMotivo.setAttribute('placeholder', 'nuevo motivo...')

  const confirmCancelContainer = document.createElement('div')
  const canBtn = document.createElement('button')
  const confBtn = document.createElement('button')

  canBtn.textContent = 'cancelar'
  confBtn.textContent = 'modificar'

  confBtn.addEventListener('click', () => {
    const d = new FormData()
    d.append('fecha-actual', infoTurnoActual[2])
    d.append('hora-actual', infoTurnoActual[3])
    d.append('motivo-actual', infoTurnoActual[4])

    if (inputDia.value === '') {
      fech = ''
    } else {
      fech = inputDia.value.split('-')
      fech = `${fech[2]}/${fech[1]}/${fech[0]}`
    }
    d.append('nueva-fecha', fech)
    if (inputHorario.children[0].value === '' || inputHorario.children[2].value === '') {
      d.append('nueva-hora', '')
    } else {
      d.append('nueva-hora', inputHorario.children[0].value + ':' + inputHorario.children[2].value)
    }
    d.append('nuevo-motivo', inputMotivo.value)

    fetch('http://localhost:8000/api/turnos/update', {
      method: "PUT",
      body: d
    })
      .then(res => res.json())
      .then(response => {
        console.log(response)
        actualizarTurnero(monday_date, friday_date)
      })
      .catch(err => {console.log(err)})
  })

  canBtn.addEventListener('click', () => {
    turno.removeChild(div)
  })

  confirmCancelContainer.appendChild(canBtn)
  confirmCancelContainer.appendChild(confBtn)

  div.appendChild(title)
  div.appendChild(inputDia)
  div.appendChild(inputHorarioText)
  div.appendChild(inputHorario)
  div.appendChild(inputMotivo)
  div.appendChild(confirmCancelContainer)

  turno.removeChild(modalInfo)
  turno.appendChild(div)
}