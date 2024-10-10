const addTurnoButton = document.getElementById("add-turno-button-id");
const addTurnoModal = document.querySelector(".modal-crear-turno");
const closeModalButton = document.querySelector(".close-modal");
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

console.log(addTurnoButton);
console.log(addTurnoModal);
console.log(closeModalButton);

// https://stackoverflow.com/questions/242608/disable-browsers-vertical-and-horizontal-scrollbars

addTurnoButton.addEventListener("click", () => {
  addTurnoModal.setAttribute("open", "");
  document.documentElement.style.overflow = "hidden";
});

closeModalButton.addEventListener("click", () => {
  addTurnoModal.removeAttribute("open");
  document.documentElement.style.overflow = "visible";
});

function mostrarTurno(infoTurno, diaSemana) {
  const div = document.createElement("div");
  div.classList.add("turnos");

  const text = document.createTextNode(`ID paciente: ${infoTurno[1]}`);
  div.appendChild(text);

  const row = HOURS_ARRAY.indexOf(infoTurno[3]) + 3;
  const col = WEEK_DAYS_ARRAY.indexOf(diaSemana) + 2;

  div.style = `grid-row: ${row} / ${row + 1};grid-column: ${col} / ${col + 1}`;

  turnero.appendChild(div);
  // <div class="turnos turno1">Perez Juan</div>
}

mostrarTurno([2, 10, "09/10/2024", "10:30"], "jueves");
mostrarTurno([2, 7, "09/10/2024", "09:00"], "viernes");

function getWeekFromADate(year, month, day) {
  const today = new Date(year, month - 1, day);
  const week = [];

  for (let i = 1; 1 <= 7; i++) {
    let first = today.getDate() - today.getDay() + i;
    const day = new Date(today.setDate(first))
      .toISOString()
      .slice(0, 10)
      .split("-");
    console.log(day);
    const formatedDay = `${day[2]}/${day[1]}/${day[0]}`;
    week.push(formatedDay);
    if (i === 5) break;
  }
  return week;
}

window.addEventListener("DOMContentLoaded", () => {
  const today = new Date();
  currentWeek = getWeekFromADate(
    today.getFullYear(),
    today.getMonth() + 1,
    today.getDate()
  );
  actualizarTurnero(currentWeek);
});

function actualizarTurnero(fechasSemanaArray) {
  document.querySelectorAll(".turnos").forEach((t) => {
    turnero.removeChild(t);
  });

  const frag = document.createDocumentFragment();

  for (fech of fechasSemanaArray) {
    const dia = fech.split("-");
    const fetchBodyData = new FormData();
    fetchBodyData.append("fecha_turno", dia.join("/"));
    console.log(dia);
    fetch("http://localhost:8000/api/enviar", {
      method: "POST",
      body: fetchBodyData,
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
      });
  }
}
