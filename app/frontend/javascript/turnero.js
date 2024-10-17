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

let monday_day_number;

function setTurneroHeaders(mondayDate) {
  const monthNumber = parseInt(mondayDate.split('/')[1]) - 1

  document.querySelector('.turnero-month').textContent = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'][monthNumber]

  let dia = monday_day_number
  document.querySelectorAll('.turnero-dia-number').forEach(element => {
    element.textContent = dia
    dia++
  })

  document.querySelector('.turnero-semana > span').textContent = Math.round(monday_day_number / 7)
}



function mostrarTurno(infoTurno, diaSemana) {
  const div = document.createElement("div");
  div.classList.add("turnos");

  apellidoNombrePaciente = infoTurno[5].split(';')

  const text = document.createTextNode(`${apellidoNombrePaciente[1]} ${apellidoNombrePaciente[0]}`);
  div.appendChild(text);

  const row = HOURS_ARRAY.indexOf(infoTurno[3]) + 3;
  const col = WEEK_DAYS_ARRAY.indexOf(diaSemana) + 2;

  div.style = `grid-row: ${row} / ${row + 1};grid-column: ${col} / ${col + 1}`;

  turnero.appendChild(div);
  // <div class="turnos turno1">Perez Juan</div>
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

  const fetchBodyData = new FormData();
  fetchBodyData.append("fecha_turno1", fechaLunes);
  fetchBodyData.append("fecha_turno2", fechaViernes);
  
  fetch("http://localhost:8000/api/turnos/get", {
    method: "POST",
    body: fetchBodyData,
  })
    .then((res) => res.json())
    .then((data) => {
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

  // \\
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