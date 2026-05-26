// =========================
const flipButton = document.getElementById("flipButton");
const triptico = document.getElementById("triptico");

/* =========================
   FLIP
========================= */

flipButton.addEventListener("click", () => {

  /* DESKTOP */

  if(window.innerWidth > 768){

    triptico.classList.toggle("flip");

    if(triptico.classList.contains("flip")){

      flipButton.textContent = "Ver Parte Frontal";

    }else{

      flipButton.textContent = "Ver Parte Trasera";

    }

  }

  /* MOBILE */

  else{

    triptico.classList.toggle("mobile-flip");

    if(triptico.classList.contains("mobile-flip")){

      flipButton.textContent = "Ver Parte Frontal";

    }else{

      flipButton.textContent = "Ver Parte Trasera";

    }

  }

});


/* =========================
   ACCORDION
========================= */

const panels = document.querySelectorAll(".panel");

panels.forEach(panel => {

  const header = panel.querySelector(".panel-header");

  if(header){

    header.addEventListener("click", () => {

      panels.forEach(p => {

        if(p !== panel){

          p.classList.remove("active");

        }

      });

      panel.classList.toggle("active");

    });

  }

});
