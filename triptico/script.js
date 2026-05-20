// =========================
const flipButton = document.getElementById("flipButton");

const triptico = document.getElementById("triptico");

/* ========================= */
/* GIRAR TRIPTICO */
/* ========================= */

flipButton.addEventListener("click", () => {

  triptico.classList.toggle("flip");

  if(triptico.classList.contains("flip")){

    flipButton.innerText = "Ver Parte Frontal";

  }else{

    flipButton.innerText = "Ver Parte Trasera";
  }

});

/* ========================= */
/* EFECTO 3D */
/* ========================= */

document.querySelectorAll(".panel").forEach(panel => {

  panel.addEventListener("mousemove", (e) => {

    const rect = panel.getBoundingClientRect();

    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const rotateY = (x - rect.width / 2) / 20;
    const rotateX = -(y - rect.height / 2) / 20;

    panel.style.transform = `
      rotateX(${rotateX}deg)
      rotateY(${rotateY}deg)
      scale(1.03)
    `;
  });

  panel.addEventListener("mouseleave", () => {

    panel.style.transform = `
      rotateX(0deg)
      rotateY(0deg)
      scale(1)
    `;
  });

});

/* ========================= */
/* TOQUE EN MOVIL */
/* ========================= */

let touchStartX = 0;

document.addEventListener("touchstart", (e) => {

  touchStartX = e.changedTouches[0].screenX;

});

document.addEventListener("touchend", (e) => {

  const touchEndX = e.changedTouches[0].screenX;

  if(touchEndX < touchStartX - 50){

    triptico.classList.add("flip");

    flipButton.innerText = "Ver Parte Frontal";
  }

  if(touchEndX > touchStartX + 50){

    triptico.classList.remove("flip");

    flipButton.innerText = "Ver Parte Trasera";
  }

});