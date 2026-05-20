/* ========================= */
/* EFECTO 3D TARJETAS */
/* ========================= */

const cards = document.querySelectorAll(".card");

cards.forEach(card => {

  card.addEventListener("mousemove", (e) => {

    const rect = card.getBoundingClientRect();

    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const rotateY = (x - rect.width / 2) / 18;
    const rotateX = -(y - rect.height / 2) / 18;

    card.style.transform = `
      rotateX(${rotateX}deg)
      rotateY(${rotateY}deg)
      translateY(-10px)
    `;

  });

  card.addEventListener("mouseleave", () => {

    card.style.transform = `
      rotateX(0deg)
      rotateY(0deg)
      translateY(0px)
    `;

  });

});