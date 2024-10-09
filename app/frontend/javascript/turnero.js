const addTurnoButton = document.getElementById("add-turno-button-id");
const addTurnoModal = document.querySelector(".modal-crear-turno");
const closeModalButton = document.querySelector(".close-modal");

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
